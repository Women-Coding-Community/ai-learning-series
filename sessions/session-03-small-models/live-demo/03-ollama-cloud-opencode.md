# Way 3: Call Gemma 4 Through Ollama Cloud, Driven by OpenCode

**Session:** Harness Series, Session 3, Small Models in Practice
**Cost:** Free tier available, check current plan limits before relying on it live (see note below)
**Time to test:** 20 to 30 minutes the first time, including installing both CLIs

---

## Why This Way

No local GPU or RAM ceiling to worry about, someone on an 8GB laptop gets the same experience as someone on a 32GB workstation, because the model runs on Ollama's infrastructure, not yours. OpenCode then drives it as a coding agent, so this is also the most natural bridge into the harness patterns from Sessions 1 and 2.

---

## ⚠️ Verify Before You Rely On This Live

Ollama's cloud model catalogue and plan limits change fairly often (models get retired and replaced on short notice). Before the session:
1. Check `ollama.com/library` for the current official Gemma 4 cloud tag name
2. Check [`ollama.com/settings`](https://ollama.com/settings) for your account's current usage and what's included on the Free tier this month
3. Have a screenshot or note of both, in case the live model name has moved on since you tested

---

## What You Need Installed, in Full

This way needs **two separate CLIs**, plus a runtime for one of them. None of this is optional, both tools do different jobs: Ollama CLI talks to the model, OpenCode CLI is the agent that drives it.

| Tool | What it's for | Needed? |
|---|---|---|
| **Ollama CLI** | Signs you into Ollama Cloud, resolves the `:cloud` model tag | Yes |
| **Node.js 18+** | Runtime OpenCode needs if you install it via npm, or if the install script pulls in Node-based tooling | Recommended, see install options below |
| **OpenCode CLI** | The coding agent that connects to the model and does the actual work | Yes |
| **An Ollama account** | Free to create, required for cloud model access | Yes |
| **A modern terminal** | OpenCode has a proper TUI (terminal UI), needs true colour + Unicode support | Yes |

**Terminal check:** iTerm2, Alacritty, WezTerm, Ghostty, Kitty, or VS Code's integrated terminal all work fine. macOS's default Terminal.app can have rendering glitches with OpenCode's UI, if you hit weird visual artefacts, switch terminals before debugging anything else.

---

## Prerequisites Checklist

- [ ] macOS, Linux, or Windows (Windows: use WSL for the smoothest experience, native Windows works too via Scoop/npm)
- [ ] A terminal from the list above
- [ ] An Ollama account (sign up free at ollama.com if you don't have one)
- [ ] Node.js 18 or higher, **only if** you choose the npm install route for OpenCode (check with `node --version`)

---

## Step 1: Install the Ollama CLI

If you already did Way 1 or Way 2, you have this, skip to Step 2.

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh
```

Verify:

```bash
ollama --version
```

---

## Step 2: Install the OpenCode CLI

Pick **one** of these, they all end up in the same place:

```bash
# Option A: quick install script (fastest, macOS/Linux)
curl -fsSL https://opencode.ai/install | bash

# Option B: Homebrew (macOS/Linux)
brew install opencode

# Option C: npm (any platform, needs Node.js 18+)
npm install -g opencode-ai

# Option D: Windows, Scoop
scoop install opencode
```

Note for Option C: the npm **package** name is `opencode-ai`, not `opencode`, easy to typo.

Verify it installed:

```bash
opencode --version
```

If that fails after an npm install, check `npm prefix -g` is actually on your `PATH`, this is the most common install snag on Windows in particular.

---

## Step 3: Create an Ollama Account (If You Don't Have One)

Go to [ollama.com](https://ollama.com), sign up, it's free. You need this account for cloud model access, local-only usage (Ways 1 and 2) doesn't require one, but cloud does.

---

## Step 4: Sign In to Ollama Cloud from the CLI

```bash
ollama signin
```

This opens a browser to authenticate your CLI against your Ollama account. Confirm you're signed in:

```bash
ollama whoami
```

---

## Step 5: Launch OpenCode Against a Cloud-Hosted Gemma 4

```bash
ollama launch opencode --model gemma4:cloud
```

If that exact tag has moved on by the time you test this (see the verification note above), substitute whatever the current official Gemma 4 cloud tag is from `ollama.com/library`.

This does two things in one command:
- Points OpenCode's provider config at Ollama's hosted endpoint instead of your local one
- Drops you into an interactive OpenCode session

---

## Step 6: Try a Coding Task

Inside OpenCode, give it something small and concrete:

```
Write a Python function that validates an email address with a regex, and add one test case.
```

Watch it reason and produce code, this is the same "agent driving a model" pattern from Session 1, just with the model hosted in Ollama's cloud instead of local.

Useful OpenCode keys while you're in there:
- `Tab` switches between Plan mode (read-only, thinks out loud) and Build mode (actually edits files)
- `/connect` opens the provider picker if you want to switch models mid-session
- `Ctrl+C` or typing `exit` ends the session

---

## Step 7 (Optional): Manual Config, If You Want It Persistent

If you don't want to type `ollama launch opencode` every time, wire it into OpenCode's own config so it's there whenever you open OpenCode normally:

```json
// ~/.config/opencode/opencode.json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama Cloud",
      "options": {
        "baseURL": "https://ollama.com/v1"
      },
      "models": {
        "gemma4-e4b-cloud": {
          "name": "gemma4:e4b-cloud"
        }
      }
    }
  }
}
```

Note: `ollama launch opencode` does **not** overwrite this file, it layers an inline config on top for that one session. Anything you define here persists across normal `opencode` launches too.

Run it directly after that with just:

```bash
opencode
```

---

## Troubleshooting

**"unauthorized" or sign-in loop:** run `ollama signin` again, and check you're not behind a proxy/VPN blocking the browser auth redirect.

**Model tag not found:** cloud model tags get retired and renamed more often than local ones. Check `ollama.com/library` for the current name, this is the single most likely thing to break between your test and the live session, hence the verification step at the top.

**`opencode: command not found` after install:** your shell's `PATH` hasn't picked up the new binary. Open a new terminal tab/window, or run `npm prefix -g` (if you used the npm route) and confirm that path is in your `PATH`.

**Node version too old:** OpenCode's npm install route needs Node 18+. Check with `node --version`, upgrade via `nvm install 18` (or later) if you're on an older version, or just use the curl script or Homebrew route instead, which don't need Node at all.

**Rendering looks broken (missing colours, garbled characters):** you're likely on an older terminal emulator. Switch to iTerm2, WezTerm, Alacritty, or VS Code's integrated terminal.

**OpenCode doesn't launch via `ollama launch opencode`:** confirm both CLIs are actually installed (`ollama --version` and `opencode --version` both return something), this command needs both present, it doesn't install OpenCode for you.

**Free tier limit hit mid-demo:** have Way 1 (local Ollama) ready as an immediate fallback, same model family, no cloud dependency, keeps the session moving.

---

## What "Good" Looks Like Before the Session

- [ ] `ollama --version` and `opencode --version` both return a version number
- [ ] `ollama whoami` confirms you're signed in to Ollama Cloud
- [ ] `ollama launch opencode --model <current-gemma4-cloud-tag>` opens an OpenCode session without errors
- [ ] A test coding prompt gets a sensible response with no local GPU/RAM involved
- [ ] You know the current Free tier limits, and won't be surprised mid-demo
- [ ] Your terminal renders OpenCode's UI cleanly, no garbled colours or characters

If all six are ticked, you're ready for this segment of the live demo.
