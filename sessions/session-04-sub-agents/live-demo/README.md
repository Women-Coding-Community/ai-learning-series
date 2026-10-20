# Session 4 Live Demo: One Agent vs Three Specialists

Fixtures live in [`adk-comparison/fixtures/shipit/`](adk-comparison/fixtures/shipit/). `cd` there and open `agy`. The ADK version of this comparison is in [`adk-comparison/`](adk-comparison/README.md).

## Answer key (what a good run should find)

The machine-readable version is `adk-comparison/fixtures/expected.json` (kept outside `shipit/` so `agy` cannot read it).

| Job | Expected findings |
|---|---|
| Security (`app/payments.py`) | L8 hardcoded `SECRET_KEY` (`sk_test_FAKE_DO_NOT_USE`); L21 SQL built with an f-string in `find_orders` |
| Test triage (`tests/output.log`, 1,498 lines) | 2 real failures: `test_refund_rounding` (L556, `999 == 1000`) and `test_webhook_retry` (L1142, `TimeoutError`) |
| Docs (`README.md`) | Says `amount` in pounds, code takes `amount_pence`; says `retries` defaults to 5, code defaults to 3 |

Check exact line numbers with `grep -n` before presenting. Run `python3 -m unittest -v` inside `shipit`: all 3 tests pass.

## Beat 1: one agent does everything (2 min)

Say: "Here is a small repo with a security bug, a noisy test log and out-of-date docs. Let's ask one agent to do all three."

```
Review the code in this folder as one reviewer. Do three jobs yourself, in this order:
1. Security review of app/payments.py
2. Triage tests/output.log: which tests actually failed and why
3. Check README.md against the code for anything out of date
Finish with one report: three sections, max 5 bullets each, each bullet with file and line.
```

Point at: elapsed time, transcript length, anything missed or vague. Note the numbers.

## Beat 2: three specialists in parallel (3 min)

Say: "Same task. This time the main agent only coordinates."

```
You are the orchestrator. Do not read the files yourself.
Define three subagents with define_subagent:
- security_reviewer: reviews app/payments.py only, read-only, looks for secrets and injection
- test_triager: reads tests/output.log only, returns only the real failures and the likely cause
- docs_checker: compares README.md with app/payments.py, returns only mismatches
Each one must return at most 5 bullets, each with file and line.
Invoke all three concurrently in a single invoke_subagent call.
Then merge their results into one report with three sections.
At the end, tell me how many subagents ran and in what order they finished.
```

Point at: three workers starting together, each seeing only its own file, the parent holding three short summaries instead of a 1,500 line log. Compare time with Beat 1.

### Back-pocket B2: sequential reviewer, fixer, tester

Use only if asked how it differs from Rajani's build. Say: "Her chain is sequential because the fix depends on the finding. Mine is parallel because the jobs are independent."

```
You are the PR lead. Scope: the staged changes only. Name those files in every brief. Do not read or edit files yourself.
Define three subagents with define_subagent:
- security_reviewer: read-only. Table of file, line, severity, issue, why. Ignore style.
- fix_drafter: may edit. Smallest change per finding. Secrets from the environment, SQL with parameters. Do not touch tests. List every file changed.
- test_runner: run exactly python -m unittest -v. Report passed and failed. Never edit files or tests.
Then run them in order, because each needs the last one's output:
1. invoke security_reviewer on the staged files
2. invoke fix_drafter with only the findings
3. invoke test_runner
4. invoke security_reviewer again on the fix
Finish with: found, fixed, tests, still open, needs a human.
```

Needs staged changes: `git init && git add -A` inside `adk-comparison/fixtures/shipit` first (the fixtures are not a repo on their own).

## Beat 3: make one reusable (2 min)

Say: "Transient is fine for a demo. For a team you save the specialist as a file."

Show [`.agents/agents/security_reviewer.md`](.agents/agents/security_reviewer.md). Per the [Antigravity subagents docs](https://www.antigravity.google/docs/subagents?tab=cli), custom subagents live in `.agents/agents/<name>.md` (workspace) or `~/.gemini/config/agents/` (global). The file is already in this folder. Copy it into `adk-comparison/fixtures/shipit/.agents/agents/` and restart `agy`.

Check it loaded: type `/agents`. Custom agents appear under **Available Agents**. Then ask: "Invoke security_reviewer on app/payments.py".

**Seeing subagents in `agy`:** the Beat 2 subagents from `define_subagent` are temporary. They only show up in `/agents` (under **Subagents**) while they run or after they finish in that session, not before. Open `/agents` during Beat 2 and use `Alt+J` / Enter for the detail view.

## Beat 4: land it (1 min)

Say: "Same pattern in ADK, with a script that prints the comparison. It is in the demo folder of the repo. Next month we wire this into CI/CD."

```bash
cd adk-comparison
source .venv/bin/activate
python3 compare.py
```

See [`adk-comparison/README.md`](adk-comparison/README.md) for setup. Run it once before the session and screenshot the output.

Optional: "Invoke a fixer subagent with only the security findings and have it draft a patch as a diff. Do not apply it."

## If it goes wrong

- Subagents do not spawn: add "use invoke_subagent explicitly", or show your screenshots.
- No context meter: use elapsed time and transcript length, and say so.
- Everything stalls: show the ADK comparison output instead.

## Before the session

Run both prompts once and screenshot the results as backup.
