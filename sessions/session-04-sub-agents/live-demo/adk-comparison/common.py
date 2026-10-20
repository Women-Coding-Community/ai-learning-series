"""Settings shared by both variants and the compare script."""
import os

from dotenv import load_dotenv

load_dotenv()

# Gemini via GOOGLE_API_KEY, or Vertex AI when GOOGLE_GENAI_USE_VERTEXAI=True.
# ADK reads those variables itself; we only choose the model.
MODEL = os.getenv("DEMO_MODEL", "gemini-2.5-flash")

TASK = "Review this branch: security issues, real test failures, README drift. Return one report."
