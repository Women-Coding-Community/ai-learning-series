"""Same WCC Study Buddy persona as Way 6, with zero routing logic left in
this file. Which backend actually answers is decided entirely by the
Inference Gateway's ../routing.yaml, not by anything here, this file only
ever talks to one place: the gateway's OpenAI-compatible endpoint.

Point this at whichever alias you want to demo, from ../routing.yaml:
    GATEWAY_MODEL_ALIAS=poc-tutor   adk web .   # Ways 1/2, local, £0
    GATEWAY_MODEL_ALIAS=cloud-tutor adk web .   # Way 3, Ollama Cloud
    GATEWAY_MODEL_ALIAS=prod-tutor  adk web .   # Way 4's territory, Gemini

See ../../07-inference-gateway-routing.md for the full walkthrough.
"""

import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

GATEWAY_URL = os.environ.get("GATEWAY_URL", "http://localhost:8080/v1")
MODEL_ALIAS = os.environ.get("GATEWAY_MODEL_ALIAS", "poc-tutor")

TUTOR_INSTRUCTION = """You are WCC Study Buddy. Guide the student to the \
answer themselves, never hand it over directly.

1. Never give the final answer, solution, or a complete working code block.
2. Work out what concept the student is missing, then give one short \
analogy or nudge followed by exactly one open-ended guiding question.
3. Keep it brief: a couple of sentences plus the question.
4. Reply in the same language the student used."""

root_agent = Agent(
    name="gateway_routed_tutor",
    model=LiteLlm(
        model=f"openai/{MODEL_ALIAS}",
        api_base=GATEWAY_URL,
        api_key=os.environ.get("GATEWAY_API_KEY", "not-required-without-gateway-auth"),
    ),
    instruction=TUTOR_INSTRUCTION,
    description="WCC Study Buddy tutor whose backend is resolved by the gateway's routing.yaml, not by this code.",
)
