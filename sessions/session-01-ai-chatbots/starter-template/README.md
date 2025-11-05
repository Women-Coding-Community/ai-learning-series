# Starter Template: Basic Chatbot

This is a starter template for building a chatbot with Gemini API. Use this as a foundation for your Session 1 project.

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

## How to Enhance

### Add Personality

Modify the system prompt in `main()`:

```python
system_prompt = "You are a friendly pirate who loves AI!"
bot = SimpleBot(system_prompt=system_prompt)
```

### Add Web Interface

Use Streamlit:

```bash
pip install streamlit
```

Create `app.py`:

```python
import streamlit as st
from chatbot import SimpleBot

st.title("My Chatbot")
bot = SimpleBot()

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("You:")
if user_input:
    response = bot.chat(user_input)
    st.write(f"Bot: {response}")
```

Run with:

```bash
streamlit run app.py
```

### Add Data Integration

Fetch real data and include it in the system prompt:

```python
# Example: WCC Info Bot
wcc_info = fetch_wcc_data()  # Your function
system_prompt = f"You are a WCC assistant. Here's our info: {wcc_info}"
bot = SimpleBot(system_prompt=system_prompt)
```

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

## Next Steps

1. Enhance the chatbot with your own features
2. Deploy to Streamlit Cloud or Google Cloud Run
3. Submit your work to the participants folder

## Resources

- [Session 1 Guide](../README.md)
- [Vertex AI Quickstart](../../../getting-started/vertex-ai-quickstart.md)
- [Prompt Engineering Guide](../../../resources/prompt-engineering-guide.md)

---

Happy coding! 🚀
