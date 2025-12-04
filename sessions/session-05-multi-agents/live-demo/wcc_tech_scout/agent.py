"""
WCC Tech Scout - Main Agent (For ADK Web Interface)

A research and writing assistant that demonstrates:
- ADK: How we build agents with tools
- A2A: How agents hand off work (simulated in workflow)
- MCP: How agents access external systems (file system)

Run from the live-demo folder:
    cd live-demo
    adk web

Then open http://127.0.0.1:8000, select wcc_tech_scout, and try:
    "Research the latest on Agentic AI"
    "What's new in Vertex AI Agents?"
    "Find trends in AI for 2025"
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()


# =============================================================================
# Tools - Simulating ADK + Google Search + MCP FileSystem
# =============================================================================

def google_search(query: str) -> str:
    """
    Search Google for the latest information on a topic.
    
    This simulates Vertex AI's Google Search Grounding.
    In production, use: from google.adk.tools import GoogleSearchTool
    
    Args:
        query: The search query.
        
    Returns:
        str: Search results as formatted text.
    """
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
        "vertex ai": """
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
""",
        "mcp": """
**Search Results for "Model Context Protocol":**

1. **What is MCP?** (Anthropic, 2024)
   MCP is an open standard for connecting AI models to external data 
   and tools. Think of it as "USB-C for AI" - a universal connector.

2. **Key Benefits:**
   - Vendor-agnostic: Works with any AI system
   - Secure: Standardized authentication
   - Extensible: Easy to add new tools
   
3. **Available MCP Servers:**
   - filesystem: Read/write local files
   - github: Access repositories
   - slack: Send messages
   - postgres: Query databases
""",
        "a2a": """
**Search Results for "Agent-to-Agent Protocol":**

1. **A2A Protocol** (Google, 2024)
   A2A enables AI agents to communicate with each other, regardless 
   of which framework they were built with.

2. **Use Cases:**
   - Multi-agent orchestration
   - Cross-organization agent collaboration
   - Specialized agent teams
   
3. **Key Features:**
   - Language-agnostic (Python, Java, etc.)
   - Secure communication
   - Context passing between agents
"""
    }
    
    query_lower = query.lower()
    for key, results in mock_results.items():
        if key in query_lower:
            return results
    
    return f"""
**Search Results for "{query}":**

I found several relevant articles and resources on this topic.
Key findings include recent developments, best practices, and 
industry trends. The information has been gathered from reputable
sources including official documentation and tech blogs.

To get more specific results, try searching for:
- "agentic ai" - AI agents and automation
- "vertex ai" - Google's AI platform
- "mcp" - Model Context Protocol
- "a2a" - Agent-to-Agent communication
"""


# Output directory for reports (MCP FileSystem simulation)
REPORTS_DIR = os.path.join(os.path.dirname(__file__), ".reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def write_file(filename: str, content: str) -> str:
    """
    Write content to a file (MCP FileSystem simulation).
    
    This simulates connecting to an MCP FileSystem server.
    In production, configure mcp_servers=["filesystem-server"]
    
    Args:
        filename: Name of the file to create.
        content: The content to write.
        
    Returns:
        str: Confirmation message.
    """
    filepath = os.path.join(REPORTS_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"✅ Report saved: {filename}"
    except Exception as e:
        return f"❌ Error saving file: {str(e)}"


def list_files() -> str:
    """
    List saved reports (MCP FileSystem simulation).
    
    Returns:
        str: List of files in the reports directory.
    """
    try:
        files = [f for f in os.listdir(REPORTS_DIR) if f.endswith('.md')]
        if not files:
            return "No reports saved yet."
        return "Saved reports:\n" + "\n".join(f"- {f}" for f in files)
    except Exception as e:
        return f"Error listing files: {str(e)}"


# =============================================================================
# Root Agent - WCC Tech Scout
# =============================================================================

root_agent = Agent(
    name="wcc_tech_scout",
    model="gemini-2.0-flash",
    instruction="""You are the WCC Tech Scout, a research and writing assistant 
for the Women Coding Community.

🎯 YOUR CAPABILITIES:
1. **Research** - Use google_search to find the latest tech information
2. **Write** - Create well-formatted Markdown reports
3. **Save** - Use write_file to save reports for later

📋 WORKFLOW (A2A Pattern Simulation):
When a user asks about a topic:
1. RESEARCH: Use google_search to gather information
2. SYNTHESIZE: Organize findings into a clear report
3. SAVE: Use write_file to save the report as a .md file

📝 REPORT FORMAT:
```markdown
# [Topic]: Key Insights

*Generated by WCC Tech Scout | [Date]*

## Overview
[Brief introduction]

## Key Findings
[Bullet points of main discoveries]

## Resources
[Links for further reading]

---
*Built with ADK, A2A, and MCP by Women Coding Community*
```

💡 EXAMPLE INTERACTIONS:
- "Research the latest on Agentic AI" → Search, summarize findings
- "What's new in Vertex AI?" → Search, present key points
- "Save that as a report" → Use write_file to save
- "List my saved reports" → Show saved files

⚠️ IMPORTANT: After presenting research, ASK the user if they want to save 
it as a report before using write_file. Don't save automatically.
""",
    tools=[
        google_search,
        write_file,
        list_files,
    ],
)
