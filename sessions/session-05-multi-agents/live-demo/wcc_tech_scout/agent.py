"""
WCC Tech Scout - Main Agent (For ADK Web Interface)

This file defines the root agent for use with `adk web`.
It orchestrates the Researcher and Editor as sub-agents.

Run with:
    cd wcc_tech_scout
    adk web

Then open http://127.0.0.1:8000 and try:
    "Research the latest on Agentic AI"
    "What's new in Vertex AI Agents?"
    "Find trends in AI for 2025"
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent

# Import sub-agents
from .researcher import researcher_agent, google_search
from .editor import editor_agent, write_file, read_file, list_files

load_dotenv()


# =============================================================================
# Root Agent - Tech Scout Coordinator
# =============================================================================

root_agent = Agent(
    name="tech_scout_coordinator",
    model="gemini-2.0-flash",
    instruction="""You are the WCC Tech Scout Coordinator, managing a team of 
specialized AI agents for the Women Coding Community.

YOUR TEAM:
1. **TechScout** (@TechScout): The Researcher
   - Uses Google Search to find latest information
   - Specializes in tech topics, AI, and programming
   
2. **Editor** (@Editor): The Writer
   - Synthesizes research into polished reports
   - Uses MCP FileSystem to save reports

WORKFLOW (A2A Pattern):
When a user asks for research:
1. Route to @TechScout to gather information
2. Pass the research to @Editor to create a report
3. @Editor saves the report using MCP

EXAMPLE INTERACTIONS:

User: "Research the latest on Agentic AI"
→ TechScout researches → Editor writes report → Saved to file

User: "What's new in Vertex AI?"
→ TechScout finds info → Editor creates summary → Saved to file

GUIDELINES:
- Always use TechScout for research tasks
- Always use Editor to format and save results
- Explain what each agent is doing
- Confirm when the report is saved

This demonstrates:
- ADK: How we build agents
- A2A: How agents communicate (handoffs)
- MCP: How agents access tools (file system)
""",
    sub_agents=[
        researcher_agent,
        editor_agent,
    ],
)


# =============================================================================
# Alternative: Direct Pipeline Agent
# =============================================================================
# 
# If you want a simpler setup without sub-agents, you can create
# a single agent with all the tools:

pipeline_agent = Agent(
    name="tech_scout_pipeline",
    model="gemini-2.0-flash",
    instruction="""You are the WCC Tech Scout, a research and writing assistant.

YOUR CAPABILITIES:
1. **Research**: Use google_search to find information
2. **Write**: Create well-formatted reports
3. **Save**: Use write_file to save reports

WORKFLOW:
1. When asked about a topic, first use google_search
2. Synthesize the findings into a clear report
3. Save the report using write_file

FORMAT your reports as Markdown with:
- Clear title
- Overview section
- Key findings (bullet points)
- Resources/links
- Footer with generation info

Always save the final report to a .md file.
""",
    tools=[
        google_search,
        write_file,
        read_file,
        list_files,
    ],
)
