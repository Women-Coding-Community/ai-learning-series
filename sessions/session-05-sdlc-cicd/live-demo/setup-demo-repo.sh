#!/usr/bin/env bash
# Create the throwaway demo repo from shipit-ci/ and stage the first demo PR.
#
#   ./setup-demo-repo.sh <owner>/<repo-name>
#
# Run it once the night before. It creates a PRIVATE repo on your account,
# pushes main, and pushes the add-refunds branch WITHOUT opening the PR, so
# you open it live. It never touches the ai-learning-series repo.
# It does not store your API key: you add that yourself (step printed at the end).
set -euo pipefail

REPO="${1:?usage: ./setup-demo-repo.sh <owner>/<repo-name>}"
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="$(mktemp -d)"

cp -R "$HERE/shipit-ci/." "$WORK/"
find "$WORK" -name __pycache__ -prune -exec rm -rf {} +
cd "$WORK"

git init -q -b main
git add -A
git commit -qm "ShipIt with an AI review check"
gh repo create "$REPO" --private --source . --push

# The environment that holds the key. Add required reviewers in the UI.
gh api -X PUT "repos/$REPO/environments/ai-review" >/dev/null

# PR 1: a refunds feature with planted bugs that pass lint and tests.
git switch -qc add-refunds
cp -R "$HERE/demo-prs/01-refunds/." .
git add -A
git commit -qm "Add refunds endpoint"
git push -q -u origin add-refunds
git switch -q main

cat <<EOF

Repo ready: https://github.com/$REPO
Local clone: $WORK

Still to do by hand:
  1. Add the key to the environment (paste it when prompted, it is not echoed):
       gh secret set GEMINI_API_KEY --env ai-review --repo $REPO
  2. Settings > Environments > ai-review: add yourself as a required reviewer.
  3. Settings > Actions > General: allow Actions to create pull requests
     (only needed for the dependency audit draft PR).
  4. Optional model variables, if you want the small-model split:
       gh variable set REVIEW_MODEL_SMALL --repo $REPO --body <small model id>
       gh variable set REVIEW_MODEL --repo $REPO --body <larger model id>
  5. Open PR 1 as a rehearsal, then close it and delete the comment:
       gh pr create --repo $REPO --head add-refunds --title "Add refunds endpoint" --body "Adds POST /refund."
EOF
