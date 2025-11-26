# Session 4 Live Demo - WCC Mentorship Coordinator Agent

## Overview

This folder contains the live coding demo for Session 4. We'll build a mentorship coordinator AI agent.

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
GOOGLE_API_KEY=your-api-key-here
```

---

## Files in This Folder

- **`mentorship_agent/agent.py`** - Main demo file with single agent set-up
- **`mentorship_agent/requirements.txt`** - Python dependencies
- **`README.md`** - This file

---

## Quick Start

### How to Run Your Agent

1. Install the ADK: Open your terminal or command prompt and run:
From the path "ai-learning-series\sessions\session-04-ai-agent\live-demo"

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
adk web
```
- This will start a local server (usually at `http://127.0.0.1:8000`).
- You will see a chat interface where you can type: 
    - "I would like to join this mentorship program" or
    - "Can you find me a mentor with Java skills?"


---

## Demo Details

The demo is showcasing how an AI agent ( which will be WCC mentorship coordinator) can help with ask correct questions for registration of a mentor or mentee, how can validate a mentor or mentee's profile, and once the profile is validated how it store in a data source.


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

### Add more tools for the Agent

Edit the `mentorship_agent/tools/mentorship_tools.py` to add more custom tools for the agent:

1. The "Feedback Logger" Tool
- Goal: Track the health of the relationship of the mentor-mentee relationship. 
- Why: Allows the agent to "remember" if a pair is doing well or struggling.

```python
def log_session_feedback(mentee_name: str, mentor_name: str, rating: int, notes: str) -> str:
    """
    Logs feedback after a session to track relationship health.
    
    Args:
        mentee_name: Name of the mentee.
        mentor_name: Name of the mentor.
        rating: 1-5 score of the session.
        notes: Qualitative feedback (e.g. "Great advice," "Mentor was late").
    """
    feedback_entry = {
        "mentee": mentee_name,
        "mentor": mentor_name,
        "rating": rating,
        "notes": notes,
        "status": "At Risk" if rating < 3 else "Healthy"
    }
    
    # Append to a simple log file (or use your existing JSON structure)
    log_file = "mentorship_agent/session_logs.json"
    
    try:
        logs = []
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(feedback_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
            
        if rating < 3:
            return "Feedback logged. ⚠️ Low rating detected - flagging for human coordinator review."
        return "Feedback logged successfully. Glad to hear the session happened!"
        
    except Exception as e:
        return f"Error logging feedback: {str(e)}"
```

2. The "Resource Librarian" Tool

- Goal: Instant value add for Mentees. 
- Why: Instead of hallucinating links, this tool returns a curated list of high-quality resources.

```python
def recommend_learning_resources(topic: str) -> str:
    """
    Returns a curated list of learning resources for specific topics.
    
    Args:
        topic: The skill or topic (e.g., 'Python', 'Leadership', 'System Design').
    """
    library = {
        "python": "1. 'Fluent Python' (Book) - Advanced\n2. RealPython.com (Website) - Practical tutorials",
        "leadership": "1. 'The Making of a Manager' by Julie Zhuo\n2. HBR Podcast: IdeaCast",
        "system design": "1. 'Designing Data-Intensive Applications' (The Bible of SD)\n2. System Design Prime (GitHub Repo)",
        "career growth": "1. 'Staff Engineer: Leadership beyond the management track' by Will Larson"
    }
    
    topic_key = topic.lower()
    # Simple substring search
    matches = [content for key, content in library.items() if key in topic_key or topic_key in key]
    
    if matches:
        return f"Here are some top resources for {topic}:\n" + "\n---\n".join(matches)
    
    return f"I don't have a curated list for '{topic}' yet. Try 'Python', 'Leadership', or 'System Design'."
```

---

## Learning Outcomes

- Here are some high-level concepts you will learn from this demo:

1. **ReAct Pattern**: How agents use a "Reason-Act" loop to dynamically decide which action to take next rather than just predicting the next word like a chatbot.

2. **Tool Usage**: How to give an LLM "hands" by connecting it to custom Python functions (like saving to a JSON file) to perform real-world tasks.

3. **State Management**: The code demonstrated how to maintain both short-term conversational context (via the Runner) and long-term persistent memory (via the database file).

4. **ADK Architecture**: How Google ADK provides comprehensive framework to simplify building AI agents.

---

## Next Steps

1. **Enhance the agent** - Add more tools for this agent
2. **Deploy it** - Share with the community
3. **Customize it** - Make it your own
4. **Use other platforms** - Try AWS, Azure, or OpenAI
5. **Build your use case** - Choose from list from use-case-guides

---

## Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/get-started/)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Gemini API Key Setup](../../getting-started/gemini-api-key-setup.md)

---

## Questions?

Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel

---

**Let's build amazing AI Agents together! 🚀**
