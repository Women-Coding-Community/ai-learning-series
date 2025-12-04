"""
Multi-Agent System Starter - Main Orchestration

This file sets up the supervisor agent that coordinates
the team of specialist agents.

To add more specialists:
1. Create a new agent file in agents/
2. Import it here
3. Add it to the sub_agents list
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent

# Import your specialist agents
from .agents import specialist_agent

# Load environment variables
load_dotenv()


# =============================================================================
# Supervisor Agent
# =============================================================================

root_agent = Agent(
    name="supervisor",
    model="gemini-2.0-flash",
    instruction="""You are a Supervisor Agent coordinating a team of specialists.

YOUR ROLE:
- Understand incoming requests
- Route tasks to the appropriate specialist
- Coordinate multi-step workflows
- Compile results from specialists

YOUR TEAM:
1. **Specialist** (@specialist): Handles general tasks and information requests

ROUTING GUIDELINES:
- Analyze what the user needs
- Determine which specialist is best suited
- Transfer the request with clear context
- Follow up if multiple steps are needed

HOW TO ADD MORE SPECIALISTS:
This is a starter template. To expand your team:
1. Create new agent files in the agents/ folder
2. Import them in this file
3. Add them to the sub_agents list below
4. Update this instruction to include them

EXAMPLE SPECIALISTS YOU COULD ADD:
- Researcher: Finds and summarizes information
- Writer: Creates content and documentation  
- Analyzer: Analyzes data and provides insights
- Planner: Creates plans and schedules

WORKFLOW:
1. Receive user request
2. Determine which specialist(s) to involve
3. Route to specialist with context
4. Compile and return results
5. Suggest next steps if applicable

Be helpful, efficient, and clear about which specialist is handling each task.
""",
    sub_agents=[
        specialist_agent,
        # Add more specialists here as you create them:
        # researcher_agent,
        # writer_agent,
        # analyzer_agent,
    ],
)


# =============================================================================
# Tips for Building Your Multi-Agent System
# =============================================================================
#
# 1. START SIMPLE
#    Begin with 2 agents (supervisor + 1 specialist)
#    Add more as you understand the patterns
#
# 2. CLEAR RESPONSIBILITIES
#    Each agent should have a focused role
#    Avoid overlap between specialists
#
# 3. GOOD INSTRUCTIONS
#    Write clear, specific instructions for each agent
#    Include examples of what they should handle
#
# 4. USEFUL TOOLS
#    Give each agent tools relevant to their role
#    Shared tools can be imported by multiple agents
#
# 5. TEST WORKFLOWS
#    Try different scenarios to see how agents collaborate
#    Look for gaps in coverage or routing issues
#
# 6. ITERATE
#    Refine instructions based on how agents perform
#    Add specialists as you identify new needs
