# LinkedIn MCP server

FastMCP stdio server exposing `get_profile()` and `create_post(text, image_path?)`.
With `DRY_RUN=true` (the default) it logs the payload and returns a fake post URL —
nothing touches LinkedIn. Set `DRY_RUN=false` only for the single happy-path
verification, then flip it back.

## Prerequisites

| Tool | Needed for | Check | Install |
|---|---|---|---|
| [`uv`](https://docs.astral.sh/uv/) | Running the server / smoke tests | `uv --version` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Node.js + `npx` | MCP Inspector only | `npx --version` | https://nodejs.org (or `brew install node`) |
| [Claude Code](https://claude.com/product/claude-code) | The live Claude Code demo | `claude --version` | `npm install -g @anthropic-ai/claude-code` |
| A LinkedIn Developer app + access token | Only if you want `get_profile`/`create_post` to hit the *real* API (dry-run needs none of this) | — | see "LinkedIn Developer app setup" below |

Everything else (`fastmcp`, `httpx`) is resolved automatically by `uv` — see next section.

No `requirements.txt` needed — dependencies (`fastmcp`, `httpx`) are declared inline at
the top of `linkedin_server.py` as [PEP 723 script metadata](https://peps.python.org/pep-0723/).
`uv` reads that block and resolves an ephemeral environment on the fly, but **only when the
script itself is the thing you hand to `uv run`** — `uv run mcp/linkedin_server.py`, not
`uv run python mcp/linkedin_server.py` (the latter runs `python` as the command, so uv never
looks at the script header and you'll get `ModuleNotFoundError: No module named 'fastmcp'`).

```bash
# standalone smoke test (from the repo root)
DRY_RUN=true uv run mcp/linkedin_server.py   # then speak MCP over stdio, or:
npx @modelcontextprotocol/inspector uv run mcp/linkedin_server.py
```

First run downloads `fastmcp`/`httpx` into a throwaway env (a few seconds); after that
`uv` caches it and startup is instant. No manual `pip install` step required.

> Run only **one** of the two lines above at a time, not both back to back — the first
> starts the raw server and blocks the terminal waiting for JSON-RPC on stdin. It has
> nothing to show you and nothing to type into; typing anything (even a stray Enter)
> gets parsed as garbage input and logged as an error, harmlessly, on repeat. Exit with
> `Ctrl+C` (or `Ctrl+D` for a clean EOF shutdown). To actually see or click anything, use
> the Inspector line, or connect via Claude Code (below) — both speak proper JSON-RPC to
> it instead of a human typing into the pipe.
>
> If `Ctrl+C` doesn't kill it on the first press and you hit it again, you'll see a
> `KeyboardInterrupt` traceback and sometimes a `uv`-level `error: Failed to get PID of
> child process ... ESRCH: No such process`. Both are harmless shutdown noise (the second
> `Ctrl+C` racing an already-dying process) — not a crash, don't stop to debug it live.

> If you ever edit the Command/Arguments fields directly in the Inspector UI (instead of
> just using the connection it auto-fills from the terminal launch), use an **absolute
> path** to `linkedin_server.py`, not the relative `mcp/linkedin_server.py`. A UI-triggered
> reconnect spawns a fresh process that isn't rooted in `live-demo/` the way the original
> terminal launch was, so the relative path fails with `Failed to spawn ... No such file or
> directory`. Simplest fix: don't touch the form — reload the exact
> `http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=...` URL your terminal printed, it comes
> pre-filled with the working config.

The Inspector line takes ~10–15s to come up (longer on the very first run, while `npx`
downloads the package) and then prints something like:

```
🚀 MCP Inspector is up and running at:
   http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=<a long hex token>
```

**Use that exact URL from your terminal, token included** — it should also auto-open in
your browser. Auth is on by default in current Inspector versions, so navigating to the
bare `http://localhost:6274` without the token gets rejected/refused; that's the "I can't
access it" failure mode if you jump the gun before the URL prints, or paste the short form
from memory instead of copying the real line. Once it's open: click **Connect**, then
**Tools**, and `get_profile` / `create_post` show up as clickable forms with a response
pane underneath.

## Connect it to Claude Code (the live demo)

The project-scoped `.mcp.json` one level up (`live-demo/.mcp.json`) already declares this
server, `DRY_RUN=true`, with the token read from your shell env — nothing to type live.

1. **Set the token in your shell** before opening Claude Code, so `.mcp.json`'s
   `${LINKEDIN_ACCESS_TOKEN}` resolves (dry-run works fine with this unset or fake —
   only needed if you want `get_profile` to hit the real userinfo endpoint):
   ```bash
   export LINKEDIN_ACCESS_TOKEN=...   # optional for a pure dry-run demo
   ```
2. **Open `live-demo/` as the project root** (`cd sessions/session-02-tools-boundaries/live-demo && claude`).
   Claude Code detects `.mcp.json` and prompts to approve the `linkedin` server — approve it
   on camera, so the room sees the trust prompt, not just the result.
3. **Set permission tiers** in `.claude/settings.json` inside `live-demo/` before you start talking:
   ```json
   {
     "permissions": {
       "allow": ["mcp__linkedin__get_profile"],
       "ask": ["mcp__linkedin__create_post"]
     }
   }
   ```
4. **Demo script, in order:**
   - Ask: *"What's my LinkedIn profile?"* → `get_profile` fires with no prompt (allow tier) →
     read out the dry-run id/name.
   - Ask: *"Draft and post a LinkedIn update about tonight's session."* → Claude proposes post
     text, then `create_post` pauses on the **ask** tier → approve it live → point out the
     returned `post_url` is a fake `dryrun-` URN and `"dry_run": true` — nothing left the process.
   - Optional: point at the terminal/log line `[linkedin-mcp] DRY_RUN create_post payload: ...`
     as the receipt that the gate lived in the tool the whole time, not in the prompt.
5. **Do not set `DRY_RUN=false` or unset it during the session.** If you want to show a real
   published post, do that once beforehand per the section below, screenshot it, then reset to
   `true` and never touch it live.

## LinkedIn Developer app setup

1. **Create the app**: https://www.linkedin.com/developers/apps → *Create app*.
   You need a LinkedIn *company page* to associate (create a dummy one if needed).
2. **Add products** (Products tab, both are instant self-serve approval):
   - **Share on LinkedIn** → grants `w_member_social`
   - **Sign In with LinkedIn using OpenID Connect** → grants `openid`, `profile`
3. **Auth tab**: note *Client ID* and *Client Secret*; add a redirect URL, e.g.
   `http://localhost:3000/callback` (it never needs to serve anything).

## Getting a 3-legged OAuth token

1. Open in a browser (one line, fill in CLIENT_ID):

   ```
   https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=CLIENT_ID&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fcallback&scope=openid%20profile%20w_member_social
   ```

2. Approve; you land on `localhost:3000/callback?code=...` (page won't load —
   fine). Copy the `code` from the URL bar. **It expires in ~30 minutes.**

3. Exchange it:

   ```bash
   curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
     -d grant_type=authorization_code \
     -d code=THE_CODE \
     -d client_id=CLIENT_ID \
     -d client_secret=CLIENT_SECRET \
     -d redirect_uri=http://localhost:3000/callback
   ```

4. The response's `access_token` (valid ~60 days) — export it in your shell (the server
   reads `os.environ` directly, no `.env` file is loaded):

   ```bash
   export LINKEDIN_ACCESS_TOKEN=...
   export DRY_RUN=true
   ```

## Verify the happy path ONCE

```bash
cd sessions/session-02-tools-boundaries/live-demo
DRY_RUN=false LINKEDIN_ACCESS_TOKEN=... uv run --with fastmcp --with httpx python -c "
import sys; sys.path.insert(0, 'mcp')
from linkedin_server import create_post
print(create_post('Testing my ADK DevCamp posting pipeline. If you can read this, it worked.'))
"
```

Two gotchas found while testing this locally, both already fixed above:
- Don't `from mcp.linkedin_server import ...` — the installed `mcp` SDK package (a
  dependency of `fastmcp`) shadows the local `mcp/` folder since it has no
  `__init__.py`. `sys.path.insert(0, 'mcp')` + `from linkedin_server import ...`
  sidesteps the collision.
- `create_post` is called directly, not `create_post.fn(...)` — this fastmcp version
  (3.4.x) returns the plain function from `@mcp.tool`, it doesn't wrap it in an object
  with a `.fn` attribute.

Then set `DRY_RUN=true` and leave it forever.
