# Session 5: AI Agents - Part 2 (Multi-Agent Systems)

**Date:** December 3, 2025  
**Instructor:** Sonika  
**Duration:** 60 minutes

## 🎯 Learning Objectives

By the end of this session, you will:

- Design multi-agent architectures
- Implement agent-to-agent communication
- Coordinate specialized agents
- Create supervisor/worker patterns
- Handle complex workflows with multiple agents

## 📚 What We'll Cover

- Multi-agent system fundamentals
- Agent collaboration and orchestration
- Specialized agents and handoffs
- ADK multi-agent patterns
- A2A (Agent-to-Agent) communication
- MCP (Model Context Protocol) integration

## 🧠 Key Concepts

### What is a Multi-Agent System?

A multi-agent system is a collection of AI agents that:
- **Specialize** - Each agent has a focused role
- **Communicate** - Agents share information and hand off work
- **Coordinate** - A supervisor or protocol manages the workflow
- **Collaborate** - Agents work together to accomplish complex tasks

### Single Agent vs. Multi-Agent

| Single Agent | Multi-Agent System |
|--------------|-------------------|
| One agent handles everything | Specialized agents for each task |
| Limited expertise | Deep expertise per agent |
| Simple workflows | Complex, multi-step workflows |
| Single point of failure | Resilient, distributed work |
| Harder to scale | Easy to add new specialists |

### Multi-Agent Patterns

| Pattern | Description | Best For |
|---------|-------------|----------|
| **Supervisor-Worker** | One coordinator, multiple specialists | Task routing, quality control |
| **Pipeline** | Sequential handoffs between agents | Content creation, data processing |
| **Collaborative** | Agents work together on same task | Complex problem solving |
| **Hierarchical** | Manager agents with sub-agents | Large-scale orchestration |

## 🛠️ Technical Stack

- Python 3.11+
- Google ADK (Agent Development Kit)
- A2A Protocol (Agent-to-Agent)
- MCP (Model Context Protocol)
- Gemini API

## 📁 Folder Structure

```text
session-05-multi-agents/
├── README.md                    # This file
├── live-demo/                   # Code from live session
│   ├── README.md
│   └── community_management_team/
│       ├── __init__.py
│       ├── agent.py             # Main multi-agent setup
│       ├── agents/              # Individual agent definitions
│       │   ├── __init__.py
│       │   ├── content_creator.py
│       │   ├── responder.py
│       │   ├── moderator.py
│       │   └── scheduler.py
│       ├── tools/               # Shared tools
│       │   ├── __init__.py
│       │   └── community_tools.py
│       └── requirements.txt
├── starter-template/            # Template for participants
│   ├── README.md
│   ├── requirements.txt
│   └── multi_agent_starter/
│       ├── __init__.py
│       ├── agent.py
│       └── agents/
│           ├── __init__.py
│           └── specialist.py
├── use-case-guides/             # Detailed guides for each use case
│   ├── community-management-system.md
│   ├── event-planning-taskforce.md
│   └── content-production-pipeline.md
└── participants/                # Participant submissions
    └── ...
```

## 🚀 Quick Start

### Before the Session

1. Complete [GCP Setup](../../getting-started/gcp-setup.md)
2. Complete [Python Environment Setup](../../getting-started/python-environment.md)
3. Review Session 4 materials on single agents

### During the Session

1. Follow along with the live demo
2. Ask questions in the chat
3. Complete the hands-on activity

### After the Session

1. Choose a use case
2. Build your multi-agent system
3. Deploy to GitHub
4. Submit your work

## 📖 Resources

- [Live Demo Code](./live-demo/)
- [Starter Template](./starter-template/)
- [Use Case Guides](./use-case-guides/)

## 🎯 What We'll Build Together

A **Community Management Multi-Agent System** where:
- Each agent has a specialized role
- Agents communicate and hand off work
- A supervisor coordinates the team
- System accomplishes complex tasks

### Agent Team

| Agent | Role |
|-------|------|
| **Content Creator** | Generates social media posts, event descriptions |
| **Responder** | Answers common Slack/social questions |
| **Moderator** | Flags inappropriate content, spam |
| **Scheduler** | Plans content calendar, suggests posting times |
| **Supervisor** | Routes tasks to appropriate agent |

## 🏋️ Hands-on Activity (45 min)

1. **Design multi-agent architecture** (10 min)
2. **Implement 2-3 specialized agents** (20 min)
3. **Build supervisor/orchestration** (10 min)
4. **Test collaboration** (5 min)

## 📝 Homework Assignment

### Requirements

1. Build a multi-agent system with **at least 3 agents**
2. Implement **agent handoffs**
3. Add **shared memory/state** between agents
4. Create a **workflow diagram** of your system
5. Test **complex scenarios**
6. Document **when each agent gets invoked**

### Use Case Options

Choose one (or create your own):

1. **Community Management System** - Team of agents managing Slack, social media, content
2. **Event Planning Task Force** - Specialized agents for research, outreach, logistics, marketing
3. **Content Production Pipeline** - Sequential agents for research, writing, editing, SEO, promotion

### Submission

- Fork this repository
- Create a folder: `sessions/session-05-multi-agents/participants/[your-username]/`
- Add your code and README
- Submit a pull request

### Grading Criteria

- ✅ Multi-agent system works with at least 3 agents
- ✅ Agent handoffs are implemented
- ✅ Shared state/memory exists between agents
- ✅ Workflow diagram is included
- ✅ README documents agent responsibilities
- ✅ Complex scenario is demonstrated

## ❓ FAQ

**Q: How is this different from Session 4?**  
A: Session 4 covered single agents with tools. Session 5 focuses on multiple agents working together, with orchestration and handoffs.

**Q: Do I need to use all the patterns?**  
A: No! Start with one pattern (supervisor-worker is easiest) and expand from there.

**Q: Can I reuse my Session 4 agent?**  
A: Absolutely! Your Session 4 agent can become one specialist in your multi-agent system.

**Q: What if I get stuck?**  
A: Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel or check [Troubleshooting](../../resources/troubleshooting.md).

## 📚 Additional Resources

- [Google ADK Multi-Agent Documentation](https://google.github.io/adk-docs/agents/multi-agents/)
- [A2A Protocol Specification](https://google.github.io/A2A/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Gemini API Reference](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)

---

**Let's build amazing Multi-Agent Systems together! 🚀🤖🤖🤖**
