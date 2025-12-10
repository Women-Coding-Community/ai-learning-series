"""
Specialist Agent Template

This is a template for creating specialized agents.
Duplicate this file and customize for your use case.
"""

from google.adk.agents import Agent


# =============================================================================
# Example Tool - Replace with your own tools
# =============================================================================

def example_tool(input_text: str) -> str:
    """
    An example tool that the agent can use.
    
    Args:
        input_text: The input to process.
        
    Returns:
        str: The processed result.
    """
    return f"Processed: {input_text}"


def get_information(topic: str) -> str:
    """
    Get information about a topic.
    
    Args:
        topic: The topic to look up.
        
    Returns:
        str: Information about the topic.
    """
    # Replace with your actual implementation
    info_db = {
        "python": "Python is a versatile programming language great for beginners and experts alike.",
        "ai": "AI (Artificial Intelligence) enables machines to learn and make decisions.",
        "agents": "AI Agents are systems that can perceive, reason, and act autonomously.",
    }
    
    topic_lower = topic.lower()
    for key, value in info_db.items():
        if key in topic_lower:
            return value
    
    return f"I don't have specific information about '{topic}', but I can help you explore it!"


# =============================================================================
# Specialist Agent Definition
# =============================================================================

specialist_agent = Agent(
    name="specialist",
    model="gemini-2.0-flash",
    instruction="""You are a Specialist Agent.

YOUR ROLE:
- Handle specific tasks assigned by the supervisor
- Use your tools to accomplish tasks
- Provide clear, helpful responses

GUIDELINES:
- Be thorough but concise
- Use available tools when appropriate
- Ask for clarification if needed
- Report back with clear results

CUSTOMIZE THIS:
Replace this instruction with your specialist's specific role and guidelines.
For example:
- Research Specialist: Finds and summarizes information
- Writer Specialist: Creates content and documentation
- Analyzer Specialist: Analyzes data and provides insights
""",
    tools=[
        example_tool,
        get_information,
    ],
)


# =============================================================================
# Template for Additional Specialists
# =============================================================================
#
# Copy this template to create more specialists:
#
# another_specialist = Agent(
#     name="another_specialist",
#     model="gemini-2.0-flash",
#     instruction="""Your specialist instructions here...""",
#     tools=[your_tools_here],
# )
#
# Don't forget to:
# 1. Add to __init__.py exports
# 2. Import in agent.py
# 3. Add to supervisor's sub_agents list
