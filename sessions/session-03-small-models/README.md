# Session 3: Small Models in Practice

**Level:** All levels

## Overview

Bigger isn't always better, and this session proves it. We'll look at why you might self-host a model at all: cost, privacy, and keeping data off third-party APIs. You'll see the trade-offs between running local, in the Cloud, or via Ollama, and learn to spot when a small model is genuinely good enough for the job. The headline that ties back to the whole series: a small model with good Skills can match a much larger model without them, so specialisation does the heavy lifting. By the end you'll have stood up a small model (Gemma on Vertex AI, or Cloud Ollama) and exposed a working endpoint you own, then slotted it straight into the harness we've been building.

## Live Build

- Stand up a small model (e.g. Gemma on Vertex AI, or Cloud Ollama) to avoid third-party API calls
- Expose a working endpoint
- Plug that endpoint into the harness we've been building

**Demo safety net:** a pre-baked, fully deployed backup endpoint stays ready in the wings, in case the live cloud deploy hits latency or a sudden quota wall.

## Steal This

Right-sized models for specialist tasks, fast and cheap.

## Takeaway

Your own model endpoint, slotted into your agent.

## Folder structure

```
session-03-small-models/
├── live-demo/           # Model deployment config and endpoint code
├── starter-template/    # Blank starting point to follow along
└── participants/        # Submit your own version here (see badges/badge-criteria.md)
```

## Setup

See [`getting-started/`](../../getting-started/) for the general prerequisites. A session-specific setup checklist is posted in [#ai-learning-series](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) the week before.
