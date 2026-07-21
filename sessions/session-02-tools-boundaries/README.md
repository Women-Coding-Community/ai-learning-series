# Session 2: Tools & Boundaries: MCP, Plugins, Permissions, Hooks

**Level:** All levels

## Overview

An agent is only as useful as the tools you trust it with, and only as safe as the boundaries around them. This session is the governance half of the harness. We'll give the agent hands and eyes through MCP servers and plugins (think Jira, GitLab, Gmail), then put the seatbelt on with permissions (allow, ask, deny) and per-project boundaries, so your work tools never leak into hobby projects. We finish with hooks: un-skippable JSON gates the agent physically cannot bypass, like a pre-commit secret scan that fires on every agent commit. You'll leave with an agent that can act, but only exactly where you've let it.

## Live Build

- Wire one MCP server, scoped to a single project (work tools never leak into hobby projects)
- Add a pre-commit JSON hook that scans for secrets on every agent commit
- Set permissions and a sandbox policy

## Steal This

Project-scoped MCP, governance by default.

## Takeaway

An agent that can act, but only where you've allowed it.

## Folder structure

```
session-02-tools-boundaries/
├── live-demo/           # MCP config and pre-commit hook built live
├── starter-template/    # Blank starting point to follow along
└── participants/        # Submit your own version here (see badges/badge-criteria.md)
```

## Setup

See [`getting-started/`](../../getting-started/) for the general prerequisites. A session-specific setup checklist is posted in [#ai-learning-series](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) the week before.
