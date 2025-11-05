# Vertex AI Quickstart

## Overview

Vertex AI is Google Cloud's unified ML platform. In this quickstart, you'll make your first API call to Gemini using Vertex AI.

## Prerequisites

- Completed [GCP Setup Guide](./gcp-setup.md)
- Python 3.11+ installed
- `GOOGLE_APPLICATION_CREDENTIALS` environment variable set

## Installation

Install the required Python packages:

```bash
pip install google-cloud-aiplatform
```

## Your First API Call

Create a file named `quickstart.py`:

```python
from google.cloud import aiplatform

# Initialize Vertex AI
aiplatform.init(project="YOUR_PROJECT_ID", location="us-central1")

# Import the generative model
from vertexai.generative_models import GenerativeModel

# Initialize the model
model = GenerativeModel("gemini-2.5-flash-lite")

# Make a simple request
response = model.generate_content("What is AI?")

print("Response:")
print(response.text)
```

Replace `YOUR_PROJECT_ID` with your actual GCP project ID.

Run the script:

```bash
python quickstart.py
```

You should see a response from Gemini!

## Understanding the Response

The response object contains:

- `text`: The generated text response
- `finish_reason`: Why the generation stopped (e.g., "STOP" for normal completion)
- `usage_metadata`: Token usage information

```python
response = model.generate_content("What is AI?")

print(f"Text: {response.text}")
print(f"Finish Reason: {response.finish_reason}")
print(f"Input tokens: {response.usage_metadata.prompt_token_count}")
print(f"Output tokens: {response.usage_metadata.candidates_token_count}")
```

## Streaming Responses

For longer responses, use streaming:

```python
response = model.generate_content(
    "Explain machine learning in detail",
    stream=True
)

for chunk in response:
    print(chunk.text, end="", flush=True)
```

## Error Handling

Always handle potential errors:

```python
from google.api_core import exceptions

try:
    response = model.generate_content("Your prompt here")
    print(response.text)
except exceptions.GoogleAPICallError as e:
    print(f"API Error: {e}")
except exceptions.NotFound:
    print("Model not found. Check your project ID and location.")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Common Issues

### "Permission denied" error

- Verify your service account has "Vertex AI User" role
- Check that `GOOGLE_APPLICATION_CREDENTIALS` is set correctly

### "Model not found" error

- Ensure you're using a valid model name (e.g., "gemini-2.5-flash-lite", "gemini-2.5-flash")
- Check that Vertex AI API is enabled

### Rate limiting

- Free tier has limits on requests per minute
- Implement exponential backoff for retries

## Available Models

- **gemini-2.5-flash-lite**: Fast, efficient model (recommended for most use cases)
- **gemini-2.5-flash**: Balanced performance and quality
- **gemini-2.5-pro**: Most capable, better for complex tasks

## Next Steps

- [Build a Chatbot with Memory](../sessions/session-01-ai-chatbots/starter-template/)
- [Prompt Engineering Guide](../resources/prompt-engineering-guide.md)
- [Security Checklist](../resources/security-checklist.md)

---

**Documentation:**

- [Vertex AI Python SDK](https://cloud.google.com/python/docs/reference/aiplatform/latest)
- [Gemini API Reference](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
