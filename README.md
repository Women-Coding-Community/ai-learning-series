# Women Coding Community - AI Learning Series

This repository contains hands-on resources, code templates, and project guides for the **WCC AI Learning Series**.

---

## 🔥 Current Series: The Harness Series

**Working title:** *Stop Prompting, Start Delegating*

Women Coding Community presents the AI Learning Series: one hands-on session a month, no heavy slides, real tools and real code you can use at work.

Over six months we build an agent's **harness** from the ground up, the instructions, skills, tools and guardrails that turn a capable model into an agent that does your work, then we close the **loop** so your agents run while you sleep.

**Format:** 6 sessions, one per month
**Cadence:** 3rd Tuesday of every month
**Delivery:** Hands-on, live-build, minimal slides
**Facilitators:** Sonika Janagill (Series Lead, Google track), with Rajani Rao (Founder/Director WCC, Microsoft track) following up each session with a companion piece mapping the same patterns to Agent Framework and Foundry

**Live builds run on:** Antigravity (IDE + CLI), Claude Code, Google ADK

### The run

| # | Session | Level |
|---|---------|-------|
| 1 | [Build Your Own Agent Skill](sessions/session-01-agent-skill/) | Entry-level friendly |
| 2 | [Tools & Boundaries: MCP, Plugins, Permissions, Hooks](sessions/session-02-tools-boundaries/) | All levels |
| 3 | [Small Models in Practice](sessions/session-03-small-models/) | All levels |
| 4 | [Sub-Agents & Specialisation](sessions/session-04-sub-agents/) | Intermediate |
| 5 | [AI in the SDLC & CI/CD](sessions/session-05-sdlc-cicd/) | Intermediate |
| 6 | [Loop Engineering + Demo Day](sessions/session-06-loop-engineering/) | Advanced, community showcase |

Dates are confirmed session by session in [#ai-learning-series](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) and on [Meetup](https://www.meetup.com/women-coding-community/).

### Setup

Each session has its own quick setup guide, posted the week before in Slack, so live time stays for building. General prerequisites:

- Some Python
- A Google Cloud account (free tier is fine) or an LLM API key
- Antigravity (IDE + CLI) and Claude Code installed
- Google ADK installed locally

See [`getting-started/`](getting-started/) for the detailed guides.

### How each session works (60 min)

1. Welcome & recap (5 min)
2. Concept framing (10 min)
3. Live build (30 min), real code, real tools, debug in the open
4. Participant activity / steal-this pattern (10 min)
5. Q&A + next-session teaser (5 min)

---

## 📁 Repository Structure

```
ai-learning-series/
├── README.md                          # This file
├── STRUCTURE.md                       # Detailed structure notes
├── getting-started/                   # Setup guides
├── sessions/
│   ├── session-01-agent-skill/
│   │   ├── live-demo/                 # Code from the live session
│   │   ├── starter-template/          # Template for participants
│   │   └── participants/              # Participant submissions
│   ├── session-02-tools-boundaries/
│   ├── session-03-small-models/
│   ├── session-04-sub-agents/
│   ├── session-05-sdlc-cicd/
│   └── session-06-loop-engineering/
├── resources/                         # Cross-session reference material
├── utilities/                         # Shared scripts/helpers
└── badges/                            # Participation badge criteria
```

---

## 🚀 Quick Start

### For Instructors

1. Review the session materials in `/sessions/session-0X-.../`
2. Check `/getting-started/` for setup guides
3. Use `/resources/` for reference materials

### For Participants

1. Follow the setup guide in `/getting-started/`
2. Clone this repository
3. Navigate to your session folder
4. Use the starter template to begin coding
5. Submit your work to `/sessions/[session]/participants/[your-username]/`

---

## 🎓 Facilitators

- **Sonika Janagill** - Series Lead, Google track
- **Rajani Rao** - Founder/Director WCC, Microsoft track (companion piece)

---

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

We welcome contributions! Please:

1. Fork this repository
2. Create a feature branch
3. Submit a pull request with your improvements

---

<details>
<summary><strong>📚 2025 Series (Archived)</strong>, click to expand</summary>

# Women Coding Community - AI Learning Series 2025

Hands-on resources, code templates, and project guides for the original 12-week AI learning program.

## 🎯 Program Overview

**Format:** 12 sessions total (6 Foundational + 6 Advanced)
**Duration:** 60 minutes each
**Schedule:** Every other Wednesday, starting November 5th, 2025
**Target Audience:** Coders with no/basic AI knowledge
**Delivery:** Hands-on, project-based learning
**Certification:** GitHub-tracked participation badges

### Timeline

- **Foundational Track:** Nov 5 - Dec 10 (6 weeks)
- **Break:** Last week of January (feedback & planning)
- **Advanced Track:** Jan 14 - Feb 18 (planned, never delivered)

## 🛠️ Tech Stack

**Primary Stack:** Python 3.11+, Google Cloud Platform (GCP), Vertex AI / Gemini API, Jupyter Notebooks, VS Code, Google Colab

**Alternative Options:** AWS (Bedrock, SageMaker), Azure (OpenAI Service), OpenAI GPT, Anthropic Claude

## 🎓 Facilitators

- **Sonika** - Foundational Track Lead
- **Sonali** - Advanced Track Lead

See the original session folders under `/sessions/` (`session-01-ai-chatbots` through `session-06-deploy-agent`) for full learning objectives, use cases, and participant submissions from the 2025 run. The series restarts in 2026 as **The Harness Series** above, rather than picking up the planned Advanced Track.

**Last Updated:** November 2025

</details>
