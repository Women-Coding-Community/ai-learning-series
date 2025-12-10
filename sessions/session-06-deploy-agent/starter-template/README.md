# AI Agent Starter Guide: Mentorship Backend

This template provides the full backend foundation for your Mentorship Agent, including function calling and persistence, ready for deployment on Google Cloud Run.

## Quick Start: From Code to Cloud

Follow these steps to get your Mentorship Agent running on the cloud and ready to handle user conversations.

### 1. Setup Your Local Environment

Before touching the cloud, get your local Python environment ready.

#### Create a virtual environment
```bash
python -m venv venv
source venv/Scripts/activate  
```

#### Install all necessary Python dependencies

```pip install -r requirements.txt ```


### 2. Configure Environment Variables

You need to provide your API Key and your Google Cloud details.

Create the configuration file:

```cp .env.example .env```

Edit the .env file and add your required values:

#### Get your key from Google AI Studio: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
GOOGLE_API_KEY=your-gemini-api-key-here 

### Deployment Variables (Needed for the cloud guide)
PROJECT_ID=your-gcp-project-id 
REGION=us-central1 # Use your desired region (e.g., us-central1)

### 3. Install Google Cloud CLI

You need the gcloud command-line tool to build, push, and deploy your container.

➡️ Follow the instructions in: [google_cloud_cli_installation](../google_cloud_cli_installation.md)

### 4. Deploy to Google Cloud Run

This is the main deployment process. We will containerize your agent using Docker and deploy it as a highly scalable web service.

➡️ Follow the steps in: [cloud_run_deployment_guide.md](../cloud_run_deployment_guide.md)

(This guide includes building the Docker image, setting up Artifact Registry, handling permissions, and running the final gcloud run deploy command.)


## 🛠️ What's Included & How to Enhance

### What's Included

mentorship_agent/agent.py: Defines the agent's persona and instruction (the "career coach").

mentorship_agent/newsletter_tools.py: Contains the NewsletterTool function that the agent can choose to call (function calling).

mentorship_agent/api.py: The FastAPI application that exposes the /chat endpoint and manages the InMemoryRunner for session persistence.

mentorship_agent/Dockerfile: The instructions for packaging the application into a container.

### How to Enhance

- Improve Persona
    mentorship_agent/agent.py

- Refine the instruction string to make the coordinator more specific, specialized, or encouraging.

- Change State Manager
    - mentorship_agent/api.py - 
        Change InMemoryRunner to a persistent solution like FirestoreRunner or a custom database solution to preserve history even if the Cloud Run instance restarts.


### Incorporate Evaluation

Implement structured testing for quality, consistency, and safety. Refer to the guide below.

#### 🔬 Optional: Agent Evaluation Techniques

To ensure the quality and safety of your mentorship agent, it is highly recommended to incorporate dedicated testing.

➡️ Refer to the techniques outlined in: 
[evaluation-technique](evaluation-technique.md)


This file details how to use Golden Paths (Regression Testing) and Qualitative Rubrics (Human-in-the-Loop) to validate that your agent maintains its persona, correctly uses its tools, and provides helpful, safe advice.

🎓 Next Steps

- Full-Stack: Deploy your frontend (Streamlit, React, etc.) and point it to the deployed Cloud Run URL.

- Evaluate: Use the techniques outlined in evaluation-technique.md to ensure your agent is helpful and safe.

Happy Building! 🤖