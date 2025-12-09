# Session 6 Live Demo - WCC Mentorship Coordinator Agent

## Overview

This folder contains the live coding demo for Session 6. We'll deploy existing built  mentorship coordinator AI agent. Expose the agent through a chat endpoint and then deploy using google cloud Run.

---

## Prerequisites

Before running the demo, make sure you have:

1. ✅ Python 3.11+ installed
2. ✅ Gemini API key ([Get one here](../../getting-started/gemini-api-key-setup.md))
3. ✅ `.env` file with your API key, PROJECT_ID, REGION

### Quick Setup

```bash
# Create .env from template
cp ../../../.env.example .env

# Edit .env and add your Gemini API key
GEMINI_API_KEY=your-api-key-here
GOOGLE_API_KEY=your-api-key-here
PROJECT_ID=your-gcp-project-id 
REGION=us-central1 # Use your desired region (e.g., us-central1)
```

---

## Files in This Folder

- **`mentorship_agent/api.py`** - Main demo file with single agent exposed via FASTAPI /chat endpoint.
- **`mentorship_agent/agent.py`** - ADK agent built previously.
- **`mentorship_agent/requirements.txt`** - Python dependencies
- **`Dockerfile`** - To create an image of your agent app.
- **`README.md`** - This file

---

## Quick Start

### How to Run Your Agent APP locally

1. Install the ADK: Open your terminal or command prompt and run:
From the path "ai-learning-series\sessions\session-06-deploy-agent\live-demo"

```bash
pip install -r mentorship_agent/requirements.txt
```

2. Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your-gemini-api-key-here
```
Get your API key: [Gemini API Key Setup Guide](../../getting-started/gemini-api-key-setup.md)

3. **Launch the Web Interface:**
- Navigate to the folder containing your mentorship_agent folder (/live-demo) and run:

```bash
python api.py
```
- This will start a local server (usually at `http://localhost:8080/docs`).
- You will see a swagger doc interface where you can type: 
    - try the `/chat` endpoint with some values and it should respond from your ADK agent.

4. **Follow instruction to deploy**
- Install google cloud cli refer this [guide](../google_cloud_cli_installation.md)

- Now, follow the [cloud run deploy guide](../cloud_run_deployment_guide.md) to deploy the agent as app.

5. **DELETE THE APP/SERVICE**
- Once tested do delete the deployed app/service ( instructions in the [cloud run deploy guide](../cloud_run_deployment_guide.md))

---

## Troubleshooting

### Error: "GEMINI_API_KEY not found"

**Solution:**

1. Create `.env` file in project root
2. Add: `GEMINI_API_KEY=your-key-here`
3. Make sure `.env` is in the same folder as `wcc_demo.py`

### Error: "ModuleNotFoundError: No module named 'google'"

**Solution:**

```bash
pip install google-generativeai
```

### Error: "API key not valid"

**Solution:**

1. Get a new API key: [Gemini API Key Setup](../../getting-started/gemini-api-key-setup.md)
2. Update your `.env` file
3. Try again

---

## Customization Ideas

### Add evaluation tests for the Agent

- Read through the agent evaluation techniques [here](../starter-template/evaluation-technique.md)

### Create a Frontend for your agent and deploy

---

## Learning Outcomes

Here are some high-level concepts you will learn from this demo:

1. How ADK agent can be exposed as an endpoint.
2. Google CLoud ecosystem - Google cloud CLI, Service etc.
3. How to deploy your backend agent app via google cloud Run.

---


## Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/get-started/)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Gemini API Key Setup](../../getting-started/gemini-api-key-setup.md)
- "Evaluating LLMs is a minefield" - Hamel Husain
- "The LLM Evaluation Pyramid" - Eugene Yan
- "Production LLMs: A Guide" - Chip Huyen


---

## Questions?

Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel

---

**Let's build and deploy amazing AI Agents together! 🚀**
