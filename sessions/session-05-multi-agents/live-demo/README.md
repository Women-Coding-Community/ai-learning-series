# Session 5 Live Demo - WCC Community Management Multi-Agent System

## Overview

This folder contains the live coding demo for Session 5. We'll build a multi-agent system for community management where specialized agents collaborate to handle different tasks.

---

## Prerequisites

Before running the demo, make sure you have:

1. ✅ Python 3.11+ installed
2. ✅ Gemini API key ([Get one here](../../getting-started/gemini-api-key-setup.md))
3. ✅ `.env` file with your API key
4. ✅ Completed Session 4 (understanding of single agents)

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

```text
live-demo/
├── README.md                           # This file
└── community_management_team/
    ├── __init__.py                     # Package init
    ├── agent.py                        # Main multi-agent orchestration
    ├── agents/                         # Individual agent definitions
    │   ├── __init__.py
    │   ├── content_creator.py          # Creates social media content
    │   ├── responder.py                # Answers community questions
    │   ├── moderator.py                # Flags inappropriate content
    │   └── scheduler.py                # Plans content calendar
    ├── tools/                          # Shared tools
    │   ├── __init__.py
    │   └── community_tools.py          # Tools used by agents
    └── requirements.txt                # Python dependencies
```

---

## Quick Start

### How to Run Your Multi-Agent System

1. Install dependencies:

From the path `ai-learning-series/sessions/session-05-multi-agents/live-demo`

```bash
pip install -r community_management_team/requirements.txt
```

2. Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your-gemini-api-key-here
```

Get your API key: [Gemini API Key Setup Guide](../../getting-started/gemini-api-key-setup.md)

3. **Launch the Web Interface:**

Navigate to the folder containing your `community_management_team` folder (`/live-demo`) and run:

```bash
adk web
```

This will start a local server (usually at `http://127.0.0.1:8000`).

4. **Try these prompts:**

- "Create a social media post about our upcoming Python workshop"
- "Someone asked about mentorship opportunities, can you help?"
- "Check if this message is appropriate: [paste message]"
- "When should we post about the next event?"

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Request                            │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    SUPERVISOR AGENT                          │
│         (Routes tasks to appropriate specialist)             │
└──────┬──────────┬──────────┬──────────┬────────────────────┘
       │          │          │          │
       ▼          ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Content  │ │Responder │ │Moderator │ │Scheduler │
│ Creator  │ │  Agent   │ │  Agent   │ │  Agent   │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
       │          │          │          │
       └──────────┴──────────┴──────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Shared Tools & State                      │
│     (Community data, content calendar, response templates)   │
└─────────────────────────────────────────────────────────────┘
```

---

## Demo Details

### Agent Responsibilities

| Agent | Responsibility | Tools Used |
|-------|---------------|------------|
| **Supervisor** | Routes incoming requests to the right specialist | Agent routing |
| **Content Creator** | Generates social media posts, event descriptions | `create_post`, `get_event_info` |
| **Responder** | Answers common community questions | `search_faq`, `get_resource_links` |
| **Moderator** | Reviews content for appropriateness | `check_content`, `flag_message` |
| **Scheduler** | Plans optimal posting times | `get_calendar`, `suggest_time` |

### Multi-Agent Patterns Demonstrated

1. **Supervisor-Worker Pattern**: The supervisor agent analyzes requests and delegates to specialists
2. **Handoffs**: Agents can transfer work to other agents when needed
3. **Shared State**: All agents access common community data and tools

---

## Troubleshooting

### Error: "GEMINI_API_KEY not found"

**Solution:**

1. Create `.env` file in project root
2. Add: `GOOGLE_API_KEY=your-key-here`
3. Make sure `.env` is accessible from the live-demo folder

### Error: "ModuleNotFoundError: No module named 'google'"

**Solution:**

```bash
pip install google-adk google-generativeai
```

### Error: "Agent not found"

**Solution:**

1. Make sure all `__init__.py` files exist
2. Check that agent names match in imports
3. Verify the folder structure matches the expected layout

---

## Customization Ideas

### Add a New Specialist Agent

1. Create a new file in `agents/` folder (e.g., `analytics_agent.py`)
2. Define the agent with specific instructions and tools
3. Register it with the supervisor in `agent.py`

Example: **Analytics Agent**

```python
from google.adk.agents import Agent

analytics_agent = Agent(
    name="analytics_agent",
    model="gemini-2.0-flash",
    instruction="""You are the WCC Analytics Agent.
    Your role is to:
    - Track engagement metrics
    - Identify trending topics
    - Suggest content improvements based on data
    """,
    tools=[get_engagement_stats, analyze_trends]
)
```

### Implement Agent-to-Agent Handoffs

```python
# In content_creator.py
def request_moderation_review(content: str) -> str:
    """
    Hands off content to the Moderator Agent for review.
    """
    # This triggers a handoff to the moderator agent
    return f"HANDOFF:moderator - Please review this content: {content}"
```

### Add Shared Memory

```python
# In tools/community_tools.py
from google.adk.sessions import InMemorySessionService

# Shared state across all agents
session_service = InMemorySessionService()

def save_to_shared_memory(key: str, value: str) -> str:
    """Save data that all agents can access."""
    session_service.set(key, value)
    return f"Saved {key} to shared memory"

def get_from_shared_memory(key: str) -> str:
    """Retrieve data from shared memory."""
    return session_service.get(key, "Not found")
```

---

## Learning Outcomes

1. **Multi-Agent Architecture**: How to design systems with multiple specialized agents

2. **Supervisor Pattern**: How a coordinator agent routes tasks to specialists

3. **Agent Handoffs**: How agents transfer work to each other

4. **Shared State**: How agents share information and maintain consistency

5. **ADK Multi-Agent Features**: Using Google ADK's built-in multi-agent capabilities

---

## Next Steps

1. **Add more agents** - Expand the team with new specialists
2. **Implement A2A** - Use Agent-to-Agent protocol for communication
3. **Add MCP** - Integrate Model Context Protocol for tool sharing
4. **Deploy it** - Share with the community
5. **Build your use case** - Choose from use-case-guides

---

## Resources

- [Google ADK Multi-Agent Documentation](https://google.github.io/adk-docs/agents/multi-agents/)
- [A2A Protocol](https://google.github.io/A2A/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)

---

## Questions?

Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel

---

**Let's build amazing Multi-Agent Systems together! 🚀🤖🤖🤖**
