# Session 3: Small Models in Practice

**Level:** All levels · poll topic B
**Duration:** 60 minutes
**Date:** Tuesday, 15 September 2026, 7:00pm to 8:00pm

## Overview

Bigger isn't always better, and this session proves it, hands-on, across every way you can get a small model running. Session 1 gave the agent a brain (Skills). Session 2 gave it hands and guardrails (MCP, permissions, hooks). Session 3 asks which engine belongs under the bonnet, and as a GDE the focus is squarely on **Gemma**, whichever route you access it through: Google Cloud, Ollama, a container, or a Pixel in your pocket. The rule of thumb we keep coming back to: start every proof of concept on a small model, at no cost, prove the workflow, the Skill, the MCP wiring, and the hooks all work, and only then reach for a bigger, paid model, often only for the parts of the task that actually need it.

## Live Build

Four ways to run Gemma 4, each with a working command ready to paste (see [`live-demo/`](live-demo/) for the full guides):

1. **Download and run locally with Ollama** — zero cost, fully offline
2. **Containerise it with Docker** — same model, portable across machines and CI
3. **Ollama Cloud, called through OpenCode** — no local hardware needed
4. **Deploy your own endpoint on GCP for a fixed cost** — Vertex AI / Cloud Run, plugged into the Session 1/2 harness

**Bonus, time permitting:** Gemma 4 on-device in the Google AI Edge Gallery app on Pixel, using Agent Skills, same `SKILL.md` pattern from Session 1, running fully offline in your pocket.

**Demo safety net:** a pre-baked, fully deployed backup endpoint stays ready in the wings for Way 4, in case the live cloud deploy hits latency or a sudden quota wall.

## Steal This

**Always start your POC on a small model, at no cost.** See the outline's `model_routing.yaml` pattern: every new project starts at `poc` (local Gemma, zero cost), promotes to `validated` (Ollama Cloud or a fixed-cost endpoint) only once proven, and reaches `frontier` only for tasks that genuinely need broader reasoning.

## Takeaway

Your own Gemma endpoint, running at least two of the four ways covered, slotted into your agent, and a POC that started at zero cost.

## Folder structure

```
session-03-small-models/
├── live-demo/            # The four "ways to run Gemma 4" guides, demoed live
│   ├── 01-local-ollama.md
│   ├── 02-docker.md
│   ├── 03-ollama-cloud-opencode.md
│   └── 04-gcp-fixed-cost.md
├── starter-template/     # Blank starting point to follow along
└── participants/         # Submit your own version here (see badges/badge-criteria.md)
```

## Setup

See [`getting-started/`](../../getting-started/) for the general prerequisites. A session-specific setup checklist is posted in [#ai-learning-series](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) the week before.
