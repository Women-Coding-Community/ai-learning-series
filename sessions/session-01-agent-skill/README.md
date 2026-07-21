# Session 1: From Prompts to Harness: Build Your Own Agent Skill

**Level:** Entry-level friendly

## Overview

The kick-off. Every session in this series builds one more piece of an agent's harness, and this is where it begins. We start with the question that defines 2026: who governs the agents? You'll learn what a harness actually is, the bit Antigravity runs for you versus the bit only you can write, and we'll walk the whole lineage from prompt engineering to harness engineering so you've got the map for the next five months. Then we build something you keep: a hand-written `AGENTS.md` and your first reusable Agent Skill, running across the Antigravity IDE, the Antigravity CLI and Claude Code. We'll also show how that same skill carries into Google ADK, so yes, we're building agents from day one.

## Live Build

- Hand-write one `AGENTS.md` for a real project (conventions, do-not-touch zones, unsolved issues)
- Write one `SKILL.md` (a reusable playbook the agent loads by name)
- Run the same skill across surfaces: Antigravity IDE, Antigravity CLI, Claude Code
- Show that an Antigravity CLI skill is, in effect, skills for Google ADK, so what we write here travels into agent frameworks too

## Steal This

The "onboard the agent like a new joiner" pattern.

## Takeaway

One portable skill you own, working in more than one tool.

## Folder structure

```
session-01-agent-skill/
├── live-demo/           # AGENTS.md and SKILL.md built live in the session
├── starter-template/    # AGENTS.md and SKILL.md templates to fill in — see its README
│   ├── AGENTS.md
│   └── skill-template/SKILL.md
└── participants/        # Submit your own version here (see badges/badge-criteria.md)
```

## Setup

See [`getting-started/`](../../getting-started/) for the general prerequisites (Python, GCP/LLM API key, Antigravity, Claude Code, Google ADK). A session-specific setup checklist is posted in [#ai-learning-series](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) the week before.
