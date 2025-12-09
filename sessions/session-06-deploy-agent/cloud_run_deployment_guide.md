# Deployment Guide: Mentorship Agent to Google Cloud Run

This guide assumes you have the working `mentorship_agent/api.py`, `mentorship_agent/Dockerfile`, and the necessary Python files (`agent.py`, `newsletter_tools.py`, etc.) in your local repository.

---

## Prerequisites

* **Google Cloud Project:** An active project with Billing enabled.
* **gcloud CLI:** Google Cloud SDK installed and initialized (`gcloud init`).
* **Docker:** Docker Desktop installed and running.
* **API Key:** Your Gemini API Key ready to be injected as an environment variable.

---

## Step 1: Set Up and Authenticate Docker

You need to authorize Docker to push images to your Google Cloud Artifact Registry.

### 1. Set Environment Variables

```bash
PROJECT_ID="YOUR_GCP_PROJECT_ID"
REGION="us-central1" # Or your preferred region
```

### 2. Configure Docker

Authenticate Docker to push to the Artifact Registry:

```bash
gcloud auth configure-docker ${REGION}-docker.pkg.dev
```

---

## Step 2: Build and Push the Docker Image

You will build the container using the Dockerfile located inside the `mentorship_agent` directory and push it to Google Artifact Registry.

### Navigate to the Agent Directory

```bash
cd mentorship_agent
```

### Build the Image

```bash
IMAGE_NAME="${REGION}-docker.pkg.dev/${PROJECT_ID}/cloud-run-source/mentorship-backend"
docker build -t ${IMAGE_NAME} .
```

### Push the Image

```bash
docker push ${IMAGE_NAME}
```

> Uploading may take a few minutes.

---

## Step 3: Deploy to Google Cloud Run

You will now deploy the image to Cloud Run.
**Important:** Set `GOOGLE_API_KEY` as an environment variable and limit the service to **1 instance** (required for `InMemoryRunner` context persistence).

### Deploy the Service

```bash
SERVICE_NAME="mentorship-backend"

gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --region ${REGION} \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE" \
    --port 8080 \
    --min-instances 0 \
    --max-instances 1
```

#### Notes

* **`--allow-unauthenticated`** → Allows your frontend or tools like curl to access the API.
* **`--set-env-vars GOOGLE_API_KEY="..."`** → Injects the Gemini key used in `genai.configure()`.
* **`--max-instances 1`** → **Critical** to preserve conversation history (otherwise Cloud Run may spin up a new container and lose context).

### Retrieve the Service URL

After deployment, Cloud Run will output the service URL. To retrieve it again:

```bash
gcloud run services describe ${SERVICE_NAME} \
    --region ${REGION} \
    --format 'value(status.url)'
```

---

## Step 4: Final Verification

Test your deployed Cloud Run API using curl.

### Set the Cloud URL

Replace with your actual Cloud Run service URL:

```bash
CLOUD_URL="YOUR_CLOUD_URL" # e.g., https://mentorship-backend-xxxx.a.run.app
```

### Test the `/chat` Endpoint

```bash
curl -X POST "${CLOUD_URL}/chat" \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{  
           "session_id": "cloud_test_1",
           "user_input": "Who are you?",
           "user_id": "cloud_user"
         }'
```

## Step 5: Deleting the Service ( MUST)

To stop charges, delete the service:

```
gcloud run services delete mentorship-backend \
    --region ${REGION} \
    --platform managed
```

You will be prompted for confirmation.

## Step 5: Revoke cli authorization ( If you no longer using gc services)

To stop cli authorization:

```
gcloud auth revoke
```


If you receive a **200 OK** response with a message from the agent, your backend API is successfully deployed and running on **Google Cloud Run**.

---
