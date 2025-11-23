# Career Coach Chatbot

AI-powered career coaching chatbot that provides quick career advice, resume tips, interview preparation, and career guidance between mentorship sessions.

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

### 3. Run in Terminal

```bash
python career_coach.py
```

### 4. Run in UI

```bash
streamlit run career_coach_web.py
```

**Note**: Example of conversion history can be found [here](./career_coach_streamlit_user.json).
