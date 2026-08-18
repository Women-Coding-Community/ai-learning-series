# Session 1: From Prompts to Harness: Build Your Own Agent Skill

**Level:** Entry-level friendly

## Overview

The kick-off. Every session in this series builds one more piece of an agent's harness, and this is where it begins. We start with the question that defines 2026: who governs the agents? You'll learn what a harness actually is, the bit Antigravity runs for you versus the bit only you can write, and we'll walk the whole lineage from prompt engineering to harness engineering so you've got the map for the next five months. Then we build something you keep: a hand-written `AGENTS.md` and your first reusable Agent Skill, running across the Antigravity IDE, the Antigravity CLI and Claude Code. We'll also show how that same skill carries into Google ADK, so yes, we're building agents from day one.

## Live Build

- Hand-write one `AGENTS.md` for a real project (conventions, do-not-touch zones, unsolved issues)
- Write one `SKILL.md` (a reusable playbook the agent loads by name)
- Run the same skill across surfaces: Antigravity IDE, Antigravity CLI, Claude Code
- Show that an Antigravity CLI skill is, in effect, skills for Google ADK, so what we write here travels into agent frameworks too

### Skill built live in this session

[`live-demo/accessibility-report/`](live-demo/accessibility-report/) is the actual `SKILL.md` demoed live: audits a URL for accessibility issues against WCAG 2.2 using Chrome and Lighthouse, writes both a Markdown and an interactive HTML report, and files a GitHub issue for any critical failures. Use it as a worked example of a real, non-trivial skill, not just the starter template, when you're writing your own.

### Another example: a reference skill, not a task skill

Not every skill is a step-by-step task like the one above. [`../../.agents/skills/wcc-branding/`](../../.agents/skills/wcc-branding/) is a different shape: a brand/style reference skill that applies WCC's Harness Series colour palette, tone of voice and writing conventions to anything generated for this repo or its channels. Worth a look for how a skill can encode "house style" rather than a procedure.

## Steal This

The "onboard the agent like a new joiner" pattern.

## Takeaway

One portable skill you own, working in more than one tool.

## Folder structure

```
session-01-agent-skill/
├── live-demo/                       # Built live in the session
│   └── accessibility-report/
│       └── SKILL.md                 # WCAG 2.2 audit skill, Chrome + Lighthouse, MD/HTML reports, files GitHub issues
├── starter-template/    # AGENTS.md and SKILL.md templates to fill in — see its README
│   ├── AGENTS.md
│   └── skill-template/SKILL.md
└── participants/        # Submit your own version here (see badges/badge-criteria.md)
```

See also [`.agents/skills/wcc-branding/`](../../.agents/skills/wcc-branding/) at the repo root, a reference/style skill rather than a task skill, worth comparing against `accessibility-report` to see the difference in shape.

## Setup

See [`getting-started/`](../../getting-started/) for the general prerequisites (Python, GCP/LLM API key, Antigravity, Claude Code, Google ADK). A session-specific setup checklist is posted in [#ai-learning-series](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) the week before.
