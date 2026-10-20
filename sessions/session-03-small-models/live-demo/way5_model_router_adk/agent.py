"""Tiny ADK agent that proves the same code runs on four backends.

Which backend it talks to is decided entirely by model_router.yaml, not by
anything in this file. To switch live: edit `default` in that YAML, or
override for one run without touching the file:

    MODEL_ROUTE=docker adk web .
    MODEL_ROUTE=cloud adk web .
    MODEL_ROUTE=vertex_gemma adk web .

See ../05-model-router-adk.md for the full walkthrough.
"""

import os
import pathlib

import yaml
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

ROUTER_PATH = pathlib.Path(__file__).parent / "model_router.yaml"


def _load_route() -> dict:
    router = yaml.safe_load(ROUTER_PATH.read_text())
    route_name = os.environ.get("MODEL_ROUTE", router["default"])
    try:
        return {"name": route_name, **router["providers"][route_name]}
    except KeyError:
        known = ", ".join(router["providers"])
        raise ValueError(f"Unknown MODEL_ROUTE '{route_name}'. Pick one of: {known}")


def _build_model(route: dict):
    if route["kind"] == "vertex_endpoint":
        # Deployed Model Garden endpoint (Way 4), not a native Gemini model.
        return LiteLlm(
            model=f"vertex_ai/{route['endpoint_id']}",
            vertex_project=route["vertex_project"],
            vertex_location=route["vertex_location"],
        )
    if "base_url" in route:
        os.environ["OLLAMA_API_BASE"] = route["base_url"]
    return LiteLlm(model=route["model"])


_route = _load_route()

root_agent = Agent(
    name="router_demo_agent",
    model=_build_model(_route),
    instruction=(
        "You are a terse assistant for a live conference demo. "
        f"You are currently running on the '{_route['name']}' backend: "
        f"{_route['description']}. If asked which model or backend you are "
        "running on, answer plainly using that information."
    ),
    description="Demo agent whose backend is picked by model_router.yaml.",
)
