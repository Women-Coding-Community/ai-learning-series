"""Deterministic, explainable complexity classifier for the router.

Live-demo note: this is intentionally a plain heuristic, not another model
call. Asking a small local model to grade its own question's difficulty is
an unreliable narrator, and a flaky classifier is the last thing you want
mid-talk. A word/pattern heuristic is transparent enough that the audience
can read the exact rule that just fired.
"""

import re

COMPLEX_SIGNALS = [
    r"\bprove\b",
    r"\bderive\b",
    r"\btime complexity\b",
    r"\bbig-?o\b",
    r"\bdesign (a|an)\b.*\bsystem\b",
    r"\btrade-?offs?\b",
    r"\bdistributed\b",
    r"\barchitecture\b",
    r"\boptimi[sz]e\b",
    r"\bproof\b",
    r"\bnp-?hard\b",
]

LONG_QUESTION_WORD_COUNT = 40


def classify(question: str) -> str:
    """Returns "complex" or "simple". Empty input defaults to "simple"."""
    q = (question or "").lower()
    if not q.strip():
        return "simple"

    hits = [pattern for pattern in COMPLEX_SIGNALS if re.search(pattern, q)]
    if hits:
        return "complex"

    if len(q.split()) > LONG_QUESTION_WORD_COUNT:
        return "complex"

    return "simple"
