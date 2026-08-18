# Session 2: Tools & Boundaries: MCP, Plugins, Permissions, Hooks

**Level:** All levels

## Overview

An agent is only as useful as the tools you trust it with, and only as safe as the boundaries around them. This session is the governance half of the harness. We'll give the agent hands and eyes through MCP servers and plugins (think Jira, GitLab, Gmail), then put the seatbelt on with permissions (allow, ask, deny) and per-project boundaries, so your work tools never leak into hobby projects. We finish with hooks: un-skippable JSON gates the agent physically cannot bypass, like a pre-commit secret scan that fires on every agent commit. You'll leave with an agent that can act, but only exactly where you've let it.

## Live Build

- Wire one MCP server, scoped to a single project (work tools never leak into hobby projects)
- Add a pre-commit JSON hook that scans for secrets on every agent commit
- Set permissions and a sandbox policy
- **Live demo:** a real LinkedIn MCP server (below), because none existed off the shelf

## Tonight's demo: a LinkedIn MCP server, built because none existed

There's no official LinkedIn MCP server. This one was built for the ADK social-poster agent (`social-spark`) and is a genuinely useful "why MCP" story: a capability that doesn't exist anywhere else, wrapped once so any MCP-aware surface can use it, not just the one agent that needed it first.

**What it exposes** (`mcp/linkedin_server.py`, FastMCP over stdio):

| Tool | What it does | Risk |
|---|---|---|
| `get_profile()` | Reads the authenticated member's id/name via OpenID userinfo | Read-only, low |
| `create_post(text, image_path?)` | Publishes to the member's live feed via the LinkedIn Posts API | Write, public, irreversible |

**Two governance mechanisms already built in, which map straight onto tonight's concepts:**

1. **`DRY_RUN` (default `true`)** — a hand-rolled hook. Every call to `create_post` checks this flag *before* touching the network; with it on, the server logs the payload and hands back a fake `post_url`, nothing reaches LinkedIn. It's not called a hook in the code, but that's exactly the pattern: a gate the agent cannot talk its way past, because the check lives in the tool, not in the prompt.
2. **The OAuth scope itself (`openid profile w_member_social`)** — permissions LinkedIn granted the token, independent of anything your agent config says. Two layers of "allow": what LinkedIn's token allows, and what your own agent config allows on top of that.

**Live build sequence:**

1. Start the server with `DRY_RUN=true` (the default) and run it through `npx @modelcontextprotocol/inspector uv run mcp/linkedin_server.py` so the room sees raw MCP tool calls, no agent involved yet.
2. Call `get_profile()` live — read-only, set to **allow** in the permission config.
3. Call `create_post()` — set to **ask**, so the agent proposes the post text and waits for a thumbs up before the (still dry-run) call fires.
4. Show the JSON hook layer: `DRY_RUN` is already a hook, but for the demo, formalise it as an explicit pre-call check in `agents.yaml` too, so the boundary lives in config, not just in one Python file someone could edit.
5. **Do not flip `DRY_RUN=false` live.** If you want to show a real post, do the one verified happy-path run before the session (per the server's own README), then reset it to `true` and leave it there for the demo.

## MCP server vs. direct API call as a tool: which one, and when

This is the real decision behind `linkedin_server.py`, worth naming explicitly tonight since it's the natural follow-on question after Session 1's skills.

**Write it as a direct tool function inside the agent (no MCP) when:**
- Only one agent, in one framework, will ever call it
- It's a single function, low complexity, no need to run as its own process
- In-process latency matters more than portability
- You're happy for the capability's guardrails to live wherever that agent's code lives

**Wrap it as an MCP server (what was actually built here) when:**
- The capability should be reusable outside the one agent that needed it first — this LinkedIn server can be dropped into Claude Code, Claude Desktop, another ADK agent, or tested standalone via `mcp-inspector`, without rewriting anything
- You want the governance (the `DRY_RUN` gate, the token scope, the permission checks) to travel *with* the capability, not be re-implemented per agent that uses it
- You expect more than one agent or team to eventually need the same tool
- Nothing off-the-shelf exists yet and you'd rather build the reusable version once

Rule of thumb for the room: **skill first if it's judgment, MCP first if it's action nobody else has wired yet.** A one-off internal function is fine as a direct tool; a capability worth reusing earns the MCP wrapper.

## MCP/Hooks (this session) vs. Agent Skills (Session 1): which one, and when

Ties the two sessions together, which is worth spelling out explicitly since it's the exact confusion people hit:

- **Agent Skill (Session 1)** is the *brain*: a reusable playbook, markdown, no side effects, portable as instructions the model loads by name. Use it to standardise judgment or process — e.g. "how WCC writes a LinkedIn post in our voice and structure."
- **MCP server (this session)** is the *hands*: real code, real API calls, real side effects in the world. Use it when the agent needs to actually *do* something outside the conversation — e.g. actually publish that post.
- **Permissions + hooks (this session)** are the *seatbelt* on those hands: they govern what the hands are allowed to do, and they're enforced outside the model, so the model can't reason its way past them.

Concretely, in the `social-spark` project: a "write a WCC-voice LinkedIn post" Skill from Session 1's pattern would sit next to this LinkedIn MCP server. The Skill decides *what to write and how*; the MCP server is the only thing that can actually *publish* it; `DRY_RUN` plus an `ask` permission tier decide *whether it's allowed to, right now*. All three layers, one agent.

## Steal This

Project-scoped MCP, governance by default. Also worth stealing: a `DRY_RUN`-style flag baked into any tool with real-world side effects, checked in code, not just described in a prompt.

## Takeaway

An agent that can act, but only where you've allowed it.

## Folder structure

```
session-02-tools-boundaries/
├── live-demo/           # MCP config and pre-commit hook built live, incl. linkedin_server.py demo
├── starter-template/    # Blank starting point to follow along
└── participants/        # Submit your own version here (see badges/badge-criteria.md)
```

## Setup

See [`getting-started/`](../../getting-started/) for the general prerequisites. A session-specific setup checklist is posted in [#ai-learning-series](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) the week before.

If you're following along with the LinkedIn MCP demo specifically: you'll need `uv`, `fastmcp`, `httpx`, and (only if you want a real, non-dry-run post) a LinkedIn Developer app with the `Share on LinkedIn` and `Sign In with LinkedIn using OpenID Connect` products added. Full OAuth walkthrough lives in `mcp/README.md` next to the server.
