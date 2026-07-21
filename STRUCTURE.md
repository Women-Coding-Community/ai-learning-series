# Repository Structure Overview

## Complete Directory Layout

```text
ai-learning-series/
│
├── README.md                                    # Main repository overview
├── STRUCTURE.md                                 # This file
│
├── getting-started/                             # Setup & onboarding guides
│   ├── gcp-setup.md                            # GCP project & Vertex AI setup
│   ├── vertex-ai-quickstart.md                 # First API call tutorial
│   ├── gemini-api-key-setup.md                 # Gemini API key setup
│   ├── python-environment.md                   # Python venv & dependencies
│   └── alternative-platforms.md                # AWS, Azure, OpenAI guides
│
├── sessions/                                    # Session materials
│   │
│   ├── session-01-agent-skill/                 # 2026 · Session 1: Build Your Own Agent Skill
│   ├── session-02-tools-boundaries/            # 2026 · Session 2: MCP, Plugins, Permissions, Hooks
│   ├── session-03-small-models/                # 2026 · Session 3: Small Models in Practice
│   ├── session-04-sub-agents/                  # 2026 · Session 4: Sub-Agents & Specialisation
│   ├── session-05-sdlc-cicd/                   # 2026 · Session 5: AI in the SDLC & CI/CD
│   ├── session-06-loop-engineering/            # 2026 · Session 6: Loop Engineering + Demo Day
│   │   ├── README.md                           # Session overview & learning objectives
│   │   ├── live-demo/                          # Code from live session
│   │   ├── starter-template/                   # Template for participants
│   │   └── participants/                       # Participant submissions
│   │       └── [username]/
│   │           ├── code/
│   │           ├── README.md
│   │           └── demo.mp4
│   │
│   └── 2025 archive (Foundational Track, delivered)
│       ├── session-01-ai-chatbots/             # AI Fundamentals & LLM APIs
│       ├── session-02-prompt-eng/              # Prompt Engineering
│       ├── session-03-rag/                     # Introduction to RAG
│       ├── session-04-ai-agent/                # AI Agents - Part 1
│       ├── session-05-multi-agents/            # AI Agents - Part 2 / Multi-Agents
│       └── session-06-deploy-agent/            # Evaluation, Monitoring & Deployment
│
├── resources/                                   # Cross-session reference material
│   ├── prompt-engineering-guide.md
│   ├── security-checklist.md
│   ├── troubleshooting.md
│   └── reading-list.md
│
├── utilities/                                   # Shared scripts/helpers
│   ├── function_calling.py
│   ├── gcp_dlp_safety_pipeline.py
│   ├── safety_pipeline_multilayer.py
│   └── token_counter.py
│
└── badges/                                      # Participation tracking
    └── badge-criteria.md                       # Badge requirements & grading
```

## 2026: The Harness Series

The 2025 run delivered the 6-session Foundational Track (chatbots → deployment). The planned 6-session Advanced Track from that original 12-week plan was never delivered. Rather than pick that plan back up, 2026 restarts the series as **The Harness Series**: a new 6-session run building an agent's harness piece by piece, then closing the loop. See the [root README](README.md) for the full run and [`WCC-Harness-files/wcc-harness-series-outline-v1.md`](WCC-Harness-files/wcc-harness-series-outline-v1.md) for the detailed session-by-session outline this repo structure is built from.

### File status

**Complete for 2026 launch:**

- `README.md` — updated with The Harness Series overview, run table, and 2025 series archived below
- `STRUCTURE.md` — this file
- `sessions/session-01-agent-skill/` through `sessions/session-06-loop-engineering/` — README + `live-demo/`, `starter-template/`, `participants/` scaffolding for all 6 sessions
- `badges/badge-criteria.md` — updated with 2026 Harness Series badge, 2025 track archived

**To be added per session, as each one is delivered:**

- `live-demo/` code and configs (populated after each live session)
- `starter-template/` starting points (populated ahead of each session)
- Session-specific `use-case-guides/` if a session needs them

**Not yet updated for 2026 tooling:**

- `getting-started/` guides still assume Gemini API key + GCP as the only path; Antigravity (IDE + CLI), Claude Code, and Google ADK setup notes are pending

## Quick Navigation

### For Participants

- **Getting Started:** `getting-started/` — Setup guides (API keys, Antigravity, Claude Code, ADK)
- **Session Materials:** `sessions/session-01-agent-skill/` — Start of the 2026 run
- **Resources:** `resources/` — Reference materials
- **Badges:** `badges/badge-criteria.md` — Participation tracking

### For Instructors

- **Session Overview:** `sessions/session-0X-.../README.md`
- **Live Demo Code:** `sessions/session-0X-.../live-demo/`
- **Starter Template:** `sessions/session-0X-.../starter-template/`
- **Participant Submissions:** `sessions/session-0X-.../participants/`

## Session Timeline

| # | Session | Level | Status |
|---|---------|-------|--------|
| 1 | From Prompts to Harness: Build Your Own Agent Skill | Entry-level friendly | 📋 Dates TBC |
| 2 | Tools & Boundaries: MCP, Plugins, Permissions, Hooks | All levels | 📋 Dates TBC |
| 3 | Small Models in Practice | All levels | 📋 Dates TBC |
| 4 | Sub-Agents & Specialisation | Intermediate | 📋 Dates TBC |
| 5 | AI in the SDLC & CI/CD | Intermediate | 📋 Dates TBC |
| 6 | Loop Engineering + Demo Day | Advanced, community showcase | 📋 Dates TBC |

Dates lock to the 3rd Tuesday of every month once the first date is confirmed. Watch [#ai-learning-series](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) and [Meetup](https://www.meetup.com/women-coding-community/).

---

## Support

- **Questions?** Ask in [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7)
- **Issues?** Check `resources/troubleshooting.md`
- **Resources?** See `resources/reading-list.md`
- **Feedback?** Create an issue or PR

---

**Last Updated:** July 2026
**Repository:** Women Coding Community - AI Learning Series
