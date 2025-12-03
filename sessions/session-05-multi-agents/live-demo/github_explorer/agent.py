"""
GitHub Explorer Agent - MCP Pattern Demo with State Management

This agent demonstrates:
- MCP (Model Context Protocol) tool patterns
- State management between agent calls
- Remembering searches and bookmarks across conversation

Run from live-demo folder:
    adk web

Try:
- "Search GitHub for AI agents"
- "Bookmark the first result"
- "What have I searched for?"
- "Show my bookmarks"
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext

load_dotenv()

# Get GitHub token for API calls (optional)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Directory for file operations
REPORTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".reports"))
os.makedirs(REPORTS_DIR, exist_ok=True)

print(f"📁 Reports directory: {REPORTS_DIR}")
if GITHUB_TOKEN:
    print("✅ GITHUB_TOKEN found - GitHub API enabled")
else:
    print("⚠️  GITHUB_TOKEN not found - using demo data")


# =============================================================================
# MCP-STYLE TOOLS WITH STATE MANAGEMENT
# =============================================================================

def list_directory(path: str = ".") -> str:
    """List files in a directory (MCP FileSystem pattern)."""
    try:
        target = os.path.join(REPORTS_DIR, path) if path != "." else REPORTS_DIR
        items = os.listdir(target)
        if not items:
            return "📁 Directory is empty"
        result = ["📁 Files:"]
        for item in sorted(items):
            full_path = os.path.join(target, item)
            if os.path.isdir(full_path):
                result.append(f"  📂 {item}/")
            else:
                size = os.path.getsize(full_path)
                result.append(f"  📄 {item} ({size} bytes)")
        return "\n".join(result)
    except Exception as e:
        return f"Error: {e}"


def read_file(path: str) -> str:
    """Read a file's contents (MCP FileSystem pattern)."""
    try:
        with open(os.path.join(REPORTS_DIR, path), 'r', encoding='utf-8') as f:
            return f"📄 {path}:\n\n{f.read()}"
    except FileNotFoundError:
        return f"File not found: {path}"
    except Exception as e:
        return f"Error: {e}"


def write_file(path: str, content: str) -> str:
    """Write content to a file (MCP FileSystem pattern)."""
    try:
        with open(os.path.join(REPORTS_DIR, path), 'w', encoding='utf-8') as f:
            f.write(content)
        return f"✅ Saved: {path}"
    except Exception as e:
        return f"❌ Error: {e}"


def search_repositories(query: str, tool_context: ToolContext) -> str:
    """
    Search GitHub repositories and remember the search.
    
    State: Stores search history and last results for bookmarking.
    """
    # Store search in history
    history = tool_context.state.get("search_history", [])
    history.append({"query": query, "time": datetime.now().isoformat()})
    tool_context.state["search_history"] = history
    
    if not GITHUB_TOKEN:
        # Demo data
        results = [
            {"full_name": "google/adk-python", "stars": 1200, "desc": "Agent Development Kit"},
            {"full_name": "langchain-ai/langchain", "stars": 75000, "desc": "LLM framework"},
        ]
        tool_context.state["last_search_results"] = results
        return f"🔍 Search '{query}' (Demo)\n\n" + "\n".join(
            f"{i+1}. � {r['full_name']} ⭐{r['stars']}\n   {r['desc']}" 
            for i, r in enumerate(results)
        ) + "\n\n�💡 Add GITHUB_TOKEN for real results"
    
    try:
        url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&per_page=5"
        req = urllib.request.Request(url, headers={
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "WCC-GitHub-Explorer"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        
        if not data.get("items"):
            return f"No results for '{query}'"
        
        # Store results for bookmarking
        results = [
            {"full_name": r["full_name"], "stars": r["stargazers_count"], 
             "desc": r.get("description", "")[:60], "url": r["html_url"]}
            for r in data["items"][:5]
        ]
        tool_context.state["last_search_results"] = results
        
        output = [f"🔍 GitHub: '{query}'\n"]
        for i, r in enumerate(results):
            output.append(f"{i+1}. 📁 **{r['full_name']}** ⭐{r['stars']}\n   {r['desc']}")
        output.append("\n💡 Say 'bookmark #1' to save a result")
        return "\n".join(output)
    except Exception as e:
        return f"Error: {e}"


def bookmark_repo(number: int, tool_context: ToolContext) -> str:
    """
    Bookmark a repository from the last search results.
    
    State: Reads last_search_results, writes to bookmarks.
    """
    results = tool_context.state.get("last_search_results", [])
    if not results:
        return "❌ No search results to bookmark. Search first!"
    
    if number < 1 or number > len(results):
        return f"❌ Invalid number. Choose 1-{len(results)}"
    
    repo = results[number - 1]
    bookmarks = tool_context.state.get("bookmarks", [])
    
    # Check if already bookmarked
    if any(b["full_name"] == repo["full_name"] for b in bookmarks):
        return f"📌 Already bookmarked: {repo['full_name']}"
    
    bookmarks.append({
        "full_name": repo["full_name"],
        "stars": repo["stars"],
        "desc": repo.get("desc", ""),
        "bookmarked_at": datetime.now().isoformat()
    })
    tool_context.state["bookmarks"] = bookmarks
    
    return f"📌 Bookmarked: {repo['full_name']}"


def show_bookmarks(tool_context: ToolContext) -> str:
    """
    Show all bookmarked repositories.
    
    State: Reads from bookmarks.
    """
    bookmarks = tool_context.state.get("bookmarks", [])
    if not bookmarks:
        return "📌 No bookmarks yet. Search and bookmark repos!"
    
    output = ["📌 **Your Bookmarks:**\n"]
    for i, b in enumerate(bookmarks, 1):
        output.append(f"{i}. 📁 {b['full_name']} ⭐{b['stars']}")
    return "\n".join(output)


def show_search_history(tool_context: ToolContext) -> str:
    """
    Show search history.
    
    State: Reads from search_history.
    """
    history = tool_context.state.get("search_history", [])
    if not history:
        return "📜 No searches yet."
    
    output = ["📜 **Search History:**\n"]
    for h in history[-10:]:  # Last 10 searches
        time = h["time"][:16].replace("T", " ")
        output.append(f"- '{h['query']}' ({time})")
    return "\n".join(output)


def clear_state(tool_context: ToolContext) -> str:
    """Clear all stored state (bookmarks, history)."""
    tool_context.state.clear()
    return "🗑️ Cleared all bookmarks and history"


def get_repository(owner: str, repo: str) -> str:
    """Get repository info (MCP GitHub pattern)."""
    if not GITHUB_TOKEN:
        return f"📁 {owner}/{repo} (Demo)\n\n💡 Add GITHUB_TOKEN for real data"
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}"
        req = urllib.request.Request(url, headers={
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "WCC-GitHub-Explorer"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            d = json.loads(resp.read().decode())
        return f"📁 **{d['full_name']}**\n\n{d.get('description','')}\n\n⭐ {d['stargazers_count']} | 🍴 {d['forks_count']}\n\n🔗 {d['html_url']}"
    except Exception as e:
        return f"Error: {e}"


# =============================================================================
# Root Agent with State-Aware Tools
# =============================================================================

root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="github_explorer",
    instruction="""You are the GitHub Explorer with memory! You remember searches and bookmarks.

🎯 TOOLS:

**File Operations:**
- list_directory: List files
- read_file: Read a file
- write_file: Create/update a file

**GitHub Operations:**
- search_repositories: Search GitHub (remembers results)
- get_repository: Get repo details
- bookmark_repo: Bookmark a search result by number
- show_bookmarks: Show saved bookmarks
- show_search_history: Show past searches
- clear_state: Clear all memory

📋 EXAMPLES:
- "Search GitHub for AI agents" → search, results numbered 1-5
- "Bookmark number 2" → bookmark_repo(2)
- "What have I searched for?" → show_search_history()
- "Show my bookmarks" → show_bookmarks()

🧠 STATE MANAGEMENT:
You maintain state across the conversation:
- Search history is remembered
- Last search results available for bookmarking
- Bookmarks persist until cleared

Always explain what you're doing!
""",
    tools=[
        list_directory, 
        read_file, 
        write_file, 
        search_repositories, 
        get_repository,
        bookmark_repo,
        show_bookmarks,
        show_search_history,
        clear_state,
    ],
)


# =============================================================================
# REAL MCP CONFIG (for production - requires Node.js + working npx)
# =============================================================================
# from google.adk.tools.mcp_tool import McpToolset
# from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
# from mcp import StdioServerParameters
#
# filesystem_mcp = McpToolset(
#     connection_params=StdioConnectionParams(
#         server_params=StdioServerParameters(
#             command="npx",
#             args=["-y", "@modelcontextprotocol/server-filesystem", REPORTS_DIR],
#         ),
#     ),
# )
# root_agent = LlmAgent(..., tools=[filesystem_mcp])
