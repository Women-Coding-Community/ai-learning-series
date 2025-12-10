# Deployment Guide: Mentorship Agent to Google Cloud Run

This guide assumes you have the working `mentorship_agent/api.py`, `mentorship_agent/Dockerfile`, and the necessary Python files (`agent.py`, `newsletter_tools.py`, etc.) in your local repository.

---

## Prerequisites

* **Google Cloud Project:** An active Google Cloud Project with Billing enabled.
* **gcloud CLI:** Google Cloud SDK installed and initialized (`gcloud init`).
* **Docker:** Docker Desktop installed and running.
* **API Key:** Your Gemini API Key to be injected as an environment variable.

---

## Step 1: Set Up and Authenticate Docker

You must authorize Docker to push images to your Google Cloud Artifact Registry.

### Set Environment Variables

(Use PowerShell syntax if on Windows.)

> **NOTE: Replace the values below**

```bash
PROJECT_ID="YOUR_GCP_PROJECT_ID"
REGION="us-central1"  # Or your preferred region
```

**Windows PowerShell equivalent:**

```powershell
$PROJECT_ID="YOUR_GCP_PROJECT_ID"
$REGION="us-central1"
```

### Create Artifact Registry Repository (MANDATORY)

```bash
REPO_NAME="cloud-run-source"

gcloud artifacts repositories create ${REPO_NAME} \
    --repository-format=docker \
    --location=${REGION} \
    --description="Docker repository for Cloud Run source images"
```

### Configure Docker Credentials

```bash
gcloud auth configure-docker ${REGION}-docker.pkg.dev
```

---

## Step 2: Build and Push the Docker Image

You will build the container image using the Dockerfile inside the `mentorship_agent` directory.

### Navigate to the Agent Directory

```bash
cd mentorship_agent
```

### Build the Image (CRITICAL: Use the variable)

```bash
IMAGE_NAME="${REGION}-docker.pkg.dev/${PROJECT_ID}/cloud-run-source/mentorship-backend"

docker build -t ${IMAGE_NAME} .
```

### Windows CMD Alternative

```cmd
set IMAGE_NAME="us-central1-docker.pkg.dev/YOUR_GCP_PROJECT_ID/cloud-run-source/mentorship-backend"
docker build -t %IMAGE_NAME% .
```

or use the full string:

```cmd
docker build -t us-central1-docker.pkg.dev/YOUR_GCP_PROJECT_ID/cloud-run-source/mentorship-backend .
```

### Push the Image

```bash
docker push ${IMAGE_NAME}
```

#### ⚠️ Troubleshooting: 403 Forbidden (Permission Denied)

If `docker push` fails:

1. Run `gcloud auth list`
2. Go to **IAM & Admin → IAM**
3. Assign the role: **Artifact Registry Writer**
4. Retry the push.

---

## Step 3: Deploy to Google Cloud Run

You must inject `GOOGLE_API_KEY` and restrict Cloud Run to **1 instance** to preserve session history.

### ⚠️ Troubleshooting: PERMISSION_DENIED on Deploy

If deployment fails:

1. Run `gcloud auth list`
2. In **IAM**, give your user: **Cloud Run Admin (roles/run.admin)**
3. Retry the deploy.

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

#### Flags Explained

* **`--allow-unauthenticated`**: Lets your frontend or curl access the API
* **`--set-env-vars`**: Passes `GOOGLE_API_KEY` to `api.py`
* **`--max-instances 1`**: Enforces a single container for InMemoryRunner context

### Retrieve the Service URL

```bash
gcloud run services describe ${SERVICE_NAME} \
    --region ${REGION} \
    --format 'value(status.url)'
```

---

## Step 4: Final Verification

Test your deployed Cloud Run service.

### Set Cloud URL

```bash
CLOUD_URL="YOUR_CLOUD_URL"
# Example:
# https://mentorship-backend-xxxx.a.run.app
```

### Test `/chat` Endpoint

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

If you receive **200 OK**, your backend is successfully deployed.

---

## Step 5: Deleting the Service (Optional)

To stop charges, delete the service:

```bash
gcloud run services delete mentorship-backend \
    --region ${REGION} \
    --platform managed
```

You will be prompted for confirmation.

---

## Miscellaneous Useful Commands

```bash
gcloud iam service-accounts get-iam-policy goelsonali@gmail.com
gcloud auth configure-docker us-central1-docker.pkg.dev
gcloud artifacts repositories list --location=us-central1

gcloud artifacts repositories create cloud-run-source \
    --repository-format=docker \
    --location=us-central1 \
    --description="Docker repository for Cloud Run source images"
```

---
