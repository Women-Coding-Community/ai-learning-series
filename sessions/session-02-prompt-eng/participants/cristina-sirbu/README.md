# Career Quick Coach

AI-powered career counselor that helps students explore career paths, understand job market trends and prepare for interviews.

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
python demo.py
```

**Note**: Example of run of the demo script can be found [here](./example.txt).

## What I learned

- There are techniques for prompts to make the responses more consistent.
- There are ways to handle PII
- How to test responses for PII

## Challenges

- Python. Still new to it.
- Did not really understand on the first try the flow of the demo.py script. I had to take it step by step through code to understand what it does. So I guess it was a good learning experience in the end.

## Future improvements

- Implement resume analysis
- Add mock interview practice with evaluation metrics
- Create a skills gap analyzer based on target roles
