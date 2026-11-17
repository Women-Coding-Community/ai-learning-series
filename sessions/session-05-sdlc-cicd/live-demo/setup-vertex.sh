#!/usr/bin/env bash
# Let ONE GitHub repo call Vertex AI from GitHub Actions with no API key.
#
#   ./setup-vertex.sh <gcp-project-id> <owner>/<repo>
#
# Example:
#   ./setup-vertex.sh my-project octocat/shipit-ci-demo
#
# What it creates in your Google Cloud project:
#   - a Workload Identity pool "github" and a provider that only trusts <owner>/<repo>
#   - a service account "shipit-reviewer" with one role: Vertex AI User
#   - permission for that one repo to act as the service account
# What it sets on the GitHub repo (plain variables, nothing secret):
#   WORKLOAD_IDENTITY_PROVIDER, VERTEX_SERVICE_ACCOUNT,
#   GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION
#
# Needs: gcloud and gh, both signed in. You must be Owner (or IAM admin) on the
# project and admin on the repo. Safe to run twice: existing pieces are kept.
#
# Using a different Google login from your gcloud default? Prefix the command:
#   CLOUDSDK_CORE_ACCOUNT=you@example.com ./setup-vertex.sh ...
set -euo pipefail

PROJECT="${1:?usage: ./setup-vertex.sh <gcp-project-id> <owner>/<repo>}"
REPO="${2:?usage: ./setup-vertex.sh <gcp-project-id> <owner>/<repo>}"
LOCATION="${GOOGLE_CLOUD_LOCATION:-global}"
POOL="github"
PROVIDER="$(basename "$REPO" | tr '[:upper:]_.' '[:lower:]--' | cut -c1-32)"
SA_NAME="shipit-reviewer"
SA="$SA_NAME@$PROJECT.iam.gserviceaccount.com"

case "$REPO" in */*/*|*" "*) echo "Repo must be <owner>/<repo>, for example octocat/shipit-ci-demo" >&2; exit 2;; esac
case "$REPO" in */*) ;; *) echo "Repo must be <owner>/<repo>, for example octocat/shipit-ci-demo" >&2; exit 2;; esac

g() { gcloud "$@" --project "$PROJECT"; }

echo "Checking access to $PROJECT and $REPO..."
NUM="$(gcloud projects describe "$PROJECT" --format='value(projectNumber)')"
gh repo view "$REPO" --json name >/dev/null

echo "1/5 Enabling the APIs this needs..."
g services enable aiplatform.googleapis.com iam.googleapis.com \
  iamcredentials.googleapis.com sts.googleapis.com >/dev/null

echo "2/5 Workload Identity pool..."
g iam workload-identity-pools describe "$POOL" --location global >/dev/null 2>&1 ||
  g iam workload-identity-pools create "$POOL" --location global \
    --display-name "GitHub Actions" >/dev/null

echo "3/5 Provider that trusts only $REPO..."
# The attribute condition is the guardrail. Without it, any GitHub repo in the
# world could ask this provider for a token.
g iam workload-identity-pools providers describe "$PROVIDER" --location global \
  --workload-identity-pool "$POOL" >/dev/null 2>&1 ||
  g iam workload-identity-pools providers create-oidc "$PROVIDER" --location global \
    --workload-identity-pool "$POOL" \
    --issuer-uri https://token.actions.githubusercontent.com \
    --attribute-mapping "google.subject=assertion.sub,attribute.repository=assertion.repository" \
    --attribute-condition "assertion.repository=='$REPO'" >/dev/null

echo "4/5 Service account with one role (Vertex AI User)..."
if ! g iam service-accounts describe "$SA" >/dev/null 2>&1; then
  g iam service-accounts create "$SA_NAME" --display-name "ShipIt demo AI reviewer" >/dev/null
  sleep 8 # a new service account takes a few seconds to be usable in IAM
fi
gcloud projects add-iam-policy-binding "$PROJECT" --role roles/aiplatform.user \
  --member "serviceAccount:$SA" --condition None >/dev/null
g iam service-accounts add-iam-policy-binding "$SA" --role roles/iam.workloadIdentityUser \
  --member "principalSet://iam.googleapis.com/projects/$NUM/locations/global/workloadIdentityPools/$POOL/attribute.repository/$REPO" >/dev/null

echo "5/5 Repo variables..."
gh variable set WORKLOAD_IDENTITY_PROVIDER --repo "$REPO" \
  --body "projects/$NUM/locations/global/workloadIdentityPools/$POOL/providers/$PROVIDER"
gh variable set VERTEX_SERVICE_ACCOUNT --repo "$REPO" --body "$SA"
gh variable set GOOGLE_CLOUD_PROJECT --repo "$REPO" --body "$PROJECT"
gh variable set GOOGLE_CLOUD_LOCATION --repo "$REPO" --body "$LOCATION"

cat <<EOF

Done. $REPO can now call Vertex AI in $PROJECT with no API key.

Check it:   gh variable list --repo $REPO
Try it:     open a pull request, the "Authenticate to Google Cloud" step should run.
Spend:      AI Studio spend caps do not cover Vertex AI. Set a budget alert:
            https://console.cloud.google.com/billing/budgets

Undo everything this script made:
  gcloud iam service-accounts delete $SA --project $PROJECT
  gcloud iam workload-identity-pools providers delete $PROVIDER --location global --workload-identity-pool $POOL --project $PROJECT
  gcloud iam workload-identity-pools delete $POOL --location global --project $PROJECT
  for v in WORKLOAD_IDENTITY_PROVIDER VERTEX_SERVICE_ACCOUNT GOOGLE_CLOUD_PROJECT GOOGLE_CLOUD_LOCATION; do gh variable delete \$v --repo $REPO; done
EOF
