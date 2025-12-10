# Session 6: AI Agents evaluations & deployment

**Date:** December 10, 2025  
**Instructor:** Sonali & Sonika 
**Duration:** 60 minutes

## 🎯 Learning Objectives

By the end of this session, you will:

- Understand what are AI agents evaluation techniques and matrix
- Production checklist
- Deploy your ADK agent via google cloud Run

## 📚 What We'll Cover

- AI Agents Recap
- Why Evaluation Matters
- Types of Metrics
- Evaluation Methods
- Production Checklist
- Demo - deployment to google cloud run


## 🛠️ Technical Stack

- Python 3.11+
- Google Vertex AI / Gemini API
- Function Calling for tool integration
- Google cloud CLI
- Google Cloud Run

## 📁 Folder Structure

```text
session-04-ai-agent/
├── README.md                    # This file
├── live-demo/                   # Code from live session
│   ├── mentorship_agent
│        ├── agent.py  
|        ├── api.py
|        ├── DockerFile
|        ├── program_guidelines.txt
│        ├── requirements.txt
|        |── tools
|              └── mentorship_tools.py
├── starter-template/            # Template for participants
|   ├── .env.example
|   ├── evaluation-technique.md
│   └── README.md
|
└── participants/                # Participant submissions
    ├── username1/
    ├── username2/
    └── ...
```

## 🚀 Quick Start

### Before the Session

1. Complete [GCP Setup](../../getting-started/gcp-setup.md)
2. Complete [Python Environment Setup](../../getting-started/python-environment.md)

### During the Session

1. Follow along with the live demo
2. Ask questions in the chat
3. Complete the hands-on activity

### After the Session

1. Checkout the starter-template [README](starter-template\README.md)
2. Try to deploy your agent
3. Submit your work (PR with screenshot of deployed agent)

## 📖 Resources

- [Live Demo Code](./live-demo/)
- [Starter Template](./starter-template/)

## 📝 Homework Assignment

### Requirements

1. Choose the same agent or create a new.
2. Enhance the AI agent
3. Deploy the agent via google cloud run. (Do delete your service once tested)
4. Write a clear README explaining:
   - What your AI agent does
   - Screenhot of your agent working on google cloud run.
5. Submit the link to your repo

### Submission

- Fork this repository
- Create a folder: `sessions/session-06-deploy-agent/participants/[your-username]/`
- Add your code and README
- Submit a pull request

### Grading Criteria

- ✅ Screenshot showcasing agent deployed and responding.
- ✅ README is clear and complete


## ❓ FAQ

**Q: Do I need to pay for GCP?**  
A: No! You get $300 free credits for 90 days. The free tier is generous.

**Q: Can I use a different platform?**  
A: Yes! Check [Alternative Platforms](../../getting-started/alternative-platforms.md) for guides.

**Q: What if I get stuck?**  
A: Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel or check [Troubleshooting](../../resources/troubleshooting.md).

**Q: How long will this take?**  
A: The basic AI agent takes ~30 minutes. Enhancements depend on your ideas!

## 📚 Additional Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/get-started/)
- [Gemini API Reference](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)

---
