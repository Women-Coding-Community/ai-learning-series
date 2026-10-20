"""Variant B: three specialists in parallel, then a synthesiser merges their findings."""
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent

from common import MODEL
from tools import make_read_file

BULLETS = "Return at most 5 bullets. Each bullet: file, line, what is wrong."

# output_key writes each specialist's final answer into session.state under
# that name, so later agents can read it with {name} in their instruction.
security_reviewer = LlmAgent(
    name="security_reviewer",
    model=MODEL,
    tools=[make_read_file(("app/payments.py",))],
    output_key="security_findings",
    instruction=(
        "You are a security reviewer. Read app/payments.py only. "
        f"Look for hardcoded secrets and injection. {BULLETS}"
    ),
)

test_triager = LlmAgent(
    name="test_triager",
    model=MODEL,
    tools=[make_read_file(("tests/output.log",))],
    output_key="test_findings",
    instruction=(
        "You triage test runs. Read tests/output.log only. Ignore passing tests, debug logging and "
        f"warnings. Return only the real failures and the likely cause. {BULLETS}"
    ),
)

docs_checker = LlmAgent(
    name="docs_checker",
    model=MODEL,
    tools=[make_read_file(("README.md", "app/payments.py"))],
    output_key="docs_findings",
    instruction=(
        "You check docs against code. Read README.md and app/payments.py. "
        f"Return only mismatches between them. {BULLETS}"
    ),
)

# ParallelAgent runs its sub-agents at the same time. Each branch gets its own
# isolated context, so the security reviewer never sees the 1,500 line log.
specialists = ParallelAgent(
    name="specialists",
    sub_agents=[security_reviewer, test_triager, docs_checker],
)

# The synthesiser has no tools and sees only three short summaries, read from
# session.state through the {placeholders} below.
synthesiser = LlmAgent(
    name="synthesiser",
    model=MODEL,
    instruction=(
        "Merge these specialist findings into one review report with three sections "
        "(Security, Tests, Docs). Keep each bullet's file and line. Do not invent findings.\n\n"
        "Security findings:\n{security_findings}\n\n"
        "Test findings:\n{test_findings}\n\n"
        "Docs findings:\n{docs_findings}"
    ),
)

# SequentialAgent runs every step in order, unconditionally: specialists, then synthesiser.
#
# Alternative: wrap a specialist in AgentTool and give it to a parent agent.
# The parent then calls it like a function and gets the answer back, and
# decides for itself whether to call it. Use that when delegation is optional;
# use ParallelAgent when every specialist must always run.
root_agent = SequentialAgent(name="fan_out", sub_agents=[specialists, synthesiser])
