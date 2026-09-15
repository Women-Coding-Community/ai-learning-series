# WCC Study Buddy

A tutor that guides you to an answer with a question instead of giving it directly, and routes each question to a different model depending on environment and complexity:

- **dev**: local Gemma 4 by default, escalates to Gemini for genuinely hard questions
- **staging** / **prod**: always Gemini, the same model production uses

Every reply ends with a note on which model actually answered, e.g. `_(answered by: ollama_chat/gemma4:e4b · env=dev)_`.

Set the environment for this run with `APP_ENV` (`dev` / `staging` / `prod`), defaults to `dev`.

Full setup, walkthrough, and troubleshooting: [`../06-smart-router-study-buddy.md`](../06-smart-router-study-buddy.md)
