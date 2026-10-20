# Way 7: Gateway-Level Routing — What Production Teams Actually Use

**Session:** Harness Series, Session 3, Small Models in Practice
**Cost:** £0 for the gateway itself, whatever the resolved backend costs per call
**Time to test:** ~15 minutes if Ways 1 and 3 are already working

---

## Why This Way, and Why It's Different from Ways 5 and 6

Ways 5 and 6 put the routing decision **inside the agent's Python** (a YAML file the code reads, or a custom `BaseAgent` router). That's a fine place for it in a demo, but it means every app that wants to switch backends has to carry that logic itself, in whatever language it's written in, and needs a redeploy to change providers.

What teams running this at real scale tend to do instead is push routing **out of the app and into a gateway**: a small proxy that speaks one OpenAI-compatible API, sits in front of every provider, and resolves a *logical model name* to a real `provider/model` pair via its own config, config that ops owns, not the app team. The app never touches provider SDKs, API keys, or `if env == "prod"` branches, it just calls the gateway and asks for `"the tutor model"`.

This way rebuilds Way 6's WCC Study Buddy tutor on top of exactly that pattern, using a real open-source example: [Inference Gateway](https://github.com/inference-gateway/inference-gateway)'s own [`routing.yaml`](https://github.com/inference-gateway/inference-gateway/blob/main/examples/routing.yaml) format, pointed at this session's actual backends (Ways 1 to 4) instead of the project's own example providers.

**Why it's worth the extra segment:** a vendor writeup on this exact problem ([Inworld AI, "AI model routing for cost reduction"](https://inworld.ai/resources/ai-model-routing-cost-reduction)) puts numbers on why teams bother: they estimate **70 to 80% of subtasks** in a typical conversational AI turn can run on a small model instead of a frontier one, small models can run **10 to 20x cheaper per token**, and they cite an **80 to 95% aggregate cost reduction** at scale from routing well. Treat those as one vendor's estimates, not a peer-reviewed benchmark, but they're the right order of magnitude to explain why "just always call the frontier model" stops being an option once you have real traffic.

---

## Important Caveat, Say This Out Loud

Inference Gateway's routing config is **Phase 1**: the only strategy is `round_robin`, load-balancing across a pool of *interchangeable* deployments for redundancy and throughput. It does **not** do complexity-aware routing, there's no built-in "if this looks hard, send it to the bigger model." That decision still has to be made somewhere upstream of the gateway, which is exactly what Way 6's heuristic does. The two ways are complementary, not competing:

- **Way 6 decides *which alias to call*** (complexity, environment, whatever your app logic needs).
- **Way 7 (this one) decides *what's actually behind that alias*** (which provider, which region, load-balanced across how many deployments), without the app knowing or caring.

---

## Prerequisites

- Way 1 (local Ollama) and ideally Way 3 (Ollama Cloud signed in) already working
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey) (or Way 4's Vertex project)
- Docker, or a Linux/macOS/Windows machine to run the standalone `inference-gateway` binary

---

## Step 1: Install and Configure the Gateway

```bash
cd sessions/session-03-small-models/live-demo/way7-inference-gateway-routing
curl -fsSL https://raw.githubusercontent.com/inference-gateway/inference-gateway/main/install.sh | bash
cp .env.example .env
# edit .env: paste GOOGLE_API_KEY, and OLLAMA_CLOUD_API_KEY if you signed in for Way 3
```

`.env` also sets `ROUTING_ENABLED=true` and points `ROUTING_CONFIG_PATH` at this folder's `routing.yaml`, that's what turns on the alias-based routing below instead of plain `provider/model` passthrough.

---

## Step 2: Look at `routing.yaml`

```yaml
models:
  poc-tutor:
    deployments:
      - provider: ollama
        model: gemma4:e4b
  cloud-tutor:
    deployments:
      - provider: ollama-cloud
        model: gemma4:cloud
  prod-tutor:
    deployments:
      - provider: google
        model: gemini-3-flash-preview
  resilient-tutor:
    strategy: round_robin
    deployments:
      - provider: ollama
        model: gemma4:e4b
      - provider: ollama-cloud
        model: gemma4:cloud
```

Three aliases map one-to-one onto Ways 1/2, 3, and 4. The fourth, `resilient-tutor`, is the bonus case that `round_robin` is actually built for: two equivalent deployments load-balanced for redundancy, not one "smart" and one "dumb" deployment picked by difficulty.

---

## Step 3: Start the Gateway and Prove the Unification

```bash
export $(cat .env | grep -v '^#' | xargs)
inference-gateway &
```

With native Ollama (Way 1) already running, call the local alias:

```bash
curl -s http://localhost:8080/v1/chat/completions -d '{
  "model": "poc-tutor",
  "messages": [{"role": "user", "content": "Say hello in one sentence."}]
}' | jq '.choices[0].message.content'
```

Now call the prod alias, same endpoint, same request shape, different backend entirely:

```bash
curl -s http://localhost:8080/v1/chat/completions -d '{
  "model": "prod-tutor",
  "messages": [{"role": "user", "content": "Say hello in one sentence."}]
}' | jq '.choices[0].message.content'
```

That's the whole pitch in two `curl` calls: identical client code, the only thing that changed is a string.

---

## Step 4: Point the ADK Agent at the Gateway Instead of a Provider

```bash
cd agent
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Open [`agent/agent.py`](way7-inference-gateway-routing/agent/agent.py) and compare it to Way 6's `agent.py`: there's no `model_routing.yaml`, no per-provider `LiteLlm`/`Gemini` branching, no `_build_model`. It just does this:

```python
root_agent = Agent(
    name="gateway_routed_tutor",
    model=LiteLlm(
        model=f"openai/{MODEL_ALIAS}",
        api_base=GATEWAY_URL,
        api_key=os.environ.get("GATEWAY_API_KEY", "not-required-without-gateway-auth"),
    ),
    instruction=SOCRATIC_INSTRUCTION,
)
```

`openai/<alias>` tells LiteLLM to treat the gateway as a plain OpenAI-compatible endpoint, the alias is resolved entirely server-side. All the routing intelligence from Way 5 and Way 6 moved out of this file.

Run it against each alias:

```bash
GATEWAY_MODEL_ALIAS=poc-tutor   adk run .   # Ways 1/2, £0
GATEWAY_MODEL_ALIAS=cloud-tutor adk run .   # Way 3
GATEWAY_MODEL_ALIAS=prod-tutor  adk run .   # Way 4's territory, Gemini
```

---

## Step 5: The Live Comparison

Ask the exact same question against `poc-tutor` and `prod-tutor` back to back:

```
I don't understand how binary search trees find things faster than arrays.
```

Same WCC Study Buddy persona both times, different depth and phrasing underneath, and neither the app code nor the person asking had to know which provider actually answered. That's the demo: routing as an infrastructure concern, invisible to the app, changeable without a redeploy.

---

## Troubleshooting

**`inference-gateway: command not found`:** the install script installs to `/usr/local/bin` by default, open a new terminal or check that directory is on your `PATH`.

**Gateway starts but `poc-tutor` 404s or times out:** confirm native/Docker Ollama (Way 1/2) is actually running on `:11434` and `OLLAMA_API_URL` in `.env` points at it with `/v1` on the end.

**`cloud-tutor` unauthorized:** `OLLAMA_CLOUD_API_KEY` isn't set, or Way 3's `ollama signin` has expired.

**`prod-tutor` 404s:** a Gemini API key or endpoint issue, not a routing.yaml problem, confirm `GOOGLE_API_KEY` is set and test that alias in isolation with the `curl` from Step 3.

**Not sure `ollama-cloud` is the exact provider key:** list what the gateway sees with `curl http://localhost:8080/v1/models?provider=ollama-cloud | jq`, provider keys can shift between gateway versions, don't trust this guide over what the running gateway actually reports.

**Agent gets a connection refused on `:8080`:** the gateway isn't running, or `GATEWAY_URL` in the agent's shell doesn't match where you started it.

---

## What "Good" Looks Like Before the Session

- [ ] The gateway starts cleanly with `ROUTING_ENABLED=true` and this folder's `routing.yaml`
- [ ] Both `curl` calls in Step 3 (`poc-tutor` and `prod-tutor`) return real completions from two different backends
- [ ] `GATEWAY_MODEL_ALIAS=poc-tutor adk run .` and `GATEWAY_MODEL_ALIAS=prod-tutor adk run .` both work from the `agent/` folder
- [ ] You've rehearsed the one-question, two-alias comparison in Step 5
- [ ] You can explain in one breath why this is different from Way 6 (app decides *which alias*, gateway decides *what's behind it*), and that the gateway itself doesn't do complexity-aware routing yet

If all five are ticked, you're ready for this segment of the live demo.
