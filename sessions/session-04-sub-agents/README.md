# Session 4: Sub-Agents & Specialisation

**Level:** Intermediate

## Overview

No team hires one person to be the security expert, QA, architect and tech writer all in the same afternoon. So why ask one agent to do all of it in a single chat window, where the security review drowns under test logs and debug chatter? This session is about specialisation. We'll dynamically define and invoke sub-agents, each with its own clean, scoped context, running in parallel and reporting back only the result. You'll see why a focused context beats a stuffed one, and why four specialists fail gracefully where one generalist fails completely. We build it live by splitting one real task across sub-agents (a security pair that reviews a diff while a second drafts the fix), then cover delegation patterns you can steal straight away.

## Live Build

- Split one real task across sub-agents (e.g. the security pair: one reviews the diff, one drafts the fix)
- Show fan-out fetch (one specialist per source) and scanner → codemod → verifier
- Touch on auto-provisioned worktrees for isolation

## Steal This

Delegation patterns that work today.

## Takeaway

One chunky ticket, split across a reviewer, a fixer and a tester.

## Folder structure

```
session-04-sub-agents/
├── live-demo/           # Sub-agent definitions and orchestration code
├── starter-template/    # Blank starting point to follow along
└── participants/        # Submit your own version here (see badges/badge-criteria.md)
```

## Setup

See [`getting-started/`](../../getting-started/) for the general prerequisites. A session-specific setup checklist is posted in [#ai-learning-series](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) the week before.
