# Mentorship Team - WCC Mentorship Coordinator

An AI-powered mentorship coordinator that connects to the **live WCC website** and manages a local mentorship database. Demonstrates ADK tools, web scraping, and state management.

## 🎯 What This Demo Shows

- **Live Web Integration**: Fetches real data from womencodingcommunity.com
- **MCP-Style Tools**: File operations, web scraping, database management
- **State Management**: Local profiles database for registrations
- **Multi-Role Agent**: Acts as different specialists based on task

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Request                              │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              MENTORSHIP COORDINATOR                          │
│         (Acts as different specialists)                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  📝 INTAKE  │ │  🌐 WCC WEB │ │ 🎯 MATCHING │
│             │ │             │ │             │
│ save_profile│ │ search_wcc_ │ │ find_mentors│
│ read_guide  │ │ mentors     │ │ match_mentee│
│ list_profile│ │ get_events  │ │             │
│             │ │ get_faq     │ │             │
└─────────────┘ └─────────────┘ └─────────────┘
         │             │             │
         ▼             │             │
┌─────────────┐        │             │
│profiles.json│        │             │
│(local DB)   │        │             │
└─────────────┘        │             │
                       ▼             
              ┌─────────────────┐
              │  WCC Website    │
              │  (live data)    │
              └─────────────────┘
```

## 🚀 Quick Start

```bash
cd sessions/session-05-multi-agents/live-demo
adk web
```

Select **mentorship_team** from the dropdown.

---

## � Demo Script (10 minutes)

### Step 1: Explore Live WCC Data (2 min)

```
"What events are coming up at WCC?"
```
→ Fetches live events from womencodingcommunity.com/events

```
"Tell me about the WCC mentorship program"
```
→ Fetches overview from womencodingcommunity.com/mentorship

```
"What are the FAQs for mentorship?"
```
→ Fetches FAQ from womencodingcommunity.com/mentorship-faq

### Step 2: Search WCC Mentors (2 min)

```
"Search WCC website for mentors"
```
→ Fetches mentor list from womencodingcommunity.com/mentors

```
"Search WCC for Python mentors"
```
→ Filters mentors by skill

### Step 3: View Local Database (1 min)

```
"Show all registered profiles"
```
→ Shows profiles from local profiles.json (pre-loaded sample data)

### Step 4: Register a New User (3 min)

```
"I want to register as a mentee"
```
→ Agent collects: name, email, goals, availability, bio, LinkedIn
→ Saves to local profiles.json

### Step 5: Find a Match (2 min)

```
"Find me a mentor for Python"
```
→ Searches local database for Python mentors

```
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

```
mentorship_team/
├── agent.py                 # Main agent with all tools
├── agent.yaml               # A2A agent card
├── __init__.py
├── profiles.json            # Local database (sample data)
├── program_guidelines.txt   # Program rules
├── README.md
├── tools/
│   └── mentorship_tools.py  # All tool implementations
└── agents/
    ├── intake.yaml          # A2A card for intake role
    ├── verification.yaml    # A2A card for verification role
    └── matching.yaml        # A2A card for matching role
```

---

## 🎓 Key Teaching Points

1. **Live Web Integration**: Agent fetches real data from WCC website
2. **MCP Pattern**: Tools mirror what MCP servers would provide
3. **State Management**: Local JSON database for persistence
4. **Multi-Role Agent**: Single agent acts as different specialists
5. **A2A Cards**: YAML files describe agent capabilities

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
