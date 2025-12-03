# WCC Tech Scout - Multi-Agent Demo

## Overview

A 45-minute live demo showcasing the **Google Agent Stack**:
- **ADK** (Agent Development Kit) - Build agents
- **A2A** (Agent-to-Agent Protocol) - Connect agents
- **MCP** (Model Context Protocol) - Provide context

We'll build a 2-agent system: **Researcher** + **Editor** working together.

---

## 🎯 What We're Building

```
┌─────────────────────────────────────────────────────────────┐
│                    User Request                              │
│        "Research the latest on Agentic AI"                   │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   RESEARCHER AGENT                           │
│              (ADK + Google Search Tool)                      │
│                                                              │
│  🔍 Finds accurate, up-to-date information                   │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              │  A2A Handoff (Context Passing)
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    EDITOR AGENT                              │
│                  (ADK + MCP FileSystem)                      │
│                                                              │
│  📝 Synthesizes research into formatted report               │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Output: report.md                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧠 Key Concepts

### The Google Agent Stack

| Component | What It Does | Analogy |
|-----------|--------------|---------|
| **ADK** | Framework to build agents (Python SDK) | The blueprint for your agent |
| **A2A** | Protocol for agents to communicate | HTTP for Agents |
| **MCP** | Standard for connecting to data/tools | USB-C port for AI |

### Why Multi-Agent?

| Single Agent | Multi-Agent System |
|--------------|-------------------|
| Freelancer doing sales, coding, support | Company with specialists |
| Gets confused with too many tools | Each agent is focused |
| Hard to maintain | Easy to extend |

---

## 🚀 Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

### Run the Demo

```bash
# Option 1: Run the full pipeline
python pipeline.py

# Option 2: Test agents individually
python researcher.py
python editor.py

# Option 3: Use ADK Web Interface
adk web
```

---

## 📁 Files in This Demo

```text
wcc_tech_scout/
├── README.md                # This file
├── requirements.txt         # Dependencies
├── __init__.py             # Package init
├── agent.py                # Main orchestration (for ADK web)
├── researcher.py           # Researcher agent with Google Search
├── editor.py               # Editor agent with MCP FileSystem
├── pipeline.py             # A2A orchestration script
├── mcp_config.json         # MCP server configuration
└── .reports/               # Where reports are saved (hidden from ADK)
```

---

## ⏱️ Demo Flow (45 Minutes)

### Part 1: Introduction (0-5 min)
- Recap single agents from Session 4
- The problem: Single agents get confused with too many tools
- Visual: Freelancer vs. Company analogy

### Part 2: Tech Stack Explained (5-10 min)
- **ADK**: How we define "who the agent is"
- **A2A**: How agents talk to each other
- **MCP**: How agents connect to tools/data

### Part 3: Live Coding (10-35 min)
1. Build the Researcher (ADK + Google Search)
2. Build the Editor (ADK + MCP)
3. Connect them (A2A Pattern)

### Part 4: Production & Deployment (35-40 min)
- Vertex AI Agent Engine overview
- The deploy flow: `agent.yaml` → `adk deploy`

### Part 5: Wrap-Up (40-45 min)
- Homework assignment
- Q&A

---

## 💡 Pro Tips (Speaker Notes)

### On MCP
> "MCP prevents vendor lock-in. If you write a tool for Claude, it works for Gemini if you use MCP. This is huge for developers."

### On A2A
> "A2A isn't just for Python scripts. It allows a Java agent in a bank to talk to a Python agent in a retail store securely."

### On Deployment
> "Vertex AI Agent Engine handles the state (memory) for you, so you don't have to manage databases for conversation history."

---

## 📚 Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [A2A Protocol Specification](https://google.github.io/A2A/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Vertex AI Agent Builder](https://cloud.google.com/vertex-ai/docs/agents)

---

## 🏠 Homework

Build the **Event Planning Task Force** using the patterns learned today:
- Research Agent → finds topics and speakers
- Outreach Agent → drafts emails
- Logistics Agent → handles scheduling
- Marketing Agent → creates promo content

See: [Event Planning Task Force Guide](../../use-case-guides/event-planning-taskforce.md)

---

**Let's build a team of agents! 🚀🤖🤖**
