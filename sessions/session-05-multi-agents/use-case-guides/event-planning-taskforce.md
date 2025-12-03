# Event Planning Task Force - Use Case Guide

## Overview

Build a team of specialized AI agents that collaborate to plan community events, from initial research to final promotion.

## Problem Statement

**Challenge**: Planning events involves multiple distinct tasks:
- Researching trending topics and potential speakers
- Drafting outreach emails to speakers
- Handling logistics (venue, time, tech requirements)
- Creating marketing and promotional content

**Why it matters**: Well-planned events drive community engagement. Coordinating all these tasks manually is time-consuming and error-prone.

## What You'll Build

A multi-agent task force with:
- **Research Agent**: Finds trending topics and potential speakers
- **Outreach Agent**: Drafts speaker invitation emails
- **Logistics Agent**: Handles venue, time, and tech requirements
- **Marketing Agent**: Creates promotional content
- **Supervisor**: Manages the overall event planning workflow

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Event Planning Request                    │
│        "Plan a workshop on AI careers for January"           │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    SUPERVISOR AGENT                          │
│              Coordinates the planning workflow               │
└──────┬──────────┬──────────┬──────────┬────────────────────┘
       │          │          │          │
       ▼          ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Research │ │ Outreach │ │Logistics │ │Marketing │
│  Agent   │ │  Agent   │ │  Agent   │ │  Agent   │
│          │ │          │ │          │ │          │
│ Topics & │ │ Speaker  │ │ Venue &  │ │ Promo    │
│ Speakers │ │ Emails   │ │ Schedule │ │ Content  │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
       │          │          │          │
       └──────────┴──────────┴──────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Complete Event Plan                        │
│   Topic + Speakers + Logistics + Marketing Materials         │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Guide

### Step 1: Define Your Agent Team

Create a folder structure:

```text
event_planning_taskforce/
├── __init__.py
├── agent.py                 # Supervisor
├── agents/
│   ├── __init__.py
│   ├── researcher.py
│   ├── outreach.py
│   ├── logistics.py
│   └── marketing.py
├── tools/
│   ├── __init__.py
│   └── planning_tools.py
└── requirements.txt
```

### Step 2: Create Planning Tools

```python
# tools/planning_tools.py

import json
from datetime import datetime, timedelta

# Mock data for demonstration
TRENDING_TOPICS = [
    {"topic": "AI Agents", "interest_score": 95, "difficulty": "intermediate"},
    {"topic": "Career Transitions to Tech", "interest_score": 90, "difficulty": "beginner"},
    {"topic": "System Design", "interest_score": 85, "difficulty": "advanced"},
    {"topic": "Python for Data Science", "interest_score": 88, "difficulty": "beginner"},
]

SPEAKER_DATABASE = [
    {"name": "Dr. Sarah Chen", "expertise": ["AI", "Machine Learning"], "availability": "flexible"},
    {"name": "Maria Rodriguez", "expertise": ["Career Development", "Leadership"], "availability": "weekends"},
    {"name": "Priya Sharma", "expertise": ["System Design", "Architecture"], "availability": "evenings"},
]

def get_trending_topics(category: str = "all") -> str:
    """Get trending topics for community events."""
    topics = TRENDING_TOPICS
    if category != "all":
        topics = [t for t in topics if category.lower() in t["topic"].lower()]
    return json.dumps(topics, indent=2)

def find_potential_speakers(topic: str) -> str:
    """Find speakers with expertise in a topic."""
    matches = []
    for speaker in SPEAKER_DATABASE:
        for expertise in speaker["expertise"]:
            if topic.lower() in expertise.lower():
                matches.append(speaker)
                break
    
    if matches:
        return json.dumps(matches, indent=2)
    return "No speakers found for this topic. Consider reaching out to the community."

def generate_email_template(speaker_name: str, event_topic: str, event_date: str) -> str:
    """Generate a speaker invitation email template."""
    template = f"""
Subject: Speaking Invitation - Women Coding Community Event

Dear {speaker_name},

I hope this email finds you well! I'm reaching out on behalf of the Women Coding Community.

We're planning an upcoming event on "{event_topic}" scheduled for {event_date}, and we believe your expertise would be invaluable to our community members.

Would you be interested in speaking at this event? We'd love to discuss:
- Format (workshop, talk, panel)
- Duration and timing
- Any support you might need

Our community of 5,000+ women in tech would greatly benefit from your insights.

Looking forward to hearing from you!

Best regards,
WCC Events Team
"""
    return template

def check_venue_availability(date: str, duration_hours: int = 2) -> str:
    """Check venue/platform availability for an event."""
    # Mock implementation
    return json.dumps({
        "date": date,
        "available_slots": ["10:00 AM GMT", "2:00 PM GMT", "6:00 PM GMT"],
        "platform": "Zoom (up to 500 participants)",
        "backup": "Google Meet",
        "tech_requirements": ["Screen sharing", "Recording capability", "Q&A feature"]
    }, indent=2)

def get_event_checklist(event_type: str) -> str:
    """Get a checklist for event planning."""
    checklists = {
        "workshop": [
            "[ ] Confirm speaker and topic",
            "[ ] Set date and time (consider time zones)",
            "[ ] Create event page/registration",
            "[ ] Prepare promotional materials",
            "[ ] Send reminder emails (1 week, 1 day before)",
            "[ ] Test tech setup",
            "[ ] Prepare backup plan",
            "[ ] Create feedback survey",
        ],
        "panel": [
            "[ ] Confirm all panelists",
            "[ ] Assign moderator",
            "[ ] Prepare discussion questions",
            "[ ] Set up registration",
            "[ ] Create promotional content",
            "[ ] Brief panelists before event",
        ],
    }
    return "\n".join(checklists.get(event_type.lower(), checklists["workshop"]))

def create_promo_content(event_name: str, date: str, speaker: str, description: str) -> str:
    """Generate promotional content for social media."""
    content = {
        "twitter": f"🎉 Join us for {event_name}!\n\n📅 {date}\n🎤 Speaker: {speaker}\n\n{description[:100]}...\n\nRegister now! #WomenInTech #WCC",
        "linkedin": f"Excited to announce our upcoming event!\n\n{event_name}\n\nDate: {date}\nSpeaker: {speaker}\n\n{description}\n\nThis is a great opportunity for women in tech to learn and connect. Don't miss out!\n\n#WomenInTech #TechCommunity #Learning",
        "slack": f"📢 *New Event Alert!*\n\n*{event_name}*\n📅 {date}\n🎤 {speaker}\n\n{description}\n\nReact with ✅ if you're interested!",
    }
    return json.dumps(content, indent=2)
```

### Step 3: Create Specialist Agents

**Research Agent:**

```python
# agents/researcher.py

from google.adk.agents import Agent
from ..tools.planning_tools import get_trending_topics, find_potential_speakers

researcher_agent = Agent(
    name="researcher",
    model="gemini-2.0-flash",
    instruction="""You are the Research Agent for WCC Event Planning.

YOUR ROLE:
- Identify trending topics for community events
- Find potential speakers with relevant expertise
- Provide data-driven recommendations

PROCESS:
1. Analyze trending topics in tech
2. Match topics to community interests
3. Identify speakers with relevant expertise
4. Provide recommendations with rationale

OUTPUT FORMAT:
- Topic recommendations with interest scores
- Speaker suggestions with expertise match
- Reasoning for recommendations
""",
    tools=[get_trending_topics, find_potential_speakers],
)
```

**Outreach Agent:**

```python
# agents/outreach.py

from google.adk.agents import Agent
from ..tools.planning_tools import generate_email_template

outreach_agent = Agent(
    name="outreach",
    model="gemini-2.0-flash",
    instruction="""You are the Outreach Agent for WCC Event Planning.

YOUR ROLE:
- Draft professional speaker invitation emails
- Personalize outreach based on speaker background
- Follow up on pending invitations

GUIDELINES:
- Be professional but warm
- Highlight benefits of speaking at WCC
- Include all necessary event details
- Make it easy for speakers to respond
""",
    tools=[generate_email_template],
)
```

**Logistics Agent:**

```python
# agents/logistics.py

from google.adk.agents import Agent
from ..tools.planning_tools import check_venue_availability, get_event_checklist

logistics_agent = Agent(
    name="logistics",
    model="gemini-2.0-flash",
    instruction="""You are the Logistics Agent for WCC Event Planning.

YOUR ROLE:
- Check venue/platform availability
- Manage event scheduling
- Ensure technical requirements are met
- Create event checklists

CONSIDERATIONS:
- Global audience (multiple time zones)
- Platform capacity and features
- Backup plans for technical issues
- Accessibility requirements
""",
    tools=[check_venue_availability, get_event_checklist],
)
```

**Marketing Agent:**

```python
# agents/marketing.py

from google.adk.agents import Agent
from ..tools.planning_tools import create_promo_content

marketing_agent = Agent(
    name="marketing",
    model="gemini-2.0-flash",
    instruction="""You are the Marketing Agent for WCC Event Planning.

YOUR ROLE:
- Create promotional content for events
- Adapt content for different platforms
- Maximize event visibility and registrations

PLATFORMS:
- Twitter: Short, engaging, hashtags
- LinkedIn: Professional, detailed
- Slack: Community-focused, interactive

GUIDELINES:
- Highlight value for attendees
- Include clear call-to-action
- Use appropriate emojis and formatting
""",
    tools=[create_promo_content],
)
```

### Step 4: Create Supervisor Agent

```python
# agent.py

from google.adk.agents import Agent
from .agents import (
    researcher_agent,
    outreach_agent,
    logistics_agent,
    marketing_agent,
)

root_agent = Agent(
    name="event_planning_supervisor",
    model="gemini-2.0-flash",
    instruction="""You coordinate the WCC Event Planning Task Force.

YOUR TEAM:
- @researcher: Finds topics and speakers
- @outreach: Drafts speaker invitations
- @logistics: Handles venue and scheduling
- @marketing: Creates promotional content

PLANNING WORKFLOW:
1. Research → Identify topic and speakers
2. Outreach → Draft speaker invitations
3. Logistics → Confirm venue and schedule
4. Marketing → Create promotional materials

For full event planning, coordinate all agents in sequence.
For specific tasks, route to the appropriate specialist.

Always provide a summary of progress and next steps.
""",
    sub_agents=[
        researcher_agent,
        outreach_agent,
        logistics_agent,
        marketing_agent,
    ],
)
```

## Example Workflows

### Workflow 1: Full Event Planning

**User**: "Plan a workshop on AI careers for January"

**Flow**:
1. Researcher → Suggests "AI Careers" topic, finds speakers
2. Outreach → Drafts invitation for recommended speaker
3. Logistics → Checks January availability, creates checklist
4. Marketing → Generates promo content for all platforms

### Workflow 2: Speaker Research Only

**User**: "Find speakers for a Python workshop"

**Flow**:
1. Supervisor routes to Researcher
2. Researcher searches speaker database
3. Returns list of Python experts

### Workflow 3: Create Marketing Materials

**User**: "Create promotional content for our Dec 10 workshop"

**Flow**:
1. Supervisor routes to Marketing
2. Marketing generates content for Twitter, LinkedIn, Slack
3. Returns formatted content for each platform

## Submission Checklist

- [ ] 4+ specialized agents implemented
- [ ] Full planning workflow demonstrated
- [ ] Shared tools for event data
- [ ] Agent handoffs working correctly
- [ ] README with workflow diagram
- [ ] Example event plan documented

## Resources

- [Google ADK Multi-Agent Docs](https://google.github.io/adk-docs/agents/multi-agents/)
- [Starter Template](../starter-template/)

---

## Questions?

Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel
