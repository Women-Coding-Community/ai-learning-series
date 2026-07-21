# Session 1 Starter Template

Two files to fill in for a real project during the live build: an `AGENTS.md` and a `SKILL.md`.

## Where each file goes

| File | Lives at | Why |
|---|---|---|
| `AGENTS.md` | **Project root** of the repo you're onboarding the agent onto | It's a single, tool-agnostic onboarding doc — Antigravity, Claude Code, and most other agentic tools all read `AGENTS.md` from the repo root the same way a human reads the top-level `README.md`. Don't nest it in a subfolder. |
| `SKILL.md` | A tool-specific skills folder, **not** a single shared location | Each tool discovers skills its own way. For **Claude Code**, that's a project-level `.claude/skills/<skill-name>/SKILL.md`. For **Antigravity**, check the current Antigravity docs for its skill-discovery path on the day — this is a newer tool and the convention may move. The `SKILL.md` content itself is portable; only the folder it sits in changes per tool. |

So: one `AGENTS.md` at your project root, and one copy of your `SKILL.md` per tool, placed wherever that tool looks for skills.

## How to use these templates

1. Copy [`AGENTS.md`](./AGENTS.md) to the root of a real project you're bringing to the session.
2. Fill in the placeholders — conventions, do-not-touch zones, unsolved issues. Be specific; vague onboarding docs are as useless for an agent as they are for a new joiner.
3. Copy [`skill-template/SKILL.md`](./skill-template/SKILL.md) into your Claude Code skills folder: `.claude/skills/<your-skill-name>/SKILL.md`.
4. Fill in the skill's frontmatter and body, then load it by name and run it.
5. Try the same `SKILL.md` in Antigravity (IDE and CLI) — same content, different folder, per that tool's current docs.

## Folder structure

```text
starter-template/
├── README.md          # This file
├── AGENTS.md           # Template: copy to your project root
└── skill-template/
    └── SKILL.md         # Template: copy into your tool's skills folder
```

When you're happy with your version, submit it to `sessions/session-01-agent-skill/participants/[your-username]/` — see [badge criteria](../../../badges/badge-criteria.md).
