# Multi-Agent System Starter Template

This template provides a foundation for building multi-agent systems using Google's ADK with the supervisor-worker pattern.

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
cp ../../../.env.example .env
```

Then edit `.env` and add your Gemini API key:

```bash
GEMINI_API_KEY=your-gemini-api-key-here
GOOGLE_API_KEY=your-gemini-api-key-here
```

Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 3. Run the Multi-Agent System

From the path `session-05-multi-agents/starter-template`:

```bash
adk web
```

Once the server is up, access it at http://127.0.0.1:8000

Try these prompts:
- "I need help with a task"
- "Can you analyze this problem?"
- "Let's work on something together"

## 🛠️ How to Use This Template

### Project Structure

```text
starter-template/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
└── multi_agent_starter/
    ├── __init__.py
    ├── agent.py                 # Main supervisor agent
    └── agents/
        ├── __init__.py
        └── specialist.py        # Example specialist agent
```

### Understanding the Code

1. **`agent.py`**: The supervisor agent that routes requests to specialists
2. **`agents/specialist.py`**: Template for creating specialist agents
3. Add more specialists by creating new files in the `agents/` folder

## 🚀 How to Enhance

### Step 1: Add a New Specialist Agent

Create a new file in `agents/` (e.g., `researcher.py`):

```python
from google.adk.agents import Agent

researcher_agent = Agent(
    name="researcher",
    model="gemini-2.0-flash",
    instruction="""You are a Research Specialist.
    Your role is to:
    - Find information on topics
    - Summarize research findings
    - Provide sources and references
    """,
    tools=[your_research_tools],
)
```

### Step 2: Register with Supervisor

Update `agent.py` to include your new agent:

```python
from .agents.researcher import researcher_agent

root_agent = Agent(
    name="supervisor",
    # ... existing config ...
    sub_agents=[
        specialist_agent,
        researcher_agent,  # Add your new agent
    ],
)
```

### Step 3: Add Custom Tools

Create tools that your agents can use:

```python
def search_database(query: str) -> str:
    """Search for information in the database."""
    # Your implementation here
    return f"Results for: {query}"
```

## 📚 Multi-Agent Patterns

### Pattern 1: Supervisor-Worker (Default)

```
User → Supervisor → Specialist A
                 → Specialist B
                 → Specialist C
```

### Pattern 2: Pipeline

```
User → Agent A → Agent B → Agent C → Output
```

### Pattern 3: Collaborative

```
User → All Agents work together → Combined Output
```

## 🎓 Next Steps

1. **Start Simple**: Begin with 2 agents (supervisor + 1 specialist)
2. **Add Specialists**: Create agents for specific tasks
3. **Implement Handoffs**: Let agents transfer work to each other
4. **Add Shared State**: Create tools that all agents can access
5. **Test Workflows**: Try complex multi-step scenarios
6. **Document**: Create a workflow diagram of your system

## 📝 Homework Requirements

- [ ] At least 3 specialized agents
- [ ] Agent handoffs implemented
- [ ] Shared memory/state between agents
- [ ] Workflow diagram included
- [ ] README documenting agent responsibilities
- [ ] Complex scenario demonstrated

---

Happy Building! 🤖🤖🤖
