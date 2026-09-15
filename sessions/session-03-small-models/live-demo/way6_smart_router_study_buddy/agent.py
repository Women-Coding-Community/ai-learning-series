"""WCC Study Buddy with a two-axis model router.

Axis 1 -- environment tier (model_routing.yaml): decides which backend
answers an ordinary question by default. dev defaults to the free local
Gemma 4 (no/low-cost dev); staging and prod default straight to the frontier
model, since from staging onward you want to be talking to the exact
backend prod will use, no local Ollama server behind it to fall back to.

Axis 2 -- task complexity (complexity.py): independent of environment, a
deterministic heuristic on the question text decides whether to escalate to
the frontier tutor even when the environment default is the small model.
Same rule in every tier, a genuinely hard question always ends up at the
frontier model, dev just has further to travel to reach it. In staging and
prod the two axes collapse: the default is already the frontier model, so
escalation is a visible no-op. That collapse is itself the point, see
../06-smart-router-study-buddy.md.

Every final reply is tagged with which model actually answered (see
`_MODEL_LABELS` and `_run_async_impl` below), visible in the chat itself,
not just on stdout, so it shows up in `adk web`'s UI too.

Inspired by leslysandra/socratic-study-buddy-gemma4's local-first tutor, renamed
WCC Study Buddy here:
https://github.com/leslysandra/socratic-study-buddy-gemma4
"""

import os
import pathlib
from typing import AsyncGenerator

import yaml
from google.adk.agents import Agent, BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.models.lite_llm import LiteLlm

from .complexity import classify

HERE = pathlib.Path(__file__).parent
ENV_CONFIG_PATH = HERE / "model_routing.yaml"
TUTOR_INSTRUCTION = (HERE / "config" / "system_prompt.txt").read_text()


def _load_config() -> dict:
    return yaml.safe_load(ENV_CONFIG_PATH.read_text())


def _build_model(backend: dict):
    if backend["kind"] == "gemini":
        return backend["model"]  # native Gemini, resolved by google-genai directly
    os.environ["OLLAMA_API_BASE"] = backend["base_url"]
    return LiteLlm(model=backend["model"])


def _last_user_text(ctx: InvocationContext) -> str:
    """Pulls the most recent user turn straight out of session history.

    Reading `ctx.session.events` rather than a request-scoped shortcut is
    deliberate: session events are ADK's stable, documented record of the
    conversation, so this keeps working regardless of how the surrounding
    LLM flow assembles its own request.
    """
    for event in reversed(ctx.session.events):
        if event.author == "user" and event.content and event.content.parts:
            return "".join(part.text or "" for part in event.content.parts)
    return ""


_config = _load_config()
_env_name = os.environ.get("APP_ENV", _config["default_env"])
_env = _config["environments"][_env_name]
_default_backend = _config["backends"][_env["default"]]
_frontier_backend = _config["backends"]["frontier"]

primary_tutor = Agent(
    name="wcc_tutor_primary",
    model=_build_model(_default_backend),
    instruction=TUTOR_INSTRUCTION,
    description="Default WCC Study Buddy tutor for this environment tier.",
)

frontier_tutor = Agent(
    name="wcc_tutor_frontier",
    model=_build_model(_frontier_backend),
    instruction=(
        TUTOR_INSTRUCTION
        + "\n\nThis question was flagged as genuinely hard (a proof, a "
        "derivation, a system design trade-off). You may reason through "
        "more of the structure than usual, but you still guide with a "
        "question at the end, you never just hand over the final answer."
    ),
    description="Frontier tutor for questions that need deeper reasoning.",
)

# Shown to the audience inside the actual reply, not just on stdout, so it's
# visible in `adk web`'s UI too, not only a terminal running `adk run`.
_MODEL_LABELS = {
    primary_tutor.name: f"{_default_backend['model']} · env={_env_name}",
    frontier_tutor.name: f"{_frontier_backend['model']} · frontier",
}


class StudyBuddyRouter(BaseAgent):
    """Deterministically picks the primary or frontier tutor per question."""

    primary: Agent
    frontier: Agent
    primary_is_frontier: bool

    model_config = {"arbitrary_types_allowed": True}

    def __init__(self, name: str, primary: Agent, frontier: Agent, primary_is_frontier: bool):
        super().__init__(
            name=name,
            primary=primary,
            frontier=frontier,
            primary_is_frontier=primary_is_frontier,
            sub_agents=[primary, frontier],
        )

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        question = _last_user_text(ctx)
        verdict = classify(question)
        escalate = verdict == "complex" and not self.primary_is_frontier
        chosen = self.frontier if escalate else self.primary
        label = _MODEL_LABELS[chosen.name]

        note = ""
        if verdict == "complex" and self.primary_is_frontier:
            note = "  (already frontier by default in this env, escalation is a no-op)"

        print(f"\n>>> ROUTER  env={_env_name}  complexity={verdict}  -> '{chosen.name}' ({label}){note}\n")

        ctx.session.state["routed_to"] = chosen.name
        ctx.session.state["complexity_verdict"] = verdict

        async for event in chosen.run_async(ctx):
            if event.is_final_response() and event.content and event.content.parts:
                for part in reversed(event.content.parts):
                    if part.text:
                        part.text += f"\n\n_(answered by: {label})_"
                        break
            yield event


root_agent = StudyBuddyRouter(
    name="study_buddy_router",
    primary=primary_tutor,
    frontier=frontier_tutor,
    primary_is_frontier=(_env["default"] == "frontier"),
)
