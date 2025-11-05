# Session 1 Live Demo - WCC Info Bot

## Overview

This folder contains the live coding demo for Session 1. We'll build a chatbot step-by-step, progressively adding features to demonstrate key concepts.

---

## Prerequisites

Before running the demo, make sure you have:

1. ✅ Python 3.11+ installed
2. ✅ Gemini API key ([Get one here](../../getting-started/gemini-api-key-setup.md))
3. ✅ `.env` file with your API key

### Quick Setup

```bash
# Create .env from template
cp ../../../.env.example .env

# Edit .env and add your Gemini API key
GEMINI_API_KEY=your-api-key-here
```

---

## Files in This Folder

- **`wcc_demo.py`** - Main demo file with 5 progressive sections
- **`requirements.txt`** - Python dependencies
- **`README.md`** - This file

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Your API Key

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your-gemini-api-key-here
```

Get your API key: [Gemini API Key Setup Guide](../../getting-started/gemini-api-key-setup.md)

### 3. Run the Demo

```bash
python wcc_demo.py
```

---

## Demo Structure

The demo is divided into 5 progressive sections. Start with Section 1 and uncomment sections as you follow along during the live session.

### Section 1: Basic API Call ✅ (ACTIVE BY DEFAULT)

**What you'll learn:**

- How to configure the Gemini API
- Making your first API call
- Getting a response from the AI

**Key code:**

```python
import google.generativeai as genai

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')
response = model.generate_content("What is Women Coding Community (WCC)?")
print(response.text)
```

**Output:**

```bash
AI Response: [AI's response about WCC]
🎉 SUCCESS! You just talked to AI! 🎉
```

---

### Section 2: Add Personality with System Prompts

**What you'll learn:**

- Using system prompts to give AI a personality
- How system prompts influence responses
- Creating domain-specific AI assistants

**To activate:**

1. Find the `'''` (triple quotes) on line ~49
2. Delete them to uncomment Section 1 code
3. Find the `'''` on line ~64
4. Delete them to uncomment Section 2

**Key code:**

```python
wcc_system_prompt = '''You are a helpful assistant for WCC...'''

model_with_personality = genai.GenerativeModel(
    'gemini-2.5-flash-lite',
    system_instruction=wcc_system_prompt
)

response = model_with_personality.generate_content("What is WCC?")
```

**What changes:**

- Responses become more WCC-focused
- AI shows personality and enthusiasm
- Answers align with community values

---

### Section 3: Add Conversation Memory

**What you'll learn:**

- Maintaining conversation history
- Context-aware responses
- Building multi-turn conversations

**To activate:**

1. Find the `"""` (triple quotes) on line ~114
2. Delete them to uncomment Section 3

**Key code:**

```python
class WCCChatBot:
    def __init__(self):
        self.conversation_history = []
    
    def chat(self, user_input):
        # Add to history
        self.conversation_history.append(f"User: {user_input}")
        
        # Generate response with context
        response = self.model.generate_content(full_prompt)
        
        # Add response to history
        self.conversation_history.append(f"Assistant: {response.text}")
        return response.text
```

**What you'll see:**

- Bot remembers previous messages
- Responses reference earlier context
- Natural multi-turn conversations

---

### Section 4: Explore Model Parameters

**What you'll learn:**

- Temperature (creativity vs consistency)
- Top-p (diversity of responses)
- Top-k (token selection)
- Max tokens (response length)

**To activate:**

1. Find the `"""` (triple quotes) on line ~167
2. Delete them to uncomment Section 4

**Key code:**

```python
generation_config = genai.types.GenerationConfig(
    temperature=0.7,      # 0=deterministic, 2=very creative
    max_output_tokens=100,
    top_p=0.9,           # nucleus sampling
    top_k=50             # top-k sampling
)

model = genai.GenerativeModel(
    'gemini-2.5-flash-lite',
    generation_config=generation_config
)
```

**Parameter Guide:**

| Parameter | Range | Effect |
|-----------|-------|--------|
| **Temperature** | 0.0 - 2.0 | Higher = more creative, lower = more consistent |
| **Top-p** | 0.0 - 1.0 | Lower = more focused, higher = more diverse |
| **Top-k** | 1+ | Limits to top-k tokens (lower = more focused) |
| **Max Tokens** | 1+ | Maximum response length |

---

### Section 5: Create Web Interface with Streamlit

**What you'll learn:**

- Building interactive web interfaces
- Streamlit components (chat, sliders, etc.)
- Session state management
- Real-time parameter adjustment

**To activate:**

1. Find the `'''` (triple quotes) on line ~246
2. Delete them to uncomment Section 5
3. Install Streamlit: `pip install streamlit`
4. Run: `streamlit run wcc_demo.py`

**Key features:**

- Interactive chat interface
- Adjustable model parameters with sliders
- Conversation history display
- Real-time settings adjustment
- Mobile-friendly design

**Streamlit code highlights:**

```python
import streamlit as st

st.title("🌟 WCC Info Bot")

# Sidebar controls
temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 500, 200)

# Chat interface
if prompt := st.chat_input("What would you like to know?"):
    st.chat_message("user").write(prompt)
    response = model.generate_content(prompt)
    st.chat_message("assistant").write(response.text)
```

---

## Running Each Section

### Option 1: Run Full Demo (All Sections)

```bash
python wcc_demo.py
```

This will run Section 1 and print instructions for activating other sections.

### Option 2: Uncomment Sections During Live Session

Follow the instructions in the file to uncomment sections one by one as the instructor demonstrates each concept.

### Option 3: Run Streamlit Web App

```bash
# Uncomment Section 5 first, then:
streamlit run wcc_demo.py
```

Your browser will open with an interactive web interface!

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

### Streamlit not starting

**Solution:**

```bash
pip install streamlit
streamlit run wcc_demo.py
```

---

## Customization Ideas

### Modify the System Prompt

Edit the `wcc_system_prompt` variable to change the bot's personality:

```python
wcc_system_prompt = '''You are a helpful assistant for WCC.
[Customize this section with your own knowledge base]
'''
```

### Add More Test Questions

Add questions to test different aspects:

```python
test_questions = [
    "What is WCC?",
    "How can I join?",
    "Your custom question here?"
]
```

### Change the Model

Try different models:

```python
MODEL_ID = 'gemini-2.5-pro'  # More powerful but slower
MODEL_ID = 'gemini-2.5-flash'  # Balanced performance
MODEL_ID = 'gemini-2.5-flash-lite'  # Fastest and cheapest (default)
```

### Extend the Web Interface

Add more Streamlit components:

```python
st.sidebar.markdown("---")
st.sidebar.write("📊 Statistics")
st.sidebar.metric("Messages", len(st.session_state.messages))
```

---

## Learning Outcomes

After completing this demo, you'll understand:

✅ How to authenticate with Gemini API  
✅ Making API calls and handling responses  
✅ Using system prompts for AI personality  
✅ Managing conversation history  
✅ Tuning model parameters  
✅ Building web interfaces with Streamlit  
✅ Best practices for chatbot development  

---

## Next Steps

1. **Enhance the bot** - Add more WCC knowledge
2. **Deploy it** - Share with the community
3. **Customize it** - Make it your own
4. **Use other platforms** - Try AWS, Azure, or OpenAI
5. **Build your use case** - Choose from Career Coach or Code Buddy

---

## Resources

- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Gemini API Key Setup](../../getting-started/gemini-api-key-setup.md)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Python SDK Reference](https://ai.google.dev/tutorials/python_quickstart)
- [Prompt Engineering Guide](../../resources/prompt-engineering-guide.md)

---

## Questions?

Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel or check the [Troubleshooting Guide](../../resources/troubleshooting.md)!

---

**Let's build amazing AI projects together! 🚀**
