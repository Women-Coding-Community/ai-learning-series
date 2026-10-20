"""Run the same review two ways and compare: one agent vs three parallel specialists.

    python3 compare.py                 one run of each
    python3 compare.py --runs 3        average timings over 3 runs
    python3 compare.py --save          also write results/<timestamp>.json

Nothing here is hardcoded: every number comes from the ADK event stream.
"""
import argparse
import asyncio
import datetime
import json
import os
import pathlib
import re
import statistics
import sys
import time
from typing import Optional

from google.adk.agents import BaseAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from common import MODEL, TASK
from fan_out.agent import root_agent as fan_out_agent
from one_agent.agent import root_agent as one_agent_agent

HERE = pathlib.Path(__file__).parent
EXPECTED_PATH = HERE / "fixtures" / "expected.json"

# (label, agent, name of the agent whose final answer is the report)
VARIANTS = [
    ("one_agent", one_agent_agent, "generalist"),
    ("fan_out", fan_out_agent, "synthesiser"),
]


async def run_once(label: str, agent: BaseAgent, report_author: str) -> dict:
    """Run one variant once and return its measurements and final report."""
    service = InMemorySessionService()
    runner = Runner(agent=agent, app_name=label, session_service=service)
    session = await service.create_session(app_name=label, user_id="demo")
    message = types.Content(role="user", parts=[types.Part(text=TASK)])

    llm_calls = prompt_tokens = output_tokens = peak_prompt = 0
    report = ""
    start = time.perf_counter()
    async for event in runner.run_async(user_id="demo", session_id=session.id, new_message=message):
        usage = event.usage_metadata
        if usage and not event.partial:
            llm_calls += 1
            prompt = usage.prompt_token_count or 0
            prompt_tokens += prompt
            output_tokens += usage.candidates_token_count or 0
            peak_prompt = max(peak_prompt, prompt)
        if event.author == report_author and event.is_final_response() and event.content and event.content.parts:
            report = "".join(part.text or "" for part in event.content.parts)
    return {
        "seconds": time.perf_counter() - start,
        "prompt_tokens": prompt_tokens,
        "output_tokens": output_tokens,
        "peak_prompt_tokens": peak_prompt,
        "llm_calls": llm_calls,
        "report": report,
    }


def backend() -> str:
    """Name the model backend in use, for the output."""
    vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "").lower() in ("true", "1")
    return "Vertex AI" if vertex else "Gemini API"


def keyword_hit(keyword: str, text: str) -> bool:
    """A keyword is a case-insensitive substring, or a regex if it starts with 're:'."""
    if keyword.startswith("re:"):
        return re.search(keyword[3:], text, re.IGNORECASE) is not None
    return keyword.lower() in text.lower()


def score(report: str, expected: list) -> dict:
    """Map each planted finding id to True (found) or False (missed)."""
    return {
        finding["id"]: sum(keyword_hit(k, report) for k in finding["keywords"]) >= finding["min_match"]
        for finding in expected
    }


def check_credentials() -> Optional[str]:
    """Return an error message if no model credentials are configured."""
    vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "").lower() in ("true", "1")
    if vertex:
        if os.getenv("GOOGLE_CLOUD_PROJECT"):
            return None
        return "Vertex AI selected but GOOGLE_CLOUD_PROJECT is not set (see .env.example)."
    if os.getenv("GOOGLE_API_KEY"):
        return None
    return ("No credentials. Use Vertex AI (GOOGLE_GENAI_USE_VERTEXAI=True plus GOOGLE_CLOUD_PROJECT) "
            "or set GOOGLE_API_KEY. See .env.example.")


def verdict(results: dict, expected: list) -> str:
    """Plain-English summary computed from the measurements, whatever they show."""
    a, b = results["one_agent"], results["fan_out"]
    total = len(expected)
    found_a = sum(a["found_by_run"][-1].values())
    found_b = sum(b["found_by_run"][-1].values())
    faster = "faster" if b["seconds"] < a["seconds"] else "not faster"
    ratio = b["seconds"] / a["seconds"] if a["seconds"] else 0
    smaller = a["peak_prompt_tokens"] - b["peak_prompt_tokens"]
    return (
        f"one_agent found {found_a}/{total}, fan_out found {found_b}/{total}. "
        f"fan_out was {faster} ({b['seconds']:.1f}s vs {a['seconds']:.1f}s, {ratio:.2f}x). "
        f"Largest single prompt: {a['peak_prompt_tokens']} vs {b['peak_prompt_tokens']} tokens "
        f"({'fan_out smaller by ' + str(smaller) if smaller > 0 else 'fan_out not smaller'}). "
        f"Total prompt tokens: {a['prompt_tokens']} vs {b['prompt_tokens']}."
    )


async def main(runs: int, save: bool) -> int:
    error = check_credentials()
    if error:
        print(error, file=sys.stderr)
        return 2
    if not EXPECTED_PATH.exists():
        print("Fixtures missing. Run: python3 fixtures/make_fixtures.py", file=sys.stderr)
        return 2
    expected = json.loads(EXPECTED_PATH.read_text())

    results = {}
    for label, agent, author in VARIANTS:
        print(f"Running {label} x{runs} on {MODEL} ({backend()}) ...", file=sys.stderr)
        raw = [await run_once(label, agent, author) for _ in range(runs)]
        results[label] = {
            key: statistics.mean(r[key] for r in raw)
            for key in ("seconds", "prompt_tokens", "output_tokens", "peak_prompt_tokens", "llm_calls")
        }
        results[label]["found_by_run"] = [score(r["report"], expected) for r in raw]
        results[label]["report"] = raw[-1]["report"]

    for label, _, _ in VARIANTS:
        print(f"\n===== {label}: final report (last run) =====\n{results[label]['report']}")

    print("\n===== Planted findings (found in how many runs) =====")
    for finding in expected:
        row = [f"{label}: {sum(r[finding['id']] for r in results[label]['found_by_run'])}/{runs}" for label, _, _ in VARIANTS]
        status = ["found" if sum(r[finding['id']] for r in results[l]['found_by_run']) == runs
                  else "missed" if not any(r[finding['id']] for r in results[l]['found_by_run']) else "partial"
                  for l, _, _ in VARIANTS]
        print(f"{finding['id']:<24} " + "   ".join(f"{r} ({s})" for r, s in zip(row, status)))

    print(f"\n===== Comparison (model {MODEL} on {backend()}, average of {runs} run(s)) =====")
    rows = [("seconds", "seconds", ".1f"), ("LLM calls", "llm_calls", ".1f"),
            ("prompt tokens (total)", "prompt_tokens", ".0f"), ("output tokens", "output_tokens", ".0f"),
            ("peak prompt (context pressure)", "peak_prompt_tokens", ".0f")]
    print(f"{'':<32}{'one_agent':>12}{'fan_out':>12}")
    for title, key, fmt in rows:
        print(f"{title:<32}{results['one_agent'][key]:>12{fmt}}{results['fan_out'][key]:>12{fmt}}")
    print(f"{'findings found (last run)':<32}"
          f"{sum(results['one_agent']['found_by_run'][-1].values()):>9}/{len(expected)}"
          f"{sum(results['fan_out']['found_by_run'][-1].values()):>9}/{len(expected)}")
    print("\n" + verdict(results, expected))

    if save:
        out = HERE / "results" / f"{datetime.datetime.now():%Y%m%d-%H%M%S}.json"
        out.write_text(json.dumps({"model": MODEL, "runs": runs, "task": TASK, "results": results}, indent=2))
        print(f"\nSaved {out.relative_to(HERE)}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runs", type=int, default=1, help="runs per variant (timings are averaged)")
    parser.add_argument("--save", action="store_true", help="write results/<timestamp>.json")
    args = parser.parse_args()
    sys.exit(asyncio.run(main(max(1, args.runs), args.save)))
