# Way 7: Gateway-Level Routing

Quick-start for this folder. Full walkthrough (including the real-world cost-reduction numbers this segment opens with, and the honest caveat about what the gateway's routing does and doesn't do), troubleshooting, and the pre-session checklist live in [`../07-inference-gateway-routing.md`](../07-inference-gateway-routing.md).

## What's here

This folder has two independent halves, deliberately kept apart, that's the whole point of this way:

| Path | Owned by | Purpose |
|---|---|---|
| `routing.yaml` | "Ops" | Logical aliases (`poc-tutor`, `cloud-tutor`, `prod-tutor`, `resilient-tutor`) mapped to real `provider/model` pairs. Config for the [Inference Gateway](https://github.com/inference-gateway/inference-gateway) binary. |
| `.env.example` | "Ops" | Provider URLs/keys for the gateway itself (`OLLAMA_API_URL`, `OLLAMA_CLOUD_API_URL`, `GOOGLE_API_URL`, etc.), plus `ROUTING_ENABLED`/`ROUTING_CONFIG_PATH`. |
| `agent/agent.py` | "App" | The ADK agent. Knows nothing about providers, only calls one alias against the gateway's OpenAI-compatible endpoint. |
| `agent/requirements.txt` | "App" | `google-adk`, `litellm`. |

## Install

**The gateway:**

```bash
curl -fsSL https://raw.githubusercontent.com/inference-gateway/inference-gateway/main/install.sh | bash
cp .env.example .env   # fill in GOOGLE_API_KEY, OLLAMA_CLOUD_API_KEY if using cloud-tutor
```

**The agent:**

```bash
cd agent
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Test it

**Fastest sanity check, no live gateway needed** — confirms the agent constructs and is pointed at the right alias/URL (from `agent/`):

```bash
python3 -c "
from agent import root_agent
m = root_agent.model
print(root_agent.name, '->', m.model, '@', m._additional_args.get('api_base'))
"
```

**Prove the gateway unifies providers**, with the gateway running (`export \$(cat .env | grep -v '^#' | xargs); inference-gateway &`) and Way 1's Ollama up:

```bash
curl -s http://localhost:8080/v1/chat/completions -d '{
  "model": "poc-tutor",
  "messages": [{"role": "user", "content": "Say hello in one sentence."}]
}' | jq '.choices[0].message.content'
```

**Real agent run**, from `agent/`:

```bash
GATEWAY_MODEL_ALIAS=poc-tutor adk run .
```

**Verified:** the agent's construction and the `LiteLlm(model="openai/poc-tutor", api_base=..., ...)` wiring were confirmed correct (see `_additional_args` above). The gateway binary itself, the live `curl` calls, and the `cloud-tutor`/`prod-tutor`/`resilient-tutor` aliases were **not** tested end-to-end, this way needs a separate binary install and real provider credentials this environment didn't have. Budget real setup time for this one before the session, more than Ways 5 or 6.
