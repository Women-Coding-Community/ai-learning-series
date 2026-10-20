# Way 5: One ADK Agent, Four Backends

Quick-start for this folder. Full walkthrough, troubleshooting, and the pre-session checklist live in [`../05-model-router-adk.md`](../05-model-router-adk.md).

## What's here

| File | Purpose |
|---|---|
| `agent.py` | The ~50-line ADK agent. Reads `model_router.yaml` (or a `MODEL_ROUTE` env override) and builds a `LiteLlm` model for every route, Ollama base URL or Vertex AI endpoint alike. |
| `model_router.yaml` | The switch: `default` route name, plus `local` / `docker` / `cloud` / `vertex_gemma` backend definitions. |
| `__init__.py` | Standard ADK package layout, exposes `agent`. |
| `requirements.txt` | `google-adk`, `litellm`, `pyyaml`. |
| `.env.example` | Copy to `.env` and fill in for whichever route you're testing. |

## Install

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Test it

**Fastest sanity check, no live model needed** — confirms the router resolves the right backend and the agent constructs without errors:

```bash
python3 -c "
from agent import root_agent
print(root_agent.name, '->', type(root_agent.model).__name__, getattr(root_agent.model, 'model', root_agent.model))
"
```

**Real run**, needs Way 1's Ollama up (`ollama serve`, with `gemma4:e4b` pulled):

```bash
adk run .                             # uses model_router.yaml's `default` route
MODEL_ROUTE=docker adk run .          # override for one run, see ../02-docker.md
MODEL_ROUTE=cloud adk run .           # needs `ollama signin` from ../03-ollama-cloud-opencode.md
MODEL_ROUTE=vertex_gemma adk run .    # needs Way 4's endpoint deployed and endpoint_id/vertex_project/vertex_location filled in below
```

`adk web .` gives the same thing with a chat UI instead of a terminal REPL.

**Verified:** the local route was run end-to-end against a real local Ollama instance during development of this guide and produced a real response, and the exact `adk run .`/`adk web .` loading path (ADK's `AgentLoader`, not just a hand-rolled script) was confirmed to load `root_agent` correctly from this directory. The `docker` and `cloud` routes were checked for correct construction only, not a live call. The `vertex_gemma` route was added later to match Way 4's fixed-cost Gemma deployment (not a frontier Gemini model), it constructs correctly with a placeholder endpoint ID, but has **not** been tested against a real deployed endpoint, no Way 4 endpoint was running when this was written, and deploying one just to test it would cost real money. Test it yourself against your own Way 4 endpoint before relying on it live.

**Naming note:** this folder is `way5_model_router_adk` (underscores), not `05-model-router-adk` (hyphens) like its guide file. `adk run`/`adk web` load the current directory as a Python module and reject directory names with hyphens (`ValueError: Invalid agent name`). If you ever copy this folder somewhere else, keep the underscore name, or `adk run`/`adk web` will fail the same way.
