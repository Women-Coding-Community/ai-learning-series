# Session 5: AI in the SDLC & CI/CD

**Level:** Intermediate

## Overview

Now we take everything we've built and wire it into how you actually ship. This session is about putting AI checks where they belong in your delivery pipeline, and running them without blowing your API budget. We'll call a hosted model endpoint from GitHub Actions to run an automated code review, then post the results straight back as PR comments. We'll add test and lint gates as harness checks, and talk budget: when to reach for the small self-hosted model from Session 3 instead of a frontier API. We'll also cover the bit that quietly bites teams: how to scope and store the API token the runner uses, so a fork or a rogue PR can't drain everyone's allocation. You'll leave with a real AI check running on your own repo's pipeline.

## Live Build

- Call a hosted model endpoint from GitHub Actions for automated code review
- Post results back as PR comments
- Secure the runner: store the API token as a repo/environment secret, scope it tightly and set a hard billing boundary, so a fork or rogue PR can't drain the team's budget
- Add automated test/lint gates as harness checks
- Budget control: when to use the small model from Session 3 instead of a frontier API

## Steal This

The draft-PR dependency-and-CVE audit that never merges itself.

## Takeaway

An AI check running on your real repo's pipeline.

## Folder structure

```
session-05-sdlc-cicd/
├── live-demo/           # GitHub Actions workflow and code review script
├── starter-template/    # Blank starting point to follow along
└── participants/        # Submit your own version here (see badges/badge-criteria.md)
```

## Setup

See [`getting-started/`](../../getting-started/) for the general prerequisites. A session-specific setup checklist is posted in [#ai-learning-series](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) the week before.
