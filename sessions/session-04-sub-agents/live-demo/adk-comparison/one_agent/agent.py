"""Variant A: one generalist agent does all three jobs in a single context window."""
from google.adk.agents import LlmAgent

from common import MODEL
from tools import list_files, read_file

root_agent = LlmAgent(
    name="generalist",
    model=MODEL,
    description="Reviews a branch for security, test failures and README drift.",
    tools=[read_file, list_files],
    instruction=(
        "You are a code reviewer. Use list_files and read_file to do three jobs yourself:\n"
        "1. Security review of app/payments.py.\n"
        "2. Triage tests/output.log: which tests really failed and why. Ignore passing tests and noise.\n"
        "3. Check README.md against app/payments.py for anything out of date.\n"
        "Finish with one report with three sections (Security, Tests, Docs). "
        "At most 5 bullets per section, each bullet with file and line."
    ),
)
