# Live Demo: Ways to Run (and Route) Gemma 4

Session 3's 30-minute Live Build segment, one guide per way. Each is written as a standalone setup doc: prerequisites, exact commands, troubleshooting, and a "what good looks like before the session" checklist to run through ahead of time.

Numbering matches the folder/file names on disk, so 5 and 7 are intentionally missing here: they're kept locally as presenter-only material (an app-level router demo and a gateway-level routing demo) and aren't checked into this shared repo. Way 6 stands on its own and doesn't need either of them.

| # | Guide | Cost | Goal |
|---|---|---|---|
| 1 | [`01-local-ollama.md`](01-local-ollama.md) | £0 | Download and run Gemma 4 locally with Ollama, the "start your POC here, for free" baseline |
| 2 | [`02-docker.md`](02-docker.md) | £0 | Containerise the same setup so it's portable across a teammate's machine or a CI runner |
| 3 | [`03-ollama-cloud-opencode.md`](03-ollama-cloud-opencode.md) | Free tier | Call Gemma 4 through Ollama Cloud, driven by OpenCode as a coding agent, no local GPU needed |
| 4 | [`04-gcp-fixed-cost.md`](04-gcp-fixed-cost.md) | ⚠️ Real money, hourly | Deploy your own Vertex AI endpoint, fixed cost regardless of traffic, plugged into the Session 1/2 harness |
| 6 | [`06-smart-router-study-buddy.md`](06-smart-router-study-buddy.md) | £0/low-cost in dev, pay-per-token from staging onward | WCC Study Buddy, a tutor agent that auto-routes: local Gemma 4 in dev (escalating to Gemini on hard questions), Gemini always in staging/prod, and tags every reply with which model actually answered, see [`06-demo-script.md`](06-demo-script.md) for the word-for-word run of show |

**Bonus, time permitting:** Gemma 4 on-device in the Google AI Edge Gallery app on Pixel, with Agent Skills. No setup guide here as it's a live phone demo; see the session outline for details.

## Before the session

Run through the "what good looks like" checklists yourself first. Way 4 in particular needs a full deploy → test → delete dry run in advance (see its safety notes), and Way 3's cloud model tag should be double-checked on the day since Ollama's cloud catalogue changes fairly often. Way 6 only needs Way 1 plus Gemini credentials (API key or Vertex ADC), but rehearse its example questions so you know which way each one routes, and check the `_(answered by: ...)_` footer actually shows up before relying on it live.

## Demo order

Follow the numbering: each guide notes where it reuses setup from the previous one (e.g. Way 2 assumes Way 1's Ollama CLI is already installed, Way 3 falls back to Way 1 if the Free tier limit is hit mid-demo). Way 6 closes the segment: same agent, same question, but the backend it answers with, and the visible model tag on the reply, both shift by environment tier and by task complexity, not by hand.
