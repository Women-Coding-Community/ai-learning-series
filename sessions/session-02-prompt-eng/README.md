# Session 02 — Prompt Engineering (Prompt Patterns & Security)

This folder demonstrates prompt-engineering patterns and basic security checks for a WCC-focused chatbot.

Quick links:
- Demo runner: [demo.py](sessions/session-02-prompt-eng/demo.py)
- Secure chatbot: [`SecureWCCChatbot`](sessions/session-02-prompt-eng/chatbot.py)
- Non-secure chatbot (for pattern comparison): [`NoSecureWCCChatbot`](sessions/session-02-prompt-eng/chatbot_not_secure.py)
- API init: [`initialize_api`](sessions/session-02-prompt-eng/config.py)
- Prompt patterns: [prompt_patterns.py](sessions/session-02-prompt-eng/prompt_patterns.py)
- Security helpers: [security.py](sessions/session-02-prompt-eng/security.py)
- Prompt engineering reference: [resources/prompt-engineering-guide.md](resources/prompt-engineering-guide.md)

## Goals
- Compare different prompt patterns (zero-shot, few-shot, chain-of-thought, role-based etc).
- Demonstrate security checks: prompt injection detection, PII handling, content filtering.
- Provide an interactive demo to test patterns and security workflows.

## Prerequisites
1. Python 3.11+
2. Create a `.env` from the template:
   cp .env.example .env
   and set your API key (e.g. `GEMINI_API_KEY`).
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to run the demo
1. Ensure your environment is configured (`.env` with GEMINI/GCP keys).
2. From repository root run:
   ```bash
   python sessions/session-02-prompt-eng/demo.py
   ```
   This runs the interactive demo. The main entry is [`run_demo`](sessions/session-02-prompt-eng/demo.py).

3. What the demo does:
   - Part 1 `Compare All PROMPT Patterns` shows how the same query is handled using multiple prompt patterns. 
   ![alt text](assets/image.png)

   - Part 2 checks `How Secure Prompts Are` identify for prompt injection, PII, content sensitivity etc.
   ![alt text](assets/image-1.png)


## Customisation
- Change the query used in pattern comparison inside [demo.py](sessions/session-02-prompt-eng/demo.py).
- Add/modify patterns in [prompt_patterns.py](sessions/session-02-prompt-eng/prompt_patterns.py).
- Tune model params or system prompts where bots construct requests (see code comments in `chatbot.py` and `chatbot_not_secure.py`).