# Community Management Multi-Agent System - Use Case Guide

## Overview

Build a team of AI agents that work together to manage community tasks across Slack, social media, and content platforms for the Women Coding Community.

## Problem Statement

**Challenge**: Managing a growing community requires many different tasks:
- Creating engaging social media content
- Responding to member questions quickly
- Moderating content for appropriateness
- Planning and scheduling posts effectively

**Why it matters**: A well-managed community keeps members engaged, informed, and feeling supported. Manual management doesn't scale.

## What You'll Build

A multi-agent system with specialized agents that:
- **Content Creator**: Generates social media posts and event descriptions
- **Responder**: Answers common community questions
- **Moderator**: Reviews content for guideline compliance
- **Scheduler**: Plans optimal posting times
- **Supervisor**: Routes tasks to the right specialist

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Request                            │
│  "Create a post about our workshop and schedule it"          │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    SUPERVISOR AGENT                          │
│         Analyzes request → Routes to specialists             │
└──────┬──────────┬──────────┬──────────┬────────────────────┘
       │          │          │          │
       ▼          ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Content  │ │Responder │ │Moderator │ │Scheduler │
│ Creator  │ │  Agent   │ │  Agent   │ │  Agent   │
│          │ │          │ │          │ │          │
│ Creates  │ │ Answers  │ │ Reviews  │ │ Plans    │
│ posts    │ │ FAQs     │ │ content  │ │ timing   │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
```

## Implementation Guide

### Step 1: Define Your Agent Team

Create a folder structure:

```text
community_management/
├── __init__.py
├── agent.py                 # Supervisor
├── agents/
│   ├── __init__.py
│   ├── content_creator.py
│   ├── responder.py
│   ├── moderator.py
│   └── scheduler.py
├── tools/
│   ├── __init__.py
│   └── community_tools.py
└── requirements.txt
```

### Step 2: Create Shared Tools

```python
# tools/community_tools.py

import json
from datetime import datetime

# Community data storage
COMMUNITY_DATA = {
    "events": [],
    "faqs": {},
    "content_calendar": [],
    "guidelines": []
}

def get_upcoming_events() -> str:
    """Get list of upcoming community events."""
    events = [
        {"name": "Python Workshop", "date": "Dec 10", "time": "6 PM GMT"},
        {"name": "Career Panel", "date": "Dec 15", "time": "7 PM GMT"},
    ]
    return json.dumps(events, indent=2)

def search_faq(query: str) -> str:
    """Search FAQ database for answers."""
    faqs = {
        "join": "Visit our website and sign up for Slack!",
        "mentorship": "Check #mentorship channel for program details.",
        "events": "See #events channel for upcoming sessions.",
    }
    for key, answer in faqs.items():
        if key in query.lower():
            return answer
    return "Please ask in our Slack community for help!"

def check_content(content: str) -> str:
    """Check content against community guidelines."""
    issues = []
    if len(content) < 10:
        issues.append("Content too short")
    if len(content) > 280:
        issues.append("Consider shortening for Twitter")
    
    if issues:
        return f"Issues found: {', '.join(issues)}"
    return "✅ Content approved!"

def get_best_posting_time(platform: str) -> str:
    """Get optimal posting time for a platform."""
    times = {
        "twitter": "Weekdays 10 AM - 12 PM",
        "linkedin": "Tuesday-Thursday 10 AM",
        "slack": "Weekdays 10 AM - 2 PM",
    }
    return times.get(platform.lower(), "Weekdays 10 AM - 2 PM")

def save_draft(title: str, content: str) -> str:
    """Save content draft for later."""
    return f"Draft saved: {title}"
```

### Step 3: Create Specialist Agents

**Content Creator Agent:**

```python
# agents/content_creator.py

from google.adk.agents import Agent
from ..tools.community_tools import get_upcoming_events, save_draft

content_creator_agent = Agent(
    name="content_creator",
    model="gemini-2.0-flash",
    instruction="""You are the Content Creator for Women Coding Community.

YOUR ROLE:
- Create engaging social media posts
- Write event announcements
- Generate promotional content

STYLE GUIDELINES:
- Friendly and encouraging tone
- Use emojis appropriately
- Include relevant hashtags (#WomenInTech #WCC)
- Keep posts concise but impactful

When creating content:
1. Gather event/topic information
2. Draft engaging copy
3. Save draft for review
""",
    tools=[get_upcoming_events, save_draft],
)
```

**Responder Agent:**

```python
# agents/responder.py

from google.adk.agents import Agent
from ..tools.community_tools import search_faq, get_upcoming_events

responder_agent = Agent(
    name="responder",
    model="gemini-2.0-flash",
    instruction="""You are the Community Responder for WCC.

YOUR ROLE:
- Answer common questions about WCC
- Help new members get started
- Provide information about programs and events

GUIDELINES:
- Search FAQ first for standard answers
- Be welcoming to new members
- Direct to Slack channels when appropriate
""",
    tools=[search_faq, get_upcoming_events],
)
```

**Moderator Agent:**

```python
# agents/moderator.py

from google.adk.agents import Agent
from ..tools.community_tools import check_content

moderator_agent = Agent(
    name="moderator",
    model="gemini-2.0-flash",
    instruction="""You are the Content Moderator for WCC.

YOUR ROLE:
- Review content before posting
- Check guideline compliance
- Flag inappropriate content

GUIDELINES:
- Be fair and consistent
- Provide constructive feedback
- Approve content that meets standards
""",
    tools=[check_content],
)
```

**Scheduler Agent:**

```python
# agents/scheduler.py

from google.adk.agents import Agent
from ..tools.community_tools import get_best_posting_time

scheduler_agent = Agent(
    name="scheduler",
    model="gemini-2.0-flash",
    instruction="""You are the Content Scheduler for WCC.

YOUR ROLE:
- Suggest optimal posting times
- Plan content calendars
- Coordinate posting schedules

Consider:
- Global audience (multiple time zones)
- Platform-specific best practices
- Event timing (announce 1 week before)
""",
    tools=[get_best_posting_time],
)
```

### Step 4: Create Supervisor Agent

```python
# agent.py

from google.adk.agents import Agent
from .agents import (
    content_creator_agent,
    responder_agent,
    moderator_agent,
    scheduler_agent,
)

root_agent = Agent(
    name="community_supervisor",
    model="gemini-2.0-flash",
    instruction="""You coordinate the WCC Community Management team.

YOUR TEAM:
- @content_creator: Creates posts and content
- @responder: Answers community questions
- @moderator: Reviews content for guidelines
- @scheduler: Plans posting times

ROUTING:
- Content creation → content_creator
- Questions about WCC → responder
- Content review → moderator
- Posting times → scheduler

For multi-step requests, coordinate agents in sequence.
""",
    sub_agents=[
        content_creator_agent,
        responder_agent,
        moderator_agent,
        scheduler_agent,
    ],
)
```

## Example Workflows

### Workflow 1: Create and Schedule a Post

**User**: "Create a post about our Python workshop and tell me when to post it"

**Flow**:
1. Supervisor routes to Content Creator
2. Content Creator generates post
3. Supervisor routes to Scheduler
4. Scheduler recommends posting time
5. Supervisor compiles response

### Workflow 2: Answer a Question

**User**: "How do I join the mentorship program?"

**Flow**:
1. Supervisor routes to Responder
2. Responder searches FAQ
3. Returns answer to user

### Workflow 3: Full Content Pipeline

**User**: "Create a post, review it, and schedule it"

**Flow**:
1. Content Creator → creates draft
2. Moderator → reviews and approves
3. Scheduler → suggests posting time

## Submission Checklist

- [ ] 4+ specialized agents implemented
- [ ] Supervisor routing works correctly
- [ ] Shared tools accessible to all agents
- [ ] Multi-step workflows demonstrated
- [ ] README with architecture diagram
- [ ] Example conversations documented

## Resources

- [Google ADK Multi-Agent Docs](https://google.github.io/adk-docs/agents/multi-agents/)
- [Live Demo Code](../live-demo/community_management_team/)

---

## Questions?

Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel
