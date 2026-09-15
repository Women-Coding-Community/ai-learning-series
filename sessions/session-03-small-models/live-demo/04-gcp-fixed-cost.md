# Way 4: Deploy Your Own Gemma 4 Endpoint on GCP for a Fixed Cost

**Session:** Harness Series, Session 3, Small Models in Practice
**Cost:** ⚠️ Real money, billed by the hour while the endpoint is up, regardless of traffic. See cost notes below. Not zero-cost like Ways 1 to 3.
**Time to test:** 20 to 30 minutes, mostly waiting for the deployment to come up

---

## Why This Way, and What "Fixed Cost" Means Here

Ways 1 to 3 are all £0. This one isn't, deliberately, because it demonstrates the other side of the trade-off: a dedicated Vertex AI endpoint bills a predictable hourly rate for the machine type and GPU you chose, whatever your traffic looks like, unlike a pay-per-token frontier API where cost scales with usage. That predictability is genuinely useful at production scale, but it means the meter runs even when nobody's calling it. **Delete the endpoint the moment you're done testing.**

---

## ⚠️ Before You Start

1. This spins up a **real GPU-backed endpoint** on your GCP billing account
2. Set a budget alert on your project before you begin (Billing → Budgets & alerts)
3. Do a full deploy → test → delete cycle as a dry run **before** the live session, so you know the timing and aren't waiting on a cold start in front of the group
4. Model IDs and available machine types in Model Garden change over time, run the `list-deployment-config` step below to confirm current names rather than trusting anything hardcoded

---

## Prerequisites

- A GCP project with billing enabled
- `gcloud` CLI installed and authenticated (`gcloud auth login`)
- Vertex AI API enabled on the project:
  ```bash
  gcloud services enable aiplatform.googleapis.com --project=YOUR_PROJECT_ID
  ```
- Quota for at least one GPU (T4 or L4) in your chosen region, check under IAM & Admin → Quotas if you've never deployed a GPU workload in this project before

---

## Step 1: Set Your Project and Region

```bash
export PROJECT_ID="your-project-id"
export REGION="us-central1"

gcloud config set project "${PROJECT_ID}"
```

---

## Step 2: Find the Current Gemma 4 Model ID

Don't hardcode a model ID from memory, list what's actually available right now:

```bash
gcloud ai model-garden models list --model-filter="gemma4"
```

Note the exact model ID for the size you want, e.g. something like `google/gemma4@gemma-4-e4b-it`. Use the smallest variant for testing, it deploys faster and costs less per hour.

---

## Step 3: Check the Deployment Config for That Model

```bash
gcloud ai model-garden models list-deployment-config \
  --model="MODEL_ID_FROM_STEP_2"
```

This tells you the supported machine types and accelerator options for that specific model size, use it to pick something sensible, don't guess.

---

## Step 4: Deploy

```bash
gcloud ai model-garden models deploy \
  --model="MODEL_ID_FROM_STEP_2" \
  --machine-type="g2-standard-8" \
  --accelerator-type="NVIDIA_L4" \
  --accelerator-count=1 \
  --endpoint-display-name="gemma4-harness-demo" \
  --accept-eula
```

This runs asynchronously and typically takes several minutes to come up. Check status:

```bash
gcloud ai endpoints list --project="${PROJECT_ID}" --region="${REGION}"
```

Note the `ENDPOINT_ID` once it shows as ready.

---

## Step 5: Test the Endpoint

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  "https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${REGION}/endpoints/ENDPOINT_ID:predict" \
  -d '{
    "instances": [{"prompt": "Explain what a Skill file does in an agent harness, in two sentences."}]
  }'
```

You should get back a JSON response with a generated completion.

---

## Step 6: Plug It Into Your Harness

Point the Session 1 Skill and Session 2 MCP/permissions config at this endpoint URL instead of `localhost:11434`, same pattern, different backend: same Skill, same governance layer, now running on a dedicated Cloud endpoint.

---

## Step 7: Delete It (Do Not Skip This)

```bash
gcloud ai endpoints delete ENDPOINT_ID \
  --project="${PROJECT_ID}" \
  --region="${REGION}"
```

Confirm it's gone:

```bash
gcloud ai endpoints list --project="${PROJECT_ID}" --region="${REGION}"
```

If it doesn't appear in the list, you're clear. **Do this immediately after testing, and again immediately after the live demo.**

---

## Cost Notes (Check Current Pricing Before the Session)

- Billing is per hour the endpoint is up, on the machine type and GPU you chose, not per request
- A small GPU-backed endpoint (single T4 or L4, smallest Gemma 4 size) is the cheapest configuration to demo with, still not free
- Use the [Vertex AI pricing calculator](https://cloud.google.com/products/calculator) with your exact machine type and region before the session so you can quote a real number live
- This is the point of the demo: contrast this hourly, predictable cost against pay-per-token frontier API pricing at the same volume

---

## Troubleshooting

**"quota exceeded" for the accelerator:** you don't have GPU quota in that region yet. Request an increase under IAM & Admin → Quotas, this can take time to approve, so check well before the session, not the morning of.

**Deployment stuck in "creating" for a long time:** GPU-backed endpoints can take 10+ minutes to come up, this is normal but budget for it. If it's stuck well past that, check the operation status:
  ```bash
  gcloud ai operations list --project="${PROJECT_ID}" --region="${REGION}"
  ```

**`accept-eula` errors:** some Model Garden models require accepting a licence, the flag above handles it for this command, but check the console UI once if the CLI flag isn't picking it up.

**Endpoint deployed but predict call fails:** confirm you're using the right endpoint ID (not the model ID) in the URL, and that your access token hasn't expired (`gcloud auth print-access-token` regenerates it).

---

## Demo Safety Net for the Live Session

Deploy a second, backup endpoint the day before and leave it running (accepting the small extra cost) as a pre-baked fallback. If the live deploy hits a quota wall or takes too long in front of the group, switch to the backup immediately rather than debugging live. **Delete both endpoints as soon as the session wraps.**

---

## What "Good" Looks Like Before the Session

- [ ] `gcloud ai model-garden models list-deployment-config` returns a valid config for your chosen Gemma 4 size
- [ ] A full deploy → predict → delete cycle completes without errors
- [ ] You've timed the deployment (know roughly how long "creating" takes)
- [ ] You've checked current pricing for your exact machine type and region
- [ ] A backup endpoint is deployed and tested the day before, ready as a fallback
- [ ] You have a calendar reminder to delete every endpoint immediately after the session

If all six are ticked, you're ready for this segment of the live demo, and your bill won't surprise you.
