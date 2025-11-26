# Event Scheduler Agent - Use Case Guide

## Overview

Build an AI-powered event scheduling assistant that helps WCC members find optimal meeting times, schedules study groups, and manages event logistics through natural language conversations.

## Problem Statement

**Challenge**: Coordinating schedules for study groups, mentorship sessions, or community events is tedious:
Endless "back-and-forth" messages to find common availability
Confusion over time zones (crucial for a global community)
Forgetfulness regarding calendar invites and reminders
Difficulty finding specific event details in long chat histories

**Why it matters**: Reducing friction in scheduling encourages more peer learning, mentorship connections, and community engagement.

## What You'll Build

A conversational scheduling agent that:

- Parses natural language dates and times (e.g., "next Tuesday at 2pm")
- Handles time zone conversions automatically
- Generates formatted calendar invites

## Architecture

┌─────────────────┐
│   User Input    │
│ ("Book a slot") │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Gemini API with Scheduler Persona │
│  (Tools: Time parser, Calendar API) │
└────────┬────────────────────────────┘
         │
         │
         ▼
┌─────────────────────────────────────┐
│      Output & Confirmation          │
└─────────────────────────────────────┘


### Step 1: Create Scheduler Data & Utilities

Create schedule_utils.py to handle time logic and mock calendar data:

```python
from datetime import datetime, timedelta
import pytz

# Mock Calendar Data
CALENDAR_DB = {
    "mentors": {
        "sarah": ["2023-10-27T10:00:00", "2023-10-27T14:00:00"],
        "ami": ["2023-10-27T09:00:00", "2023-10-27T11:00:00"]
    }
}

def check_availability(person, requested_time_str):
    """Check if a person is free at a specific ISO format time"""
    busy_slots = CALENDAR_DB.get("mentors", {}).get(person.lower(), [])
    # Simplified check: exactly matching start times are 'busy'
    if requested_time_str in busy_slots:
        return False
    return True

def convert_timezone(time_str, from_tz, to_tz):
    """Convert time between zones"""
    local = pytz.timezone(from_tz)
    target = pytz.timezone(to_tz)
    
    # Parse and localize
    dt = datetime.fromisoformat(time_str)
    if dt.tzinfo is None:
        dt = local.localize(dt)
    
    return dt.astimezone(target).isoformat()
```

### Step 2: Build the Scheduler Agent

Create scheduler_agent/agent.py with a focused system prompt:

```python
import os
from dotenv import load_dotenv
from schedule_utils import check_availability, convert_timezone
# Import the core Agent class from the ADK
from google.adk.agents.llm_agent import Agent

load_dotenv()

# --- AGENT DEFINITION ---

root_agent = Agent(
    name="scheduler_event_agent",
    model="gemini-2.5-flash-lite",
    instruction="""You are the WCC Event Scheduler Agent.
    Your goal is to help members book study sessions and mentorship calls effortlessly.
    Capabilities:
    1. Understand natural language date/time requests.
    2. Always ask for Time Zones if not provided.
    3. Check availability for specific mentors.
    4. Confirm details before finalizing.
    Current Date: {current_date}
    Guidelines:
    - Be concise and efficient.
    - If a user says "tomorrow", calculate the date based on Current Date.
    - If a slot is busy, politely suggest an alternative.
    - Output confirmation in a clear, bulleted format.
    """,
    tools=[check_availability, convert_timezone]
)

```

## Submission Checklist

- ✅ Agent understands date/time natural language
- ✅ Handles time zone conversions logic
- ✅ Checks availability constraints
- ✅ Returns clear confirmation messages
- ✅ README included with setup steps

---

## Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/get-started/)
- [Gemini API Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini-api)
- [Python Documentation](https://docs.python.org)


---

## Questions?

Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel

---