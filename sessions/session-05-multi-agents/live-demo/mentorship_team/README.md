# Mentorship Team - WCC Mentorship Multi-Agent System

An AI-powered mentorship coordinator using **Agent-to-Agent (A2A)** communication. The supervisor agent routes requests to specialized agents that handle registrations, verification, and matching. Integrates with the **live WCC website** and manages a local mentorship database.

## 🎯 What This Demo Shows

- **Agent-to-Agent Communication**: Supervisor delegates to specialized agents
- **Separation of Concerns**: Each agent has a focused responsibility
- **Live Web Integration**: Fetches real data from womencodingcommunity.com
- **MCP-Style Tools**: File operations, web scraping, database management
- **Routing/Delegation Pattern**: Dynamic routing based on request type

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                        User Request                         │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│          MENTORSHIP SUPERVISOR (Routing Agent)               │
│     Routes requests to appropriate specialist agents         │
└─────────────────────────────┬────────────────────────────────┘
                              │
         ┌────────────────────┼───────────────────────┐
         │                    │                       │
         ▼                    ▼                       ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  📝 INTAKE      │ │  ✅ VERIFICATION │ │  🎯 MATCHING    │
│  SPECIALIST      │ │  SPECIALIST      │ │  SPECIALIST      │
├──────────────────┤ ├──────────────────┤ ├──────────────────┤
│ • save_profile   │ │ • verify_online_ │ │ • find_mentors_  │
│ • read_guidelines│ │   presence       │ │   by_skill       │
│ • list_profiles  │ │ • list_profiles  │ │ • match_mentee   │
│                  │ │                  │ │ • search_wcc_    │
│                  │ │                  │ │   mentors        │
│                  │ │                  │ │ • get_wcc_page_  │
│                  │ │                  │ │   info           │
│                  │ │                  │ │ • get_wcc_faq    │
│                  │ │                  │ │ • get_wcc_events │
└────────┬─────────┘ └──────────────────┘ └────────┬─────────┘
         │                                         │
         ▼                                         ▼
┌─────────────────┐                    ┌──────────────────────┐
│  profiles.json  │                    │   WCC Website        │
│  (local DB)     │                    │   (live data)        │
└─────────────────┘                    └──────────────────────┘
```

## 🔄 Communication Pattern

This is a **routing/delegation pattern** (not sequential):

- **Supervisor** receives request and determines which specialist to route to
- **Specialist agents** execute their specific tasks independently
- **Complex workflows** may chain multiple specialists in sequence
- Each specialist only has access to tools relevant to their role

## 🚀 Quick Start

```bash
cd sessions/session-05-multi-agents/live-demo
adk web
```

Select **mentorship_team** from the dropdown.

---

## � Demo Script (10 minutes)

### Step 1: Explore Live WCC Data (2 min)

```text
"What events are coming up at WCC?"
```

→ Fetches live events from womencodingcommunity.com/events

```text
"Tell me about the WCC mentorship program"
```

→ Fetches overview from womencodingcommunity.com/mentorship

```text
"What are the FAQs for mentorship?"
```

→ Fetches FAQ from womencodingcommunity.com/mentorship-faq

### Step 2: Search WCC Mentors (2 min)

```text
"Search WCC website for mentors"
```

→ Fetches mentor list from womencodingcommunity.com/mentors

```text
"Search WCC for Python mentors"
```

→ Filters mentors by skill

### Step 3: View Local Database (1 min)

```text
"Show all registered profiles"
```

→ Shows profiles from local profiles.json (pre-loaded sample data)

### Step 4: Register a New User (3 min)

```text
"I want to register as a mentee"
```

→ Agent collects: name, email, goals, availability, bio, LinkedIn
→ Saves to local profiles.json

### Step 5: Find a Match (2 min)

```text
"Find me a mentor for Python"
```

→ Searches local database for Python mentors

```text
"Find a match for Alex Kim"
```

→ Runs matching algorithm for registered mentee

---

## 🛠️ All Tools

### Local Database Tools

| Tool | Description |
|------|-------------|
| `save_profile()` | Register new mentor/mentee |
| `list_profiles()` | Show all registered users |
| `read_guidelines()` | Show program requirements |
| `find_mentors_by_skill()` | Search local mentors |
| `match_mentee()` | Match a mentee with mentors |
| `verify_online_presence()` | Verify LinkedIn profile |

### WCC Website Tools (Live Data)

| Tool | URL | Description |
|------|-----|-------------|
| `search_wcc_mentors()` | /mentors | Search WCC mentors |
| `get_wcc_mentorship_overview()` | /mentorship | Program overview |
| `get_wcc_faq()` | /mentorship-faq | FAQ content |
| `get_wcc_events()` | /events | Upcoming events |
| `get_wcc_page_info()` | /mentors | Page metadata |

---

## 📁 Files

```text
mentorship_team/
├── agent.py                          # Supervisor agent (routing logic)
├── __init__.py
├── profiles.json                     # Local database (sample data)
├── program_guidelines.txt            # Program rules
├── README.md
├── tools/
│   ├── __init__.py
│   └── mentorship_tools.py           # All tool implementations
└── agents/
    ├── __init__.py                   # Exports all specialist agents
    ├── intake_specialist.py          # Handles registrations
    ├── verification_specialist.py    # Verifies credentials
    ├── matching_specialist.py        # Matches mentees with mentors
    ├── intake.yaml                   # A2A card for intake role
    ├── verification.yaml             # A2A card for verification role
    └── matching.yaml                 # A2A card for matching role
```

---

## 🎓 Key Teaching Points

1. **Agent-to-Agent Communication**: Supervisor routes to specialized agents
2. **Separation of Concerns**: Each agent has focused responsibility
3. **Routing/Delegation Pattern**: Dynamic routing based on request type
4. **Live Web Integration**: Agents fetch real data from WCC website
5. **MCP Pattern**: Tools mirror what MCP servers would provide
6. **State Management**: Local JSON database for persistence
7. **A2A Cards**: YAML files describe agent capabilities

---

## 💡 Demo Tips

- **Start with live data** - Shows real-world integration
- **Then show local database** - Demonstrates state management
- **Register someone** - Shows write operations
- **Run matching** - Shows business logic in tools

## ❓ Troubleshooting

**"Could not fetch page"**

- Check internet connection
- WCC website might be temporarily unavailable

**"No profiles found"**

- profiles.json might be empty
- Register a user first or check the file exists
