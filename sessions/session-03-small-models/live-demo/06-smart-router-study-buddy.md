# Way 6: WCC Study Buddy, a Smart Router for Environment Tier and Task Complexity

**Session:** Harness Series, Session 3, Small Models in Practice
**Cost:** £0/low-cost for dev's ordinary questions, pay-per-token wherever the frontier tutor answers
**Time to test:** ~10 minutes if Way 1 already works

**Presenting this live?** This guide is for setting the folder up and testing each tier yourself. For the actual word-for-word run of show, what to say and type, in order, see [`06-demo-script.md`](06-demo-script.md).

---

## Why This Way

A single ADK agent that answers the question that actually matters in production: **how do you decide, automatically, which backend answers a given request, and how do you know which one just did?**

Two independent decisions, composed:

1. **Environment tier**, which backend answers an *ordinary* question by default. Three tiers, deliberately kept simple: `dev` defaults to the free local Gemma 4, `staging` and `prod` both default straight to the frontier model, Gemini, because from staging on you want to be talking to the exact backend prod will use, not a cheaper stand-in, and there's no laptop-hosted Ollama server behind a production deployment either.
2. **Task complexity**, regardless of environment, a hard question (a proof, a derivation, a system-design trade-off) escalates to the frontier model. Same rule everywhere, in every tier, a genuinely hard question always ends up at the frontier model, `dev` just has further to travel to get there, since `staging` and `prod` are already standing on it.

In `staging` and `prod`, those two axes collapse into one: the default is already the frontier model, so "escalation" doesn't change anything. That's intentional, not a bug: cheap and fast in dev, locked onto the real target model the moment staging starts.

The whole thing is built on a single ADK `BaseAgent` subclass, `StudyBuddyRouter`, wrapping two `Agent` instances named `wcc_tutor_primary` and `wcc_tutor_frontier`. It routes deterministically (a plain heuristic on the question text), not via an LLM's own judgement call, on purpose, see Step 2. Every final reply is also tagged with which model actually answered, right in the chat itself, not just in a server log, see Step 3.

**WCC Study Buddy, and where the persona comes from:** the tutor's guide-with-a-question, never-hand-over-the-answer approach is inspired by [leslysandra/socratic-study-buddy-gemma4](https://github.com/leslysandra/socratic-study-buddy-gemma4), a local-first Socratic tutor built for the Gemma 4 challenge. This way renames it WCC Study Buddy, keeps that same approach, and adds the environment/complexity router on top.

---

## Prerequisites

- Way 1 (local Ollama with `gemma4:e4b`) working
- For any escalation, or `staging`/`prod`: a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey), or a GCP project with Vertex AI enabled and Application Default Credentials set up for it (see `.env.example`)
- Python 3.10+

---

## Step 1: Install Dependencies

```bash
cd sessions/session-03-small-models/live-demo/way6_smart_router_study_buddy
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env: set APP_ENV, and paste GOOGLE_API_KEY (or the Vertex block)
```

---

## Step 2: Read the Router Before You Run It

`model_routing.yaml` sets the default backend per tier, three tiers on purpose, not a full delivery pipeline's worth:

```yaml
environments:
  dev:     { default: local }      # free/low-cost, escalates on complexity
  staging: { default: frontier }   # locks onto the real target model
  prod:    { default: frontier }   # same as staging, that repetition is the point
```

`complexity.py` is a plain word/pattern heuristic, deliberately **not** another model call:

```python
COMPLEX_SIGNALS = [r"\bprove\b", r"\bderive\b", r"\btime complexity\b", ...]

def classify(question: str) -> str:
    ...
    return "complex" if hits or word_count > 40 else "simple"
```

Note: asking a small local model to grade its own question's difficulty would make the classifier itself non-deterministic. A plain heuristic is deterministic and transparent instead, the same input always classifies the same way.

`agent.py`'s `StudyBuddyRouter._run_async_impl` ties them together: it pulls the latest user message out of `ctx.session.events`, classifies it, decides `primary` vs `frontier`, prints the decision, and runs the chosen sub-agent:

```python
verdict = classify(question)
escalate = verdict == "complex" and not self.primary_is_frontier
chosen = self.frontier if escalate else self.primary
print(f">>> ROUTER  env={_env_name}  complexity={verdict}  -> '{chosen.name}' ({label})")
```

That `print` only shows up in the terminal running `adk run`/`adk web`, not in `adk web`'s own chat UI. Step 3 covers how the routing decision is also surfaced there.

---

## Step 3: The Model Answers, and Says So

Every final reply gets a footer appended before it's yielded, done inside `_run_async_impl` by finding the true final response event (`event.is_final_response()`, ADK's own documented helper for exactly this, not a guess) and appending to its last text part, so it never touches the model's own thinking-scratchpad text if there is one:

```python
async for event in chosen.run_async(ctx):
    if event.is_final_response() and event.content and event.content.parts:
        for part in reversed(event.content.parts):
            if part.text:
                part.text += f"\n\n_(answered by: {label})_"
                break
    yield event
```

That means a real answer now ends with something like:

```
_(answered by: ollama_chat/gemma4:e4b · env=dev)_
```

or, once escalated or in a frontier-default tier:

```
_(answered by: gemini-3-flash-preview · frontier)_
```

This is visible directly in `adk web`'s chat UI, not just a terminal running `adk run`.

---

## Step 4: Dev Tier, Watch It Stay Local, Then Escalate

```bash
APP_ENV=dev adk run .
```

Ask an easy question first:

```
How do binary search trees find things faster than arrays?
```

Terminal shows `complexity=simple -> 'wcc_tutor_primary'`, answered by local Gemma 4, guiding with a question, no cost, and the reply itself ends `_(answered by: ollama_chat/gemma4:e4b · env=dev)_`.

Now ask a hard one:

```
Can you prove why merge sort is O(n log n) and derive the recurrence?
```

Terminal shows `complexity=complex -> 'wcc_tutor_frontier'`, same dev tier, same £0 default, but this turn was answered by Gemini, footer confirms it: `_(answered by: gemini-3-flash-preview · frontier)_`.

---

## Step 5: Staging Onward, Always Frontier

```bash
APP_ENV=staging adk run .
```

Ask the same easy question again:

```
How do binary search trees find things faster than arrays?
```

Terminal shows `complexity=simple -> 'wcc_tutor_primary'`, but `wcc_tutor_primary` is now Gemini, because `staging`'s default backend is `frontier`, footer confirms: `_(answered by: gemini-3-flash-preview · env=staging)_`. Now ask the hard question:

```
Can you prove why merge sort is O(n log n) and derive the recurrence?
```

Terminal shows `complexity=complex -> 'wcc_tutor_primary'  (already frontier by default in this env, escalation is a no-op)`. Nothing changed, both turns were already answered by Gemini. `prod` behaves identically, same `default: frontier`, same collapse. Summary of the two-axis behaviour: environment tier sets the default backend, complexity only overrides that default when the default isn't already the frontier model.

---

## Step 6: Optional, Try the Web UI

```bash
adk web .
```

Same routing, now with a chat UI. The `_(answered by: ...)_` footer appears directly in the chat bubble, no terminal needed to see which model answered.

---

## Troubleshooting

**Router always answers with the local tutor, even on hard questions:** check `_last_user_text` is finding your message, run with `APP_ENV=dev adk run .` (not `adk web .`) first so you can watch stdout directly. If it's still empty, print `ctx.session.events` inside `_run_async_impl` once to see the actual event shape, ADK's internal event structure has shifted across versions before, and this is the one part of this demo that depends on it.

**No footer on the reply, or it's attached to the thinking text instead of the real answer:** check `event.is_final_response()` is actually being hit only once per real answer in your ADK version, print `event.is_final_response()` and `event.partial` for every event once to see the actual shape if this looks wrong, it was verified against a real Ollama run during development but ADK's event semantics could shift across versions.

**`gemini` turns 404:** a location issue, not a bad model name, try `GOOGLE_CLOUD_LOCATION=global` if you're on Vertex, and confirm `GOOGLE_GENAI_USE_VERTEXAI`/`GOOGLE_CLOUD_PROJECT` are actually set in the shell running `adk`, not just in `.env` if something isn't loading it.

**Everything escalates, even simple questions:** check `complexity.py`'s word-count threshold isn't being hit by a long-winded phrasing. The example questions above are tuned to sit clearly on either side of it; test any of your own questions before relying on them.

**`adk run .` / `adk web .` can't find `root_agent`:** run it from inside `way6_smart_router_study_buddy/`, not the repo root.

**`ValueError: Invalid agent name` / `Invalid app name`:** `adk run`/`adk web` load the current directory as a Python module, so it has to pass two separate checks: no hyphens (`AgentLoader`'s import-name check), and it must *start with a letter* (a second, stricter check when it wraps the agent in an `App`, digit-leading names like `06_...` pass the first check but fail this one). Effectively the directory name needs to be a real Python identifier. That's why this folder is `way6_smart_router_study_buddy`, not `06-smart-router-study-buddy` (hyphens) or `06_smart_router_study_buddy` (leading digit), even though the guide file next to it keeps the numbered, hyphenated name.

---

## What "Good" Looks Like Before the Session

- [ ] `APP_ENV=dev adk run .` answers an easy question locally, and a hard one via Gemini, with a clear `>>> ROUTER` line and a matching `_(answered by: ...)_` footer each time
- [ ] `APP_ENV=staging adk run .` (or `prod`) answers *both* questions via Gemini, with the "already frontier, no-op" note on the hard one
- [ ] You've rehearsed both example questions (or your own) enough times to know which way they classify
- [ ] `.env` is filled in and the frontier tutor responds without a 404
- [ ] `adk web .` shows the `_(answered by: ...)_` footer in the chat UI itself, not just in your terminal
- [ ] You can explain the two axes (environment = cost posture, complexity = per-question override) in one breath before you even run the demo

If all six are ticked, you're ready for this segment of the live demo.
