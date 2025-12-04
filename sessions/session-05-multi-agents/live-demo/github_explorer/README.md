# GitHub Explorer - Multi-Agent MCP Demo

This agent demonstrates a **multi-agent system** that explores GitHub repositories, showing ADK, A2A, and MCP concepts working together.

## 🎯 What This Demonstrates

- **ADK**: Building agents with specialized tools
- **A2A**: Researcher agent hands off to Writer agent
- **MCP**: GitHub tools (simulating MCP pattern)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Request                              │
│   "Research WCC repos and write a report"                    │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              SUPERVISOR (github_explorer_team)               │
│                   Coordinates the workflow                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
┌─────────────────┐         ┌─────────────────┐
│   RESEARCHER    │   A2A   │     WRITER      │
│ (GitHub tools)  │ ──────▶ │ (Report tools)  │
│                 │ handoff │                 │
│ - search_repos  │         │ - write_report  │
│ - get_info      │         │                 │
│ - get_file      │         │                 │
└─────────────────┘         └─────────────────┘
         │                           │
         │                           ▼
         │                  ┌─────────────────┐
         │                  │  .reports/      │
         │                  │  report.md      │
         └──────────────────┴─────────────────┘
```

## 🚀 Setup

### 1. Prerequisites

```bash
# Python 3.11+
python --version

# Optional: GitHub token for real API access
# Without token, demo data is used
```

### 2. Get a GitHub Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:user`
4. Copy the token

### 3. Add Token to .env

```bash
# In ai-learning-series/.env
GITHUB_TOKEN=ghp_your_token_here
```

### 4. Run the Agent

```bash
cd sessions/session-05-multi-agents/live-demo
adk web
```

Select **github_explorer** from the dropdown.

## 💬 Try These Prompts

**Simple queries (Researcher only):**
```
"What repos does Women-Coding-Community have?"

"Show me the README from Women-Coding-Community/ai-learning-series"

"Search for Python AI agent repositories"
```

**Multi-agent workflow (Researcher → Writer):**
```
"Research Women-Coding-Community repos and write a report"

"Find AI agent repos and create a summary report"

"Explore the ai-learning-series repo and save a report"
```

## 🤖 The Agents

### 1. Supervisor (`github_explorer_team`)
- Coordinates the workflow
- Decides which agent to use
- Manages handoffs between agents

### 2. Researcher (`github_researcher`)
- **Tools**: `search_repositories`, `get_repository_info`, `get_file_contents`, `list_organization_repos`
- Finds information from GitHub
- Presents raw findings

### 3. Writer (`report_writer`)
- **Tools**: `write_report`
- Creates polished reports from research
- Saves reports to `.reports/` folder

## 🔧 How It Works

### MCP-Style Tools
The GitHub tools simulate what an MCP server would provide:

```python
# These tools mirror MCP GitHub server capabilities
tools=[
    search_repositories,      # Search repos by keyword
    get_repository_info,      # Get repo details
    get_file_contents,        # Read files (README, etc.)
    list_organization_repos,  # List org repos
]
```

### Real MCP Configuration (Reference)
In production with real MCP, you'd configure:

```python
mcp_servers=[
    {
        "name": "github",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "token"}
    }
]
```

## 🔄 Available MCP Servers

| Server | What It Does | Install |
|--------|--------------|---------|
| **github** | Access GitHub repos | `@modelcontextprotocol/server-github` |
| **filesystem** | Read/write local files | `@modelcontextprotocol/server-filesystem` |
| **google-drive** | Access Google Drive | `@modelcontextprotocol/server-gdrive` |
| **slack** | Send Slack messages | `@modelcontextprotocol/server-slack` |

See all: https://github.com/modelcontextprotocol/servers

## 📁 A2A Agent Cards

This demo includes proper A2A configuration files:

```
github_explorer/
├── agent.yaml              # Main agent card (supervisor)
├── agent.py                # Python implementation
├── agents/
│   ├── researcher.yaml     # Researcher agent card
│   └── writer.yaml         # Writer agent card
└── .reports/               # Output directory
```

### What's in agent.yaml?

```yaml
# A2A Agent Card - describes capabilities for discovery
name: github_explorer_team
capabilities:
  - name: search_github
    description: Search GitHub repositories
    input_schema: { ... }
  - name: create_report
    description: Research and create a report

sub_agents:
  - name: github_researcher
  - name: report_writer
```

A2A agent cards allow:
- **Discovery**: Other agents can find and understand this agent
- **Interoperability**: Works with agents built in different frameworks
- **Schema Definition**: Clear input/output contracts

## 🎓 Key Teaching Points

1. **Multi-Agent Pattern**: Supervisor coordinates specialized agents
2. **A2A Protocol**: Agent cards define capabilities for discovery
3. **MCP Concept**: Standardized tools that work across AI systems
4. **Specialization**: Each agent has focused responsibilities

## ❓ Troubleshooting

### "MCP server not found"
```bash
# Make sure Node.js is installed
node --version

# Test the MCP server manually
npx -y @modelcontextprotocol/server-github
```

### "Authentication failed"
- Check your GITHUB_TOKEN in .env
- Make sure the token has correct scopes
- Token might have expired

### "Command not found: npx"
```bash
# Install Node.js from https://nodejs.org
# Or use a package manager:
winget install OpenJS.NodeJS  # Windows
brew install node              # Mac
```

## 📚 Resources

- [MCP Official Site](https://modelcontextprotocol.io/)
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [GitHub MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/github)
- [ADK MCP Documentation](https://google.github.io/adk-docs/)

---

**This is real MCP in action! 🚀**
