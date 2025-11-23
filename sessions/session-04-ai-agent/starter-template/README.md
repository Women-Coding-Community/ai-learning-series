# AI Agent Starter Template
This template provides a foundation for building AI agents with function calling capabilities using Google's Gemini API.

## Quick Start

### 1. Setup

```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure

Create a `.env` file from the template:

```bash
cp ../../.env.example .env
```

Then edit `.env` and add your Gemini API key:

```bash
GEMINI_API_KEY=your-gemini-api-key-here
GOOGLE_API_KEY=your-gemini-api-key-here
```

Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 3. Run the Agent

- Go to the path "session-04-ai-agent\starter-template" run the bellow command
```bash
adk web
```
- Once the server is up and running access here - http://127.0.0.1:8000
- You will see a chat interface where you can type: 
    - "What's the weather like in london ?" or
    - "Can you perform this equation 2+4+5 ?"


## 🛠️ How to Use This Template
- Run this simple AI agent defined at simple-agent/agent.py
- Try to explore the functions/lib of the Google ADK 

## What's Included

- `simple-agent/agent.py`: Basic AI agent with custom tools and agent instruction
- `requirements.txt`: Python dependencies

## How to Enhance

### Add agent instruction

Modify the agent's instruction in `agent.py`:

```bash
instruction="""
    You are a friendly Weather Bot.
    - If the user asks for weather, ALWAYS use the `get_weather` tool.
    - If the tool returns data, summarize it cheerfully.
    - If the user asks anything else (like math), politely decline.
    - Also reply the country of the city requested.
    - Do not share any other information other than weather update.
    """
```

### Add more tools

Add more tools for the agents in `agent.py`:
- Update the current "weather tool" to call an actual weather API.
- Use "google-serach" as a tool for searching more information about the city.
- Add a tool to export the weather result.

## 🎓 Next Steps
- Start Simple: Begin with one tool (e.g., weather, time, best-time to visit)
- Test Thoroughly: Make sure your tool works before adding more
- Add Complexity: Read Google adk documentation for more tools ideas
- Polish: Add error handling, logging, and documentation
- Submit: Share your work with the community!

---

Happy Building! 🤖

