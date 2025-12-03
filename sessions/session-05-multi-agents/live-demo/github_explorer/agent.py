"""
GitHub Explorer Agent - MCP Concept Demo

This agent demonstrates how MCP (Model Context Protocol) would connect 
an AI agent to GitHub. It simulates MCP tools to show the pattern.

For REAL MCP integration, you would configure mcp_servers parameter.
This demo uses Python functions that mirror what MCP tools provide.

Run from live-demo folder:
    adk web

Try:
- "What repos does Women-Coding-Community have?"
- "Show me the README from ai-learning-series"
- "Search for AI agent repositories"
"""

import os
import json
import urllib.request
import urllib.error
import urllib.parse
from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()

# Get GitHub token for API calls
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


# =============================================================================
# MCP-Style Tools (Simulating what GitHub MCP Server provides)
# =============================================================================
# 
# These functions mirror the tools that the real GitHub MCP server exposes.
# In production with real MCP, you'd configure:
#   mcp_servers=[{"name": "github", "command": "npx", ...}]
# And these tools would be auto-discovered from the MCP server.

def search_repositories(query: str, language: str = "") -> str:
    """
    Search GitHub repositories (MCP-style tool).
    
    This simulates the search_repositories tool from GitHub MCP server.
    With real MCP, this would be auto-provided by the server.
    
    Args:
        query: Search keywords
        language: Optional programming language filter
        
    Returns:
        str: Search results as formatted text
    """
    if not GITHUB_TOKEN:
        return _get_mock_search_results(query)
    
    try:
        search_query = f"{query} language:{language}" if language else query
        url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(search_query)}&per_page=5"
        
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"token {GITHUB_TOKEN}")
        req.add_header("Accept", "application/vnd.github.v3+json")
        req.add_header("User-Agent", "WCC-GitHub-Explorer")
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
        if not data.get("items"):
            return f"No repositories found for '{query}'"
        
        results = [f"**GitHub Search Results for '{query}':**\n"]
        for repo in data["items"][:5]:
            results.append(f"""
📁 **{repo['full_name']}**
   ⭐ {repo['stargazers_count']} stars | 🍴 {repo['forks_count']} forks
   📝 {repo.get('description', 'No description')}
   🔗 {repo['html_url']}
""")
        return "\n".join(results)
        
    except Exception as e:
        return f"Error searching GitHub: {str(e)}\n\nUsing cached results:\n{_get_mock_search_results(query)}"


def get_repository_info(owner: str, repo: str) -> str:
    """
    Get information about a specific repository (MCP-style tool).
    
    Args:
        owner: Repository owner (e.g., "Women-Coding-Community")
        repo: Repository name (e.g., "ai-learning-series")
        
    Returns:
        str: Repository information
    """
    if not GITHUB_TOKEN:
        return _get_mock_repo_info(owner, repo)
    
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}"
        
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"token {GITHUB_TOKEN}")
        req.add_header("Accept", "application/vnd.github.v3+json")
        req.add_header("User-Agent", "WCC-GitHub-Explorer")
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        return f"""
**📁 {data['full_name']}**

📝 **Description:** {data.get('description', 'No description')}

📊 **Stats:**
- ⭐ Stars: {data['stargazers_count']}
- 🍴 Forks: {data['forks_count']}
- 👀 Watchers: {data['watchers_count']}
- 🐛 Open Issues: {data['open_issues_count']}

🔧 **Details:**
- Language: {data.get('language', 'Not specified')}
- Created: {data['created_at'][:10]}
- Updated: {data['updated_at'][:10]}
- License: {data.get('license', {}).get('name', 'Not specified') if data.get('license') else 'Not specified'}

🔗 **Links:**
- Repository: {data['html_url']}
- Homepage: {data.get('homepage') or 'Not set'}
"""
        
    except Exception as e:
        return f"Error fetching repo: {str(e)}\n\n{_get_mock_repo_info(owner, repo)}"


def get_file_contents(owner: str, repo: str, path: str = "README.md") -> str:
    """
    Get contents of a file from a repository (MCP-style tool).
    
    Args:
        owner: Repository owner
        repo: Repository name
        path: File path (default: README.md)
        
    Returns:
        str: File contents
    """
    if not GITHUB_TOKEN:
        return _get_mock_readme(owner, repo)
    
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"token {GITHUB_TOKEN}")
        req.add_header("Accept", "application/vnd.github.v3+json")
        req.add_header("User-Agent", "WCC-GitHub-Explorer")
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        if data.get("content"):
            import base64
            content = base64.b64decode(data["content"]).decode("utf-8")
            # Truncate if too long
            if len(content) > 2000:
                content = content[:2000] + "\n\n... (truncated)"
            return f"**📄 {path} from {owner}/{repo}:**\n\n```\n{content}\n```"
        
        return f"Could not read {path}"
        
    except Exception as e:
        return f"Error reading file: {str(e)}\n\n{_get_mock_readme(owner, repo)}"


def list_organization_repos(org: str) -> str:
    """
    List repositories for an organization (MCP-style tool).
    
    Args:
        org: Organization name (e.g., "Women-Coding-Community")
        
    Returns:
        str: List of repositories
    """
    if not GITHUB_TOKEN:
        return _get_mock_org_repos(org)
    
    try:
        url = f"https://api.github.com/orgs/{org}/repos?per_page=10&sort=updated"
        
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"token {GITHUB_TOKEN}")
        req.add_header("Accept", "application/vnd.github.v3+json")
        req.add_header("User-Agent", "WCC-GitHub-Explorer")
        
        with urllib.request.urlopen(req, timeout=10) as response:
            repos = json.loads(response.read().decode())
        
        if not repos:
            return f"No public repositories found for {org}"
        
        results = [f"**📚 Repositories for {org}:**\n"]
        for repo in repos[:10]:
            results.append(f"- **{repo['name']}** - {repo.get('description', 'No description')[:60]}")
        
        return "\n".join(results)
        
    except Exception as e:
        return f"Error listing repos: {str(e)}\n\n{_get_mock_org_repos(org)}"


# =============================================================================
# Mock Data (Used when no GitHub token is available)
# =============================================================================

def _get_mock_search_results(query: str) -> str:
    return f"""
**GitHub Search Results for '{query}':** (Demo Data)

📁 **google/adk-python**
   ⭐ 1.2k stars | 🍴 89 forks
   📝 Agent Development Kit for building AI agents
   🔗 https://github.com/google/adk-python

📁 **langchain-ai/langchain**
   ⭐ 75k stars | 🍴 11k forks
   📝 Building applications with LLMs through composability
   🔗 https://github.com/langchain-ai/langchain

📁 **microsoft/autogen**
   ⭐ 24k stars | 🍴 3k forks
   📝 Multi-agent conversation framework
   🔗 https://github.com/microsoft/autogen

💡 *Add GITHUB_TOKEN to .env for real-time results*
"""

def _get_mock_repo_info(owner: str, repo: str) -> str:
    if "women-coding" in owner.lower() or "wcc" in owner.lower():
        return """
**📁 Women-Coding-Community/ai-learning-series** (Demo Data)

📝 **Description:** AI/ML learning materials for WCC workshops

📊 **Stats:**
- ⭐ Stars: 45
- 🍴 Forks: 23
- 👀 Watchers: 12

🔗 https://github.com/Women-Coding-Community/ai-learning-series

💡 *Add GITHUB_TOKEN to .env for real-time data*
"""
    return f"Repository {owner}/{repo} - Add GITHUB_TOKEN for real data"

def _get_mock_readme(owner: str, repo: str) -> str:
    return f"""
**📄 README.md from {owner}/{repo}:** (Demo Data)

```markdown
# {repo}

Welcome to this repository!

## Getting Started
1. Clone the repo
2. Install dependencies
3. Run the project

## Contributing
PRs welcome!
```

💡 *Add GITHUB_TOKEN to .env to read actual file contents*
"""

def _get_mock_org_repos(org: str) -> str:
    if "women-coding" in org.lower() or "wcc" in org.lower():
        return """
**📚 Repositories for Women-Coding-Community:** (Demo Data)

- **ai-learning-series** - AI/ML workshop materials and code
- **wcc-backend** - Backend services for WCC platform
- **wcc-frontend** - Frontend web application
- **mentorship-program** - Mentorship matching system
- **community-resources** - Shared learning resources

🔗 https://github.com/Women-Coding-Community

💡 *Add GITHUB_TOKEN to .env for real-time data*
"""
    return f"Organization {org} - Add GITHUB_TOKEN for real data"


# =============================================================================
# Output directory for reports
# =============================================================================

REPORTS_DIR = os.path.join(os.path.dirname(__file__), ".reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def write_report(filename: str, content: str) -> str:
    """
    Save a report to file (MCP FileSystem style).
    
    Args:
        filename: Name of the file to save
        content: Report content
        
    Returns:
        str: Confirmation message
    """
    filepath = os.path.join(REPORTS_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"✅ Report saved: {filename}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


# =============================================================================
# MULTI-AGENT SYSTEM: Researcher + Writer
# =============================================================================

# Agent 1: GitHub Researcher (uses GitHub tools)
researcher_agent = Agent(
    name="github_researcher",
    model="gemini-2.0-flash",
    instruction="""You are the GitHub Researcher, specialized in finding 
information from GitHub repositories.

🎯 YOUR TOOLS:
- search_repositories: Search for repos by keyword
- get_repository_info: Get details about a specific repo
- get_file_contents: Read files from repos
- list_organization_repos: List repos for an organization

📋 YOUR ROLE:
1. Find relevant GitHub information based on user requests
2. Gather data from repositories
3. Present raw findings clearly

When you find information, present it in a structured format that 
the Writer agent can use to create a polished report.
""",
    tools=[
        search_repositories,
        get_repository_info,
        get_file_contents,
        list_organization_repos,
    ],
)

# Agent 2: Report Writer (creates and saves reports)
writer_agent = Agent(
    name="report_writer",
    model="gemini-2.0-flash",
    instruction="""You are the Report Writer, specialized in creating 
polished reports from research findings.

🎯 YOUR TOOLS:
- write_report: Save a report to a file

📋 YOUR ROLE:
1. Take research findings and create well-formatted reports
2. Organize information clearly with sections
3. Save reports using write_report tool

� REPORT FORMAT:
```markdown
# [Title]

*Generated by WCC GitHub Explorer | [Date]*

## Summary
[Brief overview]

## Key Findings
[Main discoveries]

## Details
[Detailed information]

## Links
[Relevant URLs]

---
*Multi-Agent Report: Researcher → Writer*
```

Always save the final report and confirm to the user.
""",
    tools=[write_report],
)


# =============================================================================
# Root Agent (Supervisor) - Coordinates the team
# =============================================================================

root_agent = Agent(
    name="github_explorer_team",
    model="gemini-2.0-flash",
    instruction="""You are the GitHub Explorer Team Coordinator, managing 
a multi-agent system with specialized agents.

🤖 YOUR TEAM:
1. **@github_researcher** - Finds information from GitHub
   - Searches repositories
   - Gets repo details and file contents
   - Lists organization repos

2. **@report_writer** - Creates polished reports
   - Formats research findings
   - Saves reports to files

📋 WORKFLOW (A2A Pattern):
When a user asks about GitHub:
1. DELEGATE to @github_researcher to gather information
2. PASS findings to @report_writer to create a report
3. CONFIRM the report was saved

💡 EXAMPLE:
User: "Research Women-Coding-Community repos and write a report"

Step 1: @github_researcher → list_organization_repos("Women-Coding-Community")
Step 2: @report_writer → creates formatted report → saves to file
Step 3: Confirm to user

🔧 THIS DEMONSTRATES:
- **ADK**: Building agents with tools
- **A2A**: Agents handing off work to each other
- **MCP**: GitHub tools (simulated MCP pattern)

For simple queries, you can use the researcher directly.
For reports, coordinate both agents.

Always explain which agent is doing what!
""",
    sub_agents=[
        researcher_agent,
        writer_agent,
    ],
)
