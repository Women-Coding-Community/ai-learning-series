# Repository Structure Overview

## Complete Directory Layout

```text
wcc-ai-learning-series/
│
├── README.md                                    # Main repository overview
├── STRUCTURE.md                                 # This file
│
├── getting-started/                             # Setup & onboarding guides
│   ├── gcp-setup.md                            # GCP project & Vertex AI setup
│   ├── vertex-ai-quickstart.md                 # First API call tutorial
│   ├── python-environment.md                   # Python venv & dependencies
│   └── alternative-platforms.md                # AWS, Azure, OpenAI guides
│
├── sessions/                                    # Session materials
│   ├── session-01-ai-chatbots/                 # Session 1: AI Fundamentals & LLM APIs
│   │   ├── README.md                           # Session overview & learning objectives
│   │   ├── slides.pdf                          # Presentation slides (to be added)
│   │   │
│   │   ├── live-demo/                          # Code from live session
│   │   │   ├── basic_chatbot.py               # (to be added)
│   │   │   ├── chatbot_with_memory.py         # (to be added)
│   │   │   └── requirements.txt               # (to be added)
│   │   │
│   │   ├── starter-template/                   # Template for participants
│   │   │   ├── chatbot.py                     # Basic chatbot implementation
│   │   │   ├── requirements.txt               # Dependencies
│   │   │   └── README.md                      # Quick start guide
│   │   │
│   │   ├── use-case-guides/                    # Detailed implementation guides
│   │   │   ├── wcc-info-bot.md                # WCC Info Bot guide
│   │   │   └── wcc-info-bot-advanced.md       # (to be added)
│   │   │
│   │   └── participants/                       # Participant submissions
│   │       ├── username1/
│   │       │   ├── code/
│   │       │   ├── README.md
│   │       │   └── demo.mp4
│   │       └── username2/
│   │
│   ├── session-02-prompt-security/             # Session 2: Prompt Engineering & Security
│   ├── session-03-rag/                         # Session 3: Introduction to RAG
│   ├── session-04-agents-1/                    # Session 4: AI Agents - Part 1
│   ├── session-05-agents-2/                    # Session 5: AI Agents - Part 2
│   └── session-06-evaluation/                  # Session 6: Evaluation & Monitoring
│
├── resources/                                   # Reference materials
│   ├── gcp-vertex-ai-cheatsheet.md            # (to be added)
│   ├── prompt-engineering-guide.md             # Prompt engineering best practices
│   ├── security-checklist.md                   # Security best practices
│   ├── troubleshooting.md                      # Common issues & solutions
│   └── reading-list.md                         # Learning resources & references
│
└── badges/                                      # Participation tracking
    ├── badge-criteria.md                       # Badge requirements & grading
    └── badge-images/                           # Badge images (to be added)
```

## File Status

### ✅ Completed Files

**Root Level:**

- `README.md` - Main overview with program details

**Getting Started:**

- `getting-started/gcp-setup.md` - Complete GCP setup guide
- `getting-started/vertex-ai-quickstart.md` - API quickstart
- `getting-started/python-environment.md` - Python setup
- `getting-started/alternative-platforms.md` - Platform alternatives

**Session 1:**

- `sessions/session-01-ai-chatbots/README.md` - Session overview
- `sessions/session-01-ai-chatbots/starter-template/chatbot.py` - Basic chatbot
- `sessions/session-01-ai-chatbots/starter-template/requirements.txt` - Dependencies
- `sessions/session-01-ai-chatbots/starter-template/README.md` - Template guide
- `sessions/session-01-ai-chatbots/use-case-guides/wcc-info-bot.md` - WCC Info Bot guide
- `sessions/session-01-ai-chatbots/use-case-guides/career-quick-coach.md` - Career Coach guide
- `sessions/session-01-ai-chatbots/use-case-guides/code-buddy.md` - Code Buddy guide

**Resources:**

- `resources/prompt-engineering-guide.md` - Prompt engineering guide
- `resources/security-checklist.md` - Security best practices
- `resources/troubleshooting.md` - Troubleshooting guide
- `resources/reading-list.md` - Learning resources

**Badges:**

- `badges/badge-criteria.md` - Badge system & criteria

### 📝 To Be Added

**Session 1 Live Demo:**

- `sessions/session-01-ai-chatbots/live-demo/basic_chatbot.py`
- `sessions/session-01-ai-chatbots/live-demo/chatbot_with_memory.py`
- `sessions/session-01-ai-chatbots/live-demo/requirements.txt`

**Session 1 Additional:**

- `sessions/session-01-ai-chatbots/slides.pdf`
- `sessions/session-01-ai-chatbots/use-case-guides/wcc-info-bot-advanced.md`

**Resources:**

- `resources/gcp-vertex-ai-cheatsheet.md`

**Badges:**

- `badges/badge-images/` - Badge image files

**Future Sessions:**

- Session 2-6 folder structures (ready to be populated)

---

## Quick Navigation

### For Participants

- **Getting Started:** `getting-started/` - Setup guides
- **Session Materials:** `sessions/session-01-ai-chatbots/` - Starter template & guides
- **Resources:** `resources/` - Reference materials
- **Badges:** `badges/badge-criteria.md` - Participation tracking

### For Instructors

- **Session Overview:** `sessions/session-01-ai-chatbots/README.md`
- **Live Demo Code:** `sessions/session-01-ai-chatbots/live-demo/`
- **Starter Template:** `sessions/session-01-ai-chatbots/starter-template/`
- **Use Case Guides:** `sessions/session-01-ai-chatbots/use-case-guides/`
- **Participant Submissions:** `sessions/session-01-ai-chatbots/participants/`

---

## Key Features

### 📚 Comprehensive Documentation

- Setup guides for GCP, Python, and alternatives
- Detailed session materials with learning objectives
- Use case guides with step-by-step implementation
- Troubleshooting guide for common issues

### 🛠️ Ready-to-Use Templates

- Starter chatbot code with conversation memory
- Error handling and best practices
- Requirements.txt for easy setup
- Clear README with quick start instructions

### 🎓 Learning Resources

- Prompt engineering best practices
- Security checklist for AI applications
- Curated reading list with links
- Badge system for participation tracking

### 🤝 Community-Focused

- Participant submission structure
- Collaboration guidelines
- Badge system for motivation
- Multiple use case options

---

## Getting Started

### For New Participants

1. Read `README.md` for overview
2. Follow `getting-started/gcp-setup.md`
3. Complete `getting-started/python-environment.md`
4. Try `getting-started/vertex-ai-quickstart.md`
5. Use `sessions/session-01-ai-chatbots/starter-template/`

### For Instructors

1. Review `sessions/session-01-ai-chatbots/README.md`
2. Prepare slides (add to `slides.pdf`)
3. Review starter template and use case guides
4. Set up participant submission folders
5. Share resources from `resources/` folder

---

## Session Timeline

| Session | Date | Topic | Status |
|---------|------|-------|--------|
| 1 | Nov 5, 2025 | AI Fundamentals & LLM APIs | ✅ Ready |
| 2 | Nov 19, 2025 | Prompt Engineering & Security | 📋 Planned |
| 3 | Dec 3, 2025 | Introduction to RAG | 📋 Planned |
| 4 | Dec 17, 2025 | AI Agents - Part 1 | 📋 Planned |
| 5 | Jan 7, 2026 | AI Agents - Part 2 | 📋 Planned |
| 6 | Jan 21, 2026 | Evaluation & Monitoring | 📋 Planned |

---

## Contributing

To add content:

1. Create files in appropriate folders
2. Follow existing documentation style
3. Include clear examples and instructions
4. Test code before committing
5. Submit PR with description

---

## Support

- **Questions?** Ask in [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7)
- **Issues?** Check `resources/troubleshooting.md`
- **Resources?** See `resources/reading-list.md`
- **Feedback?** Create an issue or PR

---

**Last Updated:** November 2025  
**Repository:** Women Coding Community - AI Learning Series
