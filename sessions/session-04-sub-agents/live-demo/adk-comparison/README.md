# Session 4 ADK demo: one agent vs three specialists

Runs the same review task two ways in Google ADK and prints a side-by-side comparison.

- **one_agent**: a single `LlmAgent` does security review, test triage and docs check in one context window.
- **fan_out**: three narrow `LlmAgent`s run in a `ParallelAgent`, then a `synthesiser` merges their findings.

Task for both: "Review this branch: security issues, real test failures, README drift. Return one report."

## What it shows

The fixture is a small repo, `fixtures/shipit/`, with planted problems: a hardcoded fake secret and an f-string SQL query in `app/payments.py`, two real test failures buried in a 1,500 line `tests/output.log`, and two README drifts (amount in pounds, retries default 5). `fixtures/expected.json` lists them as ground truth. It sits outside `shipit/` so an agent opened there cannot read the answers.

## Run it

```bash
cd sessions/session-04-sub-agents/live-demo/adk-comparison
python3.13 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env              # Vertex AI block is the default; set your project id
python3 fixtures/make_fixtures.py # regenerate fixtures (deterministic)
pytest                            # offline tests, no API key needed
python3 compare.py                # --runs 3 to average timings, --save to write results/
adk web                           # run from this folder, pick one_agent or fan_out
```

Python 3.14 currently fails to install ADK's `watchdog` dependency on macOS; use 3.13.

## Model backend

Vertex AI is the default in `.env.example`: set `GOOGLE_GENAI_USE_VERTEXAI=True`, `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`, and sign in once with `gcloud auth application-default login`. To use an AI Studio key instead, set `GOOGLE_GENAI_USE_VERTEXAI=False` and `GOOGLE_API_KEY`. Change the model for every agent with `DEMO_MODEL`. `compare.py` prints which backend it used.

## What to look for

- **Peak prompt**: the largest prompt any single LLM call saw. The generalist carries the whole log plus code plus README. Each specialist carries one file.
- **Total prompt tokens**: fan_out makes more calls, so this can be higher. Parallel does not mean cheaper.
- **Seconds**: the three specialists run at once, so fan_out can be faster. The synthesiser step adds a call.
- **Findings**: does either variant miss a planted issue? If the single agent finds everything and is not slower, `compare.py` says exactly that.

## Known limitations

- Tiny fixture. A real repo makes the gap bigger; this one may show little.
- LLM variance. One run proves little; use `--runs 3` or more.
- Token counts include tool results (the file contents), which is the point, but it means they are not just "prompt text".
- Scoring is keyword matching, a rough guide. A correct finding phrased unusually can score as missed, and a vague report can score as found.

## When NOT to use sub-agents

- The task is small and fits comfortably in one context.
- Steps depend on each other (the fix needs the finding). Chain them, do not fan out.
- You need one consistent voice or tightly shared context across the whole job.
- Latency and cost matter more than isolation: every extra agent is another LLM call.
- You cannot check the specialists' output. More agents mean more places for errors to hide.
