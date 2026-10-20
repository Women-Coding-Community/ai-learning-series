# Way 5: One ADK Agent, Four Backends, Switched by a Router YAML

**Session:** Harness Series, Session 3, Small Models in Practice
**Cost:** £0 for local/docker/cloud, hourly regardless of traffic for `vertex_gemma` (only once that endpoint is deployed and running, see Way 4)
**Time to test:** ~10 minutes if Ways 1 to 3 are already set up

**Presenting this live?** This guide is for setting the folder up and testing each route yourself. For the actual word-for-word run of show, what to say and type, in order, see [`05-demo-script.md`](05-demo-script.md).

---

## Why This Way

Ways 1 to 4 each stood up a backend. This one is the payoff: a single tiny ADK agent (`agent.py`, ~40 lines) that never changes, pointed at a different backend purely by editing one YAML file. It's the concrete answer to "how do I actually swap models without rewriting my agent?" that ties the whole session together.

The trick is `model_router.yaml`: a `default` route name plus a `providers` map. `agent.py` reads it once at import time, resolves every route through LiteLLM, whether that's Ollama's OpenAI-compatible API or a deployed Vertex AI endpoint, and bakes the active route's name into the agent's own instruction, so you can just ask it which backend it's on. Same agent, same prompt, four completely different places actually answering: your laptop, a container, Ollama's cloud, or your own Vertex AI endpoint.

---

## Prerequisites

- Way 1 (local Ollama) working, ideally Way 2 (Docker) and Way 3 (Ollama Cloud) too, this guide reuses all three
- Python 3.10+ and a virtual environment tool of your choice
- For the `vertex_gemma` route: Way 4's Gemma 4 endpoint already deployed on Vertex AI (deploy it well before the session, per Way 4's own safety notes, this route needs it running and billing by the hour)

---

## Step 1: Install Dependencies

```bash
cd sessions/session-03-small-models/live-demo/way5_model_router_adk
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

---

## Step 2: Look at the Two Files That Matter

`model_router.yaml` is the whole switch:

```yaml
default: local

providers:
  local:
    kind: ollama
    model: ollama_chat/gemma4:e4b
    base_url: http://localhost:11434
  docker:
    kind: ollama
    model: ollama_chat/gemma4:e4b
    base_url: http://localhost:11434
  cloud:
    kind: ollama
    model: ollama_chat/gemma4:cloud
    base_url: https://ollama.com
  vertex_gemma:
    kind: vertex_endpoint
    endpoint_id: "YOUR_ENDPOINT_ID"      # from Way 4's `gcloud ai endpoints list`
    vertex_project: "your-project-id"
    vertex_location: "us-central1"
```

`agent.py` reads `default` (or a `MODEL_ROUTE` env var override) and builds a `LiteLlm` model either way, Ollama routes point it at a base URL, the `vertex_endpoint` route points it at `vertex_ai/{endpoint_id}` with the project and region, and that's the entire routing logic, no branching anywhere else in the file.

**Not yet verified against a real deployed endpoint:** the `vertex_ai/{ENDPOINT_ID}` model string is LiteLLM's documented pattern for a non-Gemini Vertex AI Model Garden deployment, but it hasn't been tested here against an actual running Way 4 endpoint (deploying one costs real money, see Way 4's safety notes). Do a real dry run against your own deployed endpoint before relying on this route live, and if the model string turns out to need adjusting, that's a one-line change in `_build_model` in `agent.py`.

---

## Step 3: Run It Against Local Ollama (Way 1)

Make sure Way 1's `ollama run gemma4:e4b` (or at least `ollama serve`) is up, then:

```bash
adk web .
```

Open the local URL it prints, pick `router_demo_agent`, and ask:

```
Which backend are you running on right now?
```

It should answer `local`, and the description from the YAML.

---

## Step 4: Flip to Docker, No Code Change (Way 2)

Way 2's container also listens on `:11434`, so the `docker` route in the YAML is identical to `local`, that's deliberate, it's the point: from the agent's point of view, "local Ollama" and "Ollama in a container" are the same backend.

```bash
# with Way 2's container running instead of native ollama
MODEL_ROUTE=docker adk web .
```

Ask the same question, same answer shape, different route name.

---

## Step 5: Flip to Ollama Cloud (Way 3)

Requires `ollama signin` from Way 3 to already be done.

```bash
MODEL_ROUTE=cloud adk web .
```

Same prompt again. This time there's no local GPU or container involved at all, just the cloud route's `base_url`.

---

## Step 6: Flip to Your Vertex AI Gemma Endpoint (Way 4)

Fill in `model_router.yaml`'s `vertex_gemma` block with the real `endpoint_id`, `vertex_project`, and `vertex_location` from Way 4's deployment (`gcloud ai endpoints list`), or set them via env vars if you'd rather not hardcode them in the YAML for a shared repo.

```bash
MODEL_ROUTE=vertex_gemma adk web .
```

Same prompt, same agent code, now answered by your own dedicated GPU-backed endpoint instead of a shared free tier. This is the moment to talk about the cost model shift: local/docker/cloud are all £0 or usage-capped, this one bills a fixed hourly rate the moment it's deployed, whatever your traffic looks like. That's the trade worth making once you have predictable, real traffic, not before.

---

## Step 7: Make It the Live Default

For the session itself, set whichever route you're demonstrating as `default` in `model_router.yaml` directly, so you're not typing `MODEL_ROUTE=` on stage, just editing one line and restarting `adk web .`.

---

## Troubleshooting

**`ValueError: Unknown MODEL_ROUTE`:** typo in the env var, check it matches a key under `providers:` in `model_router.yaml` exactly.

**`local`/`docker` routes hang or error connecting:** the relevant Ollama instance (native or container) isn't actually running, or something else already took port 11434, see Way 1 / Way 2 troubleshooting.

**`cloud` route says unauthorized:** `ollama signin` has expired or wasn't run in this environment, re-run it (Way 3, Step 4).

**`vertex_gemma` route errors or 404s:** confirm the endpoint is actually deployed and shows `READY` in `gcloud ai endpoints list` (Way 4), and that `vertex_project`/`vertex_location` in `model_router.yaml` match where you deployed it. If the request shape itself is wrong (not just a 404), the `vertex_ai/{ENDPOINT_ID}` LiteLLM pattern may need adjusting for your specific deployment, check `_build_model` in `agent.py`.

**`adk web .` can't find `root_agent`:** run it from inside `way5_model_router_adk/`, not the repo root, `adk web` expects the agent package as the current directory.

**`ValueError: Invalid agent name` / `Invalid app name`:** `adk run`/`adk web` load the current directory as a Python module, so it has to pass two separate checks: no hyphens (`AgentLoader`'s import-name check), and it must *start with a letter* (a second, stricter check when it wraps the agent in an `App`, digit-leading names like `05_...` pass the first check but fail this one). Effectively the directory name needs to be a real Python identifier. That's why this folder is `way5_model_router_adk`, not `05-model-router-adk` (hyphens) or `05_model_router_adk` (leading digit), even though the guide file next to it keeps the numbered, hyphenated name.

---

## What "Good" Looks Like Before the Session

- [ ] `adk web .` starts cleanly with the `local` default and the agent correctly names its own backend
- [ ] `MODEL_ROUTE=docker adk web .` works with Way 2's container running
- [ ] `MODEL_ROUTE=cloud adk web .` works with Way 3's sign-in already done
- [ ] Way 4's endpoint is deployed and `MODEL_ROUTE=vertex_gemma adk web .` gets a real response
- [ ] You've rehearsed the four-question sequence ("which backend are you on?") so the flip is smooth live

If all five are ticked, you're ready for this segment of the live demo.
