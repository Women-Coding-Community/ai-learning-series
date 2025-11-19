# SCVerge: Basic Chatbot for WCC info

This is a basic chatbot built with Gemini API that answers frequently asked questions about the Women Coding Community. This bot aims to help new members learn about WCC events, membership, volunteering, and more.


## Quick Start

### 1. Setup

```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash

# Install dependencies
pip install -r requirements.txt
pip install beautifulsoup4 requests
```

### 2. Configure

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Then edit `.env` and add your Gemini API key:

```bash
GEMINI_API_KEY=your-gemini-api-key-here
```

Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 3. Run

```bash
python chatbot.py
```

## What's Included

- `chatbot.py`: Basic chatbot implementation with conversation memory
- `requirements.txt`: Python dependencies
- `.env.example`: Environment variable template

## Features

✅ Conversation memory (maintains context)  
✅ Error handling  
✅ System prompts for personality  
✅ Simple CLI interface  



## Troubleshooting

**"Permission denied" error**

- Check `GOOGLE_APPLICATION_CREDENTIALS` is set correctly
- Verify service account has "Vertex AI User" role

**"Module not found" error**

- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**"Project not found" error**

- Check `GCP_PROJECT_ID` in `.env` file
- Verify project ID is correct
