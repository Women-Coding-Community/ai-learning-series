# Way 1: Download and Run Gemma 4 Locally with Ollama

**Session:** Harness Series, Session 3, Small Models in Practice
**Cost:** £0, fully offline once downloaded
**Time to test:** ~10 minutes, most of it is the download

---

## Prerequisites

- A Mac, Linux box, or Windows machine
- ~10GB free disk space (more if you try bigger sizes)
- No GCP account, no API key, no internet needed once the model is downloaded

**Tested on:** MacBook Pro M4, 16GB unified memory. At this spec, `gemma4:e4b` is the sweet spot: fast, and leaves headroom for everything else you'll have open (terminal, browser, Docker if you're also testing Way 2). `gemma4:12b` will run but eats half your RAM, so close other heavy apps first. Don't attempt `gemma4:31b` on 16GB, it won't fit.

**⚠️ Check your free RAM before you run anything, not after:** on Apple Silicon, RAM is unified between CPU and GPU, so a model that's too big for what's actually free competes directly with the graphics stack. In the worst case this doesn't just make things slow, it can starve `WindowServer` long enough that macOS's watchdog force-panics and restarts the machine, no warning, no save prompt. Before picking a size:

```bash
# macOS: check free memory before you start
vm_stat | awk '/Pages free/ {print $3 * 4096 / 1073741824 " GB free"}'
```

Close other memory-heavy apps first (Docker, browser tabs with lots of tabs, other IDEs), and match your size choice to the sizing table below, not just your total RAM, what matters is what's actually free right now.

---

## Step 1: Install Ollama

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Or on macOS, download the app directly from https://ollama.com/download
```

Verify it installed:

```bash
ollama --version
```

---

## Step 2: Pull and Run Gemma 4

Start with the smallest variant to confirm everything works, then move up:

```bash
# Edge variant, tiny, runs on almost anything
ollama run gemma4:e2b

# The recommended default for a 16GB Mac
ollama run gemma4:e4b
```

The first run downloads the model (a few GB depending on size), then drops you into an interactive chat. Try a couple of prompts:

```
>>> Explain what a Skill file does in an agent harness, in two sentences.
>>> /bye
```

`/bye` exits the chat session.

---

## Step 3: Confirm the REST API Is Live

Ollama also runs a local server on port 11434. This is what you'll point your agent, Skill, or MCP setup at.

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gemma4:e4b",
  "messages": [{"role": "user", "content": "Say hello in one sentence."}],
  "stream": false
}'
```

You should get back a JSON response with the model's reply.

---

## Step 4: Check What's Installed and How Big

```bash
ollama list
```

Shows every model you've pulled locally, with size on disk.

---

## Sizing Reference (Q4 quantised, what Ollama pulls by default)

| Gemma 4 size | Min RAM | Fits on 16GB Mac? |
|---|---|---|
| E2B | ~1.5GB | Yes, easily |
| E4B | ~5GB | Yes, recommended default |
| 12B Unified | ~8GB | Yes, but close other apps |
| 26B A4B MoE | ~14–18GB | Too tight, expect swapping |
| 31B Dense | ~20GB | No |

---

## Troubleshooting

**Model download is slow or stalls:** it's a large file, check your connection isn't rate-limited by a VPN or firewall. Retry with `ollama pull gemma4:e4b` on its own before `ollama run`.

**"out of memory," the Mac becomes unresponsive, or it force-restarts entirely:** you've picked a size too big for your free RAM. Drop down a size, and check Activity Monitor's memory pressure graph while it's running, if it's in the red before you even prompt it, that's your answer. Don't dismiss this as "just slow", it can escalate all the way to a kernel panic: if you ever see a restart with a panic log mentioning `userspace watchdog timeout: no successful checkins from WindowServer`, that's macOS force-restarting because memory pressure from the model starved the display process for too long, not a hardware fault. Same fix either way: smaller model size, or free up RAM before you run it.

**Port 11434 already in use:** something else is already running Ollama (maybe it auto-started). Check with `lsof -i :11434` and either use the existing instance or stop it first.

---

## What "Good" Looks Like Before the Session

- [ ] `ollama --version` returns a version number
- [ ] You've checked free RAM (not just total RAM) and picked a model size that comfortably fits, with other apps closed
- [ ] `ollama run gemma4:e4b` completes a chat exchange without crashing
- [ ] The `curl` call to `localhost:11434/api/chat` returns a JSON reply
- [ ] `ollama list` shows `gemma4:e4b` with a size on disk

If all four are ticked, you're ready for this segment of the live demo.
