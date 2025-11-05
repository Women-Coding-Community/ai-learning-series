# Getting Started with WCC AI Learning Series

Welcome! This folder contains everything you need to set up your environment and get ready for the AI learning sessions.

## 📦 One-Command Setup

### Step 1: Create `.env` File

```bash
cp .env.example .env
```

Then edit `.env` and add your Gemini API key:

```bash
GEMINI_API_KEY=your-api-key-here
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs Session 1 essentials. Optional packages (alternative platforms, advanced features) are commented out - uncomment them if needed.

---

## 🚀 Quick Start (5 minutes)

### ⭐ Default Path for Session 1 (Recommended)

1. **Get API Key** → [Gemini API Key Setup](./gemini-api-key-setup.md) (2 min)
2. **Set Up Python** → [Python Environment Setup](./python-environment.md) (3 min)
3. **Test Your Setup** → Run the test script (included in Python setup guide)

✅ **This is the easiest and fastest way to get started!**

### 🏢 Advanced: Vertex AI / GCP (Production)

For production deployments or advanced features:

1. **Set Up GCP** → [GCP Setup Guide](./gcp-setup.md) (10 min)
2. **Enable Vertex AI** → [Vertex AI Quickstart](./vertex-ai-quickstart.md) (5 min)
3. **Set Up Python** → [Python Environment Setup](./python-environment.md) (3 min)

### 🌐 Alternative Platforms

Prefer a different platform? See [Alternative Platforms](./alternative-platforms.md) for:

- AWS Bedrock
- Azure OpenAI Service
- OpenAI API
- Anthropic Claude
- Cohere

---

## 📚 Setup Guides

### 1. Gemini API Key Setup ⭐ (Easiest)

**File:** [`gemini-api-key-setup.md`](./gemini-api-key-setup.md)

**What you'll do:**

- Get a free Gemini API key from Google AI Studio
- Set up environment variables
- Test your API connection
- Learn about available models

**Time:** ~5 minutes  
**Cost:** Free (with generous rate limits)  
**Best for:** Quick prototyping, beginners

---

### 2. Python Environment Setup

**File:** [`python-environment.md`](./python-environment.md)

**What you'll do:**

- Create a Python virtual environment
- Install required packages from root `requirements.txt`
- Set up your IDE
- Verify installation

**Time:** ~5 minutes  
**Prerequisites:** Python 3.11+ installed  
**Required for:** All projects

**Quick Install:**

```bash
pip install -r requirements.txt
```

---

### 3. GCP & Vertex AI Setup

**File:** [`gcp-setup.md`](./gcp-setup.md)

**What you'll do:**

- Create a Google Cloud project
- Enable Vertex AI API
- Create a service account
- Set up authentication

**Time:** ~10 minutes  
**Cost:** Free tier available ($300 credits)  
**Best for:** Production deployments, enterprise use

---

### 4. Vertex AI Quickstart

**File:** [`vertex-ai-quickstart.md`](./vertex-ai-quickstart.md)

**What you'll do:**

- Make your first Vertex AI API call
- Learn about Gemini models on Vertex AI
- Handle API responses
- Implement error handling

**Time:** ~5 minutes  
**Prerequisites:** GCP setup complete  
**Best for:** GCP users

---

### 5. Alternative Platforms

**File:** [`alternative-platforms.md`](./alternative-platforms.md)

**Platforms covered:**

- AWS Bedrock
- Azure OpenAI Service
- OpenAI API
- Anthropic Claude
- Cohere

**What you'll do:**

- Set up your preferred platform
- Make your first API call
- Compare platforms
- Choose what's best for you

**Time:** ~10 minutes per platform  
**Cost:** Varies by platform  
**Best for:** Exploring options

---

## 🎯 Recommended Learning Paths

### ⭐ Path 1: Fastest Start (Recommended for Session 1)

```text
1. Gemini API Key Setup (2 min)
   ↓
2. Python Environment Setup (3 min)
   ↓
3. Ready for Session 1! 🎉
```

**Total time:** ~5 minutes  
**Best for:** Beginners, quick start, Session 1

---

### 🏢 Path 2: Production Ready (GCP/Vertex AI)

```text
1. GCP Setup (10 min)
   ↓
2. Vertex AI Quickstart (5 min)
   ↓
3. Python Environment Setup (3 min)
   ↓
4. Ready for advanced features! 🚀
```

**Total time:** ~18 minutes  
**Best for:** Production deployments, enterprise use

---

### 🌐 Path 3: Platform Exploration

```text
1. Gemini API Setup (2 min)
   ↓
2. Python Environment Setup (3 min)
   ↓
3. Alternative Platforms (10-20 min)
   ↓
4. Choose your preferred platform
   ↓
5. Ready for Session 1! 🎉
```

**Total time:** ~30-40 minutes  
**Best for:** Comparing options, exploring alternatives

---

## ✅ Setup Checklist

Before Session 1, make sure you have:

- [ ] **API Key** - Gemini, Vertex AI, or alternative platform
- [ ] **Python 3.11+** - Installed and working
- [ ] **Virtual Environment** - Created and activated
- [ ] **Dependencies Installed** - `pip install -r requirements.txt`
- [ ] **API Key Configured** - In `.env` file or environment variables
- [ ] **Test Script Passed** - Successfully called the API
- [ ] **IDE Set Up** - VS Code, PyCharm, or your preferred editor

---

## 🔑 Key Concepts

### API Keys

An API key is like a password that lets you use AI services. Keep it secret!

- ✅ Store in `.env` file (not in code)
- ✅ Add `.env` to `.gitignore`
- ✅ Regenerate if compromised
- ❌ Never commit to GitHub
- ❌ Never share in chat or email

### Virtual Environments

Virtual environments isolate your project dependencies.

```bash
# Create
python -m venv venv

# Activate (Windows Git Bash)
source venv/Scripts/activate

# Activate (Mac/Linux)
source venv/bin/activate

# Deactivate
deactivate
```

### Environment Variables

Store sensitive data outside your code:

```bash
# .env file
GEMINI_API_KEY=your-key-here
GCP_PROJECT_ID=your-project-id
```

Load in Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
```

---

## 🆘 Troubleshooting

### "Python: command not found"

**Solution:**

- Install Python from [python.org](https://python.org)
- Or use `python3` instead of `python`
- Check PATH environment variable

### "ModuleNotFoundError: No module named 'google'"

**Solution:**

```bash
pip install google-generativeai
```

### "API key not valid"

**Solution:**

1. Get a new API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Update your `.env` file
3. Restart your application

### ".env file not loading"

**Solution:**

1. Make sure file is named `.env` (not `.env.txt`)
2. Place in project root directory
3. Call `load_dotenv()` before using variables
4. Install `python-dotenv`: `pip install python-dotenv`

---

## 📖 Next Steps

Once you've completed setup:

1. **Review the Starter Template** → `sessions/session-01-ai-chatbots/starter-template/`
2. **Watch the Live Demo** → `sessions/session-01-ai-chatbots/live-demo/`
3. **Read the Resources** → `resources/prompt-engineering-guide.md`
4. **Attend Session 1** → November 5, 2025

---

## 🤝 Need Help?

- **Setup Issues?** → Check [Troubleshooting Guide](../resources/troubleshooting.md)
- **API Questions?** → See specific platform guide above
- **Still Stuck?** → Ask in [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7)

---

## 📚 Additional Resources

- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Environment Variables Best Practices](https://12factor.net/config)

---

## 🎓 Learning Outcomes

After completing setup, you'll be able to:

✅ Authenticate with your chosen AI platform  
✅ Make API calls from Python  
✅ Handle API responses  
✅ Manage environment variables securely  
✅ Set up projects for development  

---

**Ready to get started? Pick a setup guide above and let's go! 🚀**
