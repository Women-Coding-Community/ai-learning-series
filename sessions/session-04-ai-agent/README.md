# Session 1: AI Fundamentals & LLM APIs

**Date:** November 5, 2025  
**Instructor:** Sonika  
**Duration:** 60 minutes

## 🎯 Learning Objectives

By the end of this session, you will:

- Understand AI, ML, and LLM concepts
- Set up GCP/Vertex AI and get API credentials
- Make your first API call to Gemini
- Build a basic chatbot with conversation memory
- Handle API responses and errors

## 📚 What We'll Cover

### Part 1: Concepts (10 min)

- What is AI, ML, and LLM?
- How do language models work?
- API basics and authentication

### Part 2: Live Coding Demo (20 min)

- GCP/Vertex AI setup walkthrough
- Building a basic chatbot with conversation memory
- Handling errors gracefully

### Part 3: Hands-On Activity (20 min)

- Set up your own GCP account
- Code along with the instructor
- Test and enhance the chatbot

### Part 4: Wrap-up & Homework (10 min)

- Review key concepts
- Homework assignment
- Q&A

## 📁 Folder Structure

```text
session-01-ai-chatbots/
├── README.md                    # This file
├── slides.pdf                   # Presentation slides
├── live-demo/                   # Code from live session
│   ├── basic_chatbot.py
│   ├── chatbot_with_memory.py
│   └── requirements.txt
├── starter-template/            # Template for participants
│   ├── chatbot.py
│   ├── requirements.txt
│   └── README.md
├── use-case-guides/             # Detailed guides for each use case
│   ├── wcc-info-bot.md
│   └── wcc-info-bot-advanced.md
└── participants/                # Participant submissions
    ├── username1/
    ├── username2/
    └── ...
```

## 🚀 Quick Start

### Before the Session

1. Complete [GCP Setup](../../getting-started/gcp-setup.md)
2. Complete [Python Environment Setup](../../getting-started/python-environment.md)
3. Review [Vertex AI Quickstart](../../getting-started/vertex-ai-quickstart.md)

### During the Session

1. Follow along with the live demo
2. Ask questions in the chat
3. Complete the hands-on activity

### After the Session

1. Choose a use case
2. Enhance the chatbot
3. Deploy to GitHub
4. Submit your work

## 📖 Resources

- [Slides](./slides.pdf)
- [Live Demo Code](./live-demo/)
- [Starter Template](./starter-template/)
- [Use Case Guides](./use-case-guides/)

## 🎓 Use Case Options

Pick one of these use cases or create your own! All use the same core concepts.

### Option 1: WCC Info Bot (Community Assistant)

**Problem:** New members ask repetitive questions about WCC events, membership, volunteering

**Solution:** Build a chatbot that answers FAQs about WCC with personality

**Tech Stack:**

- Gemini API for conversation
- System prompts for personality
- Conversation memory for context

**Bonus:** Add web scraping to pull latest info from WCC website

**Guide:** [WCC Info Bot Guide](./use-case-guides/wcc-info-bot.md)

---

### Option 2: Career Quick Coach

**Problem:** Members need quick career advice between mentorship sessions

**Solution:** Build an AI career coach chatbot for resume tips, interview prep, career questions

**Tech Stack:**

- Gemini API with career coaching persona
- System prompts for mentoring style
- Conversation memory for tracking goals
- Optional: Persistent memory for future reference

**Bonus:** Save conversation history, create mock interview mode, add skill assessment

**Guide:** [Career Quick Coach Guide](./use-case-guides/career-quick-coach.md)

---

### Option 3: Code Buddy (Beginner Code Helper)

**Problem:** Beginners need quick code explanations and debugging help

**Solution:** Build a friendly AI assistant that explains code and suggests fixes

**Tech Stack:**

- Gemini API with code-specific prompting
- System prompts for beginner-friendly explanations
- Code analysis and debugging support
- Optional: Syntax highlighting and formatted output

**Bonus:** Add code analysis features, error explanation database, code improvement suggestions

**Guide:** [Code Buddy Guide](./use-case-guides/code-buddy.md)

---

### Option 4: Your Own Idea

Have a different use case in mind? Go for it! The concepts are the same. Some ideas:

- Study buddy for exam prep
- Fitness coach for workout guidance
- Recipe assistant for cooking help
- Travel planner for trip recommendations
- Wellness coach for mental health support

## 📝 Homework Assignment

### Requirements

1. Choose one use case (or create your own)
2. Enhance the basic chatbot:
   - Add personality with system prompts
   - Improve error handling
   - Add at least one custom feature
3. Create a GitHub repository
4. Write a clear README explaining:
   - What your chatbot does
   - How to set it up
   - How to run it
5. Submit the link to your repo

### Submission

- Fork this repository
- Create a folder: `sessions/session-01-ai-chatbots/participants/[your-username]/`
- Add your code and README
- Submit a pull request

### Grading Criteria

- ✅ Chatbot works and responds to user input
- ✅ Conversation memory is implemented
- ✅ Error handling is present
- ✅ Code is clean and well-commented
- ✅ README is clear and complete
- ✅ At least one custom enhancement

## 🎁 Bonus Challenges

- Add web scraping to fetch real data
- Deploy to Streamlit Cloud
- Add multiple conversation threads
- Implement rate limiting
- Add logging and monitoring

## ❓ FAQ

**Q: Do I need to pay for GCP?**  
A: No! You get $300 free credits for 90 days. The free tier is generous.

**Q: Can I use a different platform?**  
A: Yes! Check [Alternative Platforms](../../getting-started/alternative-platforms.md) for guides.

**Q: What if I get stuck?**  
A: Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel or check [Troubleshooting](../../resources/troubleshooting.md).

**Q: How long will this take?**  
A: The basic chatbot takes ~30 minutes. Enhancements depend on your ideas!

## 📚 Additional Resources

- [Vertex AI Python SDK Documentation](https://cloud.google.com/python/docs/reference/aiplatform/latest)
- [Gemini API Reference](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- [Prompt Engineering Guide](../../resources/prompt-engineering-guide.md)
- [Security Checklist](../../resources/security-checklist.md)

## 🎓 Next Session

**Session 2: Prompt Engineering & Security** (November 19, 2025)

Topics:

- Advanced prompting techniques
- Security best practices
- API rate limiting and costs
- Production considerations

---

**Questions?** Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel!
