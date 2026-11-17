"""Turn findings.json into the Markdown for one PR comment.

The post job runs this. It never calls a model and never reads the PR's code:
its only input is the findings file the agent job uploaded.

    python scripts/render_comment.py findings.json > comment.md
"""
from __future__ import annotations

import json
import re
import sys

MARKER = "<!-- shipit-ai-review -->"
ICONS = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}


def safe(text: object) -> str:
    """Model text is untrusted: no mentions, no HTML, no table breaks, one line."""
    value = " ".join(str(text).split())
    value = value.replace("<", "&lt;").replace(">", "&gt;").replace("|", "\\|")
    return re.sub(r"@(?=\w)", "@\u200b", value)


def render(result: dict) -> str:
    lines = [MARKER, "## AI first-pass review", ""]
    status = result.get("status")
    if status != "ok":
        lines.append(f"Review {safe(status or 'unknown')}: {safe(result.get('reason', 'no reason given'))}")
    else:
        findings = result.get("findings", [])
        if result.get("summary"):
            lines += [safe(result["summary"]), ""]
        if not findings:
            lines.append("No findings on the changed lines.")
        else:
            lines += ["| | Where | Finding |", "| --- | --- | --- |"]
            for f in findings:
                where = f"`{safe(f['file'])}:{int(f['line'])}`"
                lines.append(
                    f"| {ICONS.get(f['severity'], '')} {safe(f['severity'])} | {where} "
                    f"| **{safe(f['title'])}**<br>{safe(f['detail'])} |"
                )
        if result.get("dropped"):
            lines += ["", f"{int(result['dropped'])} malformed or surplus finding(s) were dropped."]
    lines += [
        "",
        "<sub>Advisory only. This reviewer can read the diff and nothing else: it cannot push, "
        "approve or merge. React with 👍 or 👎 so we can measure whether it is worth keeping.</sub>",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as handle:
        sys.stdout.write(render(json.load(handle)))
