# GCP & Vertex AI Setup Guide

> ⚠️ **Note:** This guide is for advanced users or production deployments.
>
> **For Session 1, use the [Gemini API Key Setup](./gemini-api-key-setup.md) instead** - it's simpler and faster!
>
> This guide is useful if you want to use Vertex AI or deploy to production with GCP.

## Overview

This guide walks you through setting up Google Cloud Platform (GCP) and Vertex AI for using Gemini models in a production environment.

## Prerequisites

- Google account (create one at [google.com](https://google.com) if needed)
- Credit card for verification (won't be charged for free tier)
- Basic familiarity with cloud consoles

## Step 1: Create a GCP Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top
3. Click **NEW PROJECT**
4. Enter project name: `wcc-ai-learning` (or your preferred name)
5. Click **CREATE**
6. Wait for the project to be created (this may take a minute)

## Step 2: Enable Vertex AI API

1. In the Cloud Console, go to **APIs & Services** > **Library**
2. Search for **Vertex AI API**
3. Click on it and press **ENABLE**
4. Wait for the API to be enabled

## Step 3: Create a Service Account

1. Go to **APIs & Services** > **Credentials**
2. Click **+ CREATE CREDENTIALS** > **Service Account**
3. Fill in the details:
   - **Service account name:** `wcc-ai-learning-sa`
   - **Service account ID:** (auto-filled)
   - Click **CREATE AND CONTINUE**
4. Grant the following roles:
   - **Vertex AI User**
   - **Vertex AI Service Agent**
   - Click **CONTINUE**
5. Click **DONE**

## Step 4: Create and Download API Key

1. In **Credentials**, find your service account and click on it
2. Go to the **KEYS** tab
3. Click **ADD KEY** > **Create new key**
4. Choose **JSON** format
5. Click **CREATE**
6. The JSON file will download automatically
7. **Save this file securely** - you'll need it for authentication

## Step 5: Set Up Application Default Credentials

### Option A: Using Environment Variable (Recommended for Development)

1. Save your JSON key file to a secure location (e.g., `~/.config/gcp/key.json`)
2. Set the environment variable:

**Windows (PowerShell):**

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\your\key.json"
```

**Windows (Git Bash):**

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/c/path/to/your/key.json"
```

**macOS/Linux:**

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcp/key.json"
```

### Option B: Using gcloud CLI

1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Run:

```bash
gcloud auth application-default login
```

## Step 6: Verify Your Setup

Run this Python script to verify everything is working:

```python
from google.cloud import aiplatform

# Initialize Vertex AI
aiplatform.init(project="YOUR_PROJECT_ID", location="us-central1")

# Test connection
print("✅ GCP setup successful!")
```

Replace `YOUR_PROJECT_ID` with your actual project ID (found in the Cloud Console).

## Troubleshooting

### "Permission denied" error

- Ensure your service account has the correct roles
- Verify the JSON key file path is correct
- Check that `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set

### "API not enabled" error

- Go to **APIs & Services** > **Library**
- Search for **Vertex AI API** and enable it
- Wait a few minutes for the API to activate

### "Project not found" error

- Verify your project ID is correct
- Check that you're using the right GCP project

## Free Tier Benefits

- **$300 credit** for new users (valid for 90 days)
- **Always free tier** for certain services after credits expire
- Vertex AI: 10 predictions per month free
- Cloud Storage: 5GB free storage

## Next Steps

- [Vertex AI Quickstart](./vertex-ai-quickstart.md)
- [Python Environment Setup](./python-environment.md)
- Start with [Session 1: AI Chatbots](../sessions/session-01-ai-chatbots/)

---

**Need Help?**

- [GCP Documentation](https://cloud.google.com/docs)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel!
