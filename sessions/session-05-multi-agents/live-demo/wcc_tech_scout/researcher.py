"""
Part A: The Researcher Agent (With Google Search)

This agent specializes in finding accurate, up-to-date information
using Google Search grounding through Vertex AI.

The Researcher is the first agent in our pipeline - it gathers
raw information that will be passed to the Editor.
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()

# =============================================================================
# Google Search Tool
# =============================================================================
# 
# In production with Vertex AI, you would use:
# from google.adk.tools import GoogleSearchTool
# 
# For this demo, we'll create a mock search tool that simulates
# the behavior. Replace with GoogleSearchTool() for production.

def google_search(query: str) -> str:
    """
    Search Google for the latest information on a topic.
    
    In production, this would use Vertex AI's Google Search Grounding.
    For the demo, we return mock results to show the pattern.
    
    Args:
        query: The search query.
        
    Returns:
        str: Search results as formatted text.
    """
    # Mock search results for demo purposes
    mock_results = {
        "agentic ai": """
**Search Results for "Agentic AI":**

1. **What is Agentic AI?** (Google AI Blog, Dec 2024)
   Agentic AI refers to AI systems that can autonomously plan, reason, 
   and take actions to achieve goals. Unlike chatbots, agents can use 
   tools, make decisions, and complete multi-step tasks.

2. **The Rise of AI Agents** (TechCrunch, Nov 2024)
   Major tech companies are investing heavily in agentic AI. Google's 
   ADK, OpenAI's Assistants API, and Anthropic's Claude all support 
   agent-based workflows.

3. **Key Trends in Agentic AI for 2025:**
   - Multi-agent orchestration (teams of specialized agents)
   - Tool use and function calling
   - Memory and context management
   - Agent-to-Agent protocols (A2A)
   - Model Context Protocol (MCP) for standardized tool access
""",
        "vertex ai agents": """
**Search Results for "Vertex AI Agents":**

1. **Vertex AI Agent Builder** (Google Cloud Docs)
   Build, deploy, and manage AI agents at scale. Features include:
   - Pre-built agent templates
   - Custom tool integration
   - Conversation memory management
   - Enterprise security and compliance

2. **Agent Development Kit (ADK)** (Google AI, 2024)
   Open-source Python SDK for building agents. Supports:
   - Multiple LLM backends (Gemini, Claude, etc.)
   - MCP tool integration
   - A2A protocol for agent communication

3. **Production Deployment:**
   - Use `adk deploy` to push to Vertex AI Agent Engine
   - Automatic scaling and state management
   - Built-in monitoring and logging
""",
        "default": """
**Search Results:**

I found several relevant articles and resources on this topic.
Key findings include recent developments, best practices, and 
industry trends. The information has been gathered from reputable
sources including official documentation, tech blogs, and research papers.
"""
    }
    
    # Find matching results
    query_lower = query.lower()
    for key, results in mock_results.items():
        if key in query_lower:
            return results
    
    return mock_results["default"]


# =============================================================================
# Researcher Agent Definition
# =============================================================================

researcher_agent = Agent(
    name="TechScout",
    model="gemini-2.0-flash",
    instruction="""You are TechScout, a tech researcher for the Women Coding Community.

YOUR ROLE:
- Find the latest, most accurate information on technology topics
- Focus on AI, programming, and career development topics
- Provide well-sourced, factual information

RESEARCH PROCESS:
1. Use the google_search tool to find current information
2. Synthesize the key findings
3. Organize information clearly with sources
4. Highlight the most important trends and insights

OUTPUT FORMAT:
Provide your research as structured notes:
- **Topic**: [The research topic]
- **Key Findings**: [Bullet points of main discoveries]
- **Sources**: [Where the information came from]
- **Trends**: [Notable patterns or predictions]

Be thorough but concise. Your research will be passed to an Editor
who will create a polished report from your notes.
""",
    tools=[google_search],
)


# =============================================================================
# Standalone Test
# =============================================================================

if __name__ == "__main__":
    # Test the researcher independently
    print("🕵️ Testing TechScout Researcher Agent...")
    print("=" * 50)
    
    # Simulate a research request
    test_query = "What is the latest on Agentic AI?"
    print(f"\n📝 Query: {test_query}\n")
    
    # In production with ADK runner:
    # from google.adk.runners import Runner
    # runner = Runner(agent=researcher_agent)
    # response = runner.run(test_query)
    
    # For demo, show the tool output directly
    results = google_search("agentic ai")
    print("🔍 Search Results:")
    print(results)
    
    print("\n" + "=" * 50)
    print("✅ Researcher agent ready for pipeline integration!")
