# Way 2: Containerise Gemma 4 with Docker

**Session:** Harness Series, Session 3, Small Models in Practice
**Cost:** £0, still fully local, just packaged
**Time to test:** ~10 minutes if Way 1 is already done (image pull only)

---

## Why This Way, and Not Just Way 1 Again

Same model, same zero cost, but now it's portable: a teammate, a CI runner, or a demo machine gets the exact same environment without installing Ollama natively. This is the version you'd actually wire into a CI/CD pipeline in Session 5.

**⚠️ Bind mount, not a named volume:** the steps below mount your host's actual `~/.ollama` directory into the container (`-v ~/.ollama:/root/.ollama`), not a Docker-managed named volume (`-v ollama:/root/.ollama`). This matters: a named volume lives inside Docker Desktop's own internal VM storage, completely separate from the `~/.ollama` that native Ollama (Way 1) already populated, so the container would re-pull the entire multi-GB model from scratch on first run even though it's already on disk. The bind mount below reuses Way 1's download directly, which is also what makes the "~10 minutes if Way 1 already done" timing in the header actually true.

---

## Prerequisites

- Docker Desktop installed and running (macOS: https://www.docker.com/products/docker-desktop)
- ~1-2GB free disk space for the `ollama/ollama` image itself (the model weights are reused from Way 1 via the bind mount below, not re-downloaded)

**Tested on:** MacBook Pro M4, 16GB. Docker Desktop itself takes a chunk of memory, so if you're running this right after Way 1's local Ollama, stop the native `ollama serve` process first, or you'll have two things fighting over port 11434 and your RAM.

---

## Step 1: Run Ollama Inside a Container

```bash
docker run -d \
  -v ~/.ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama
```

What this does:
- `-v ~/.ollama:/root/.ollama` bind-mounts your host's Ollama directory straight into the container, so it sees the models Way 1 already downloaded and doesn't re-pull them. It also means the container persists across restarts for free, since it's just reading/writing your normal host directory
- `-p 11434:11434` exposes the same port as native Ollama, so anything you built against `localhost:11434` in Way 1 works unchanged
- `-d` runs it in the background

If you'd rather keep the container's storage fully isolated from your host (e.g. demoing true portability, no dependency on Way 1 having run first), swap in a named volume instead — `-v ollama:/root/.ollama` — but budget for a full model re-download the first time, it will not see anything Way 1 pulled.

Confirm it's running:

```bash
docker ps
```

You should see a container named `ollama` with status `Up`.

---

## Step 2: Pull Gemma 4 Inside the Container

```bash
docker exec -it ollama ollama run gemma4:e4b
```

`docker exec -it` runs a command inside the already-running container. Since you bind-mounted `~/.ollama`, this should find the model Way 1 already downloaded and drop straight into an interactive chat, no re-pull. If you instead see `pulling manifest` and a multi-GB download start, check the `docker run` command actually used `-v ~/.ollama:/root/.ollama` (bind mount) and not `-v ollama:/root/.ollama` (named volume), see the note at the top of this guide.

---

## Step 3: Confirm the API Works the Same Way

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gemma4:e4b",
  "messages": [{"role": "user", "content": "Confirm you are running in a container."}],
  "stream": false
}'
```

Same endpoint, same response shape as Way 1, that's the whole point: containerising doesn't change how your agent or Skill talks to it.

---

## Step 4 (Optional): Confirm the Bind Mount Persists

```bash
# Stop and remove the container entirely, host directory is untouched
docker stop ollama
docker rm ollama

# Recreate the container against the same host directory
docker run -d -v ~/.ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# Model should already be there, no re-download
docker exec -it ollama ollama list
```

---

## Cleaning Up

```bash
docker stop ollama
docker rm ollama
```

That's it, no `docker volume rm` needed: with a bind mount, the models live at `~/.ollama` on your host, exactly where Way 1 left them, so removing the container never touches them. (If you demoed the named-volume alternative instead, clean that up separately with `docker volume rm ollama` if you want the disk space back.)

---

## Troubleshooting

**"port is already allocated":** something's already bound to 11434, most likely native Ollama from Way 1 still running. Stop it with `ollama stop` or check `lsof -i :11434`, then retry.

**Container exits immediately:** check logs with `docker logs ollama`. Usually a port conflict or insufficient Docker Desktop memory allocation (check Docker Desktop → Settings → Resources).

**Slow inside the container vs native:** expected, there's a small virtualisation overhead on macOS specifically since Docker Desktop runs a Linux VM under the hood. Fine for a demo, worth knowing for production sizing.

**`docker exec -it ollama ollama run gemma4:e4b` re-downloads the model even though Way 1 already has it:** your `docker run` used a named volume (`-v ollama:/root/.ollama`) instead of the bind mount (`-v ~/.ollama:/root/.ollama`). Named volumes are Docker-managed storage inside Docker Desktop's own VM, not your host's `~/.ollama`, so they start empty regardless of what's already on disk. Stop and remove the container, and recreate it with the bind mount from Step 1.

**Permission errors on the bind mount:** rare on macOS since Docker Desktop's VirtioFS file sharing handles the host/container UID mapping transparently, but if you see permission-denied errors reading `/root/.ollama` inside the container, confirm Docker Desktop has file-sharing access to your home directory (Settings → Resources → File Sharing).

---

## What "Good" Looks Like Before the Session

- [ ] `docker ps` shows the `ollama` container `Up`
- [ ] `docker run` used `-v ~/.ollama:/root/.ollama` (bind mount), not `-v ollama:/root/.ollama` (named volume)
- [ ] `docker exec -it ollama ollama run gemma4:e4b` completes a chat exchange **without re-downloading** the model Way 1 already pulled
- [ ] The `curl` call to `localhost:11434/api/chat` returns a JSON reply, identical shape to Way 1
- [ ] You can stop, remove, and recreate the container without re-downloading the model

If all four are ticked, you're ready for this segment of the live demo.
