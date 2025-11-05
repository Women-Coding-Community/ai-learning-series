# Gemini API Key Setup Guide

## Overview

This guide walks you through getting a free Gemini API key from Google AI Studio and setting it up for use in your projects.

---

## What You'll Need

- A Google account (free)
- Internet connection
- A text editor or IDE

---

## Step 1: Get Your API Key

### Option A: Quick Setup (Recommended for Beginners)

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"** button
3. Select your project (or create a new one)
4. Your API key will be displayed - **copy it immediately**
5. Store it safely (we'll use it in the next steps)

### Option B: Using Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the **Generative Language API**:
   - Search for "Generative Language API"
   - Click **Enable**
4. Go to **Credentials** → **Create Credentials** → **API Key**
5. Copy your API key

---

## Step 2: Set Up Your Environment

### Option 1: Using Environment Variables (Recommended)

Create a `.env` file in your project root:

```bash
# .env
GEMINI_API_KEY=your-api-key-here
```

Then load it in your Python code:

```python
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)
```

**Important:** Add `.env` to your `.gitignore` to keep your key secret!

```bash
# .gitignore
.env
.env.local
*.key
```

### Option 2: Direct Configuration (Not Recommended for Production)

```python
import google.generativeai as genai

genai.configure(api_key="your-api-key-here")
```

⚠️ **Warning:** Never hardcode API keys in production code or commit them to GitHub!

---

## Step 3: Install Required Package

Install the Google Generative AI Python SDK:

```bash
pip install google-generativeai
```

Or add to `requirements.txt`:

```bash
google-generativeai>=0.3.0
python-dotenv>=1.0.0
```

Then install:

```bash
pip install -r requirements.txt
```

---

## Step 4: Test Your Setup

Create a test file `test_gemini.py`:

```python
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env file")
    exit(1)

genai.configure(api_key=api_key)

# Test the API
try:
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    response = model.generate_content("Say 'Hello from Gemini!' in exactly those words.")
    print("✅ API is working!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")
```

Run the test:

```bash
python test_gemini.py
```

Expected output:

```bash
✅ API is working!
Response: Hello from Gemini!
```

---

## Available Models

### Current Models (Free Tier)

| Model | Speed | Quality | Best For |
|-------|-------|---------|----------|
| `gemini-2.5-flash-lite` | ⚡ Very Fast | Good | Chatbots, quick responses (RECOMMENDED) |
| `gemini-2.5-flash` | ⚡ Fast | Excellent | General purpose, balanced performance |
| `gemini-2.5-pro` | 🐢 Slower | Excellent | Complex tasks, analysis |

### Recommended for Session 1

Use `gemini-2.5-flash-lite` for chatbots - it's the fastest and most reliable on the free tier:

```python
model = genai.GenerativeModel('gemini-2.5-flash-lite')
```

**Note:** If you get a "model not found" error, try `gemini-2.5-flash-lite` instead. Model availability depends on your API key type and region.

---

## Basic Usage

### Simple Text Generation

```python
import google.generativeai as genai

genai.configure(api_key="your-api-key")
model = genai.GenerativeModel('gemini-2.5-flash-lite')

response = model.generate_content("What is AI?")
print(response.text)
```

### With System Prompt

```python
model = genai.GenerativeModel(
    'gemini-2.5-flash-lite',
    system_instruction="You are a helpful AI teacher. Explain concepts simply."
)
response = model.generate_content("What is AI?")
print(response.text)
```

### Streaming Responses

```python
response = model.generate_content(
    "Write a short story about AI",
    stream=True
)

for chunk in response:
    print(chunk.text, end="")
```

### With Configuration

```python
response = model.generate_content(
    "Write a creative story",
    generation_config=genai.types.GenerationConfig(
        temperature=0.9,  # More creative (0-2)
        top_p=0.95,       # Diversity
        max_output_tokens=1000
    )
)
```

---

## Troubleshooting

### Error: "Model not found" or "is not supported for generateContent"

**Cause:** The model name is not available for your API key type or region

**Solution:**

1. Try `gemini-2.5-flash-lite` (recommended for free tier):

   ```python
   model = genai.GenerativeModel('gemini-2.5-flash-lite')
   ```

2. If that doesn't work, try `gemini-2.5-flash`:

   ```python
   model = genai.GenerativeModel('gemini-2.5-flash')
   ```

3. List available models to see what's available:

   ```python
   import google.generativeai as genai
   genai.configure(api_key="your-api-key")
   for model in genai.list_models():
       print(model.name)
   ```

4. Check your API key type at [Google AI Studio](https://aistudio.google.com/app/apikey)

---

### Error: "API key not valid"

**Solution:**

1. Verify your API key is correct
2. Check it's in the `.env` file with correct format: `GEMINI_API_KEY=your-key`
3. Make sure you're not using quotes around the key in `.env`
4. Regenerate the key in Google AI Studio if needed

### Error: "RESOURCE_EXHAUSTED"

**Cause:** You've exceeded the free tier quota

**Solution:**

- Wait a few minutes and try again
- Check your usage at [Google AI Studio](https://aistudio.google.com/app/usage)
- Upgrade to a paid plan if needed

### Error: "PERMISSION_DENIED"

**Cause:** API key doesn't have permission

**Solution:**

1. Regenerate your API key
2. Make sure Generative Language API is enabled
3. Try a different project

### Error: "ModuleNotFoundError: No module named 'google'"

**Solution:**

```bash
pip install google-generativeai
```

### `.env` file not loading

**Solution:**

1. Make sure file is named `.env` (not `.env.txt`)
2. Place it in your project root directory
3. Call `load_dotenv()` before using variables
4. Check that `python-dotenv` is installed: `pip install python-dotenv`

---

## Security Best Practices

### ✅ DO

- Store API keys in environment variables
- Use `.env` files locally (not in version control)
- Regenerate keys if compromised
- Use different keys for different environments
- Implement rate limiting in your app

### ❌ DON'T

- Hardcode API keys in source code
- Commit `.env` files to GitHub
- Share API keys in chat or emails
- Use the same key for multiple projects
- Log API keys in error messages

---

## Keeping Your Key Safe

### If Your Key is Compromised

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Delete the compromised key
3. Create a new API key
4. Update your `.env` file
5. Redeploy your application

---

## Next Steps

Now that you have your API key set up:

1. ✅ Complete [Python Environment Setup](./python-environment.md)
2. ✅ Try [Vertex AI Quickstart](./vertex-ai-quickstart.md)
3. ✅ Build the [Session 1 Chatbot](../sessions/session-01-ai-chatbots/starter-template/)

---

## Resources

- [Google AI Studio](https://aistudio.google.com)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Python SDK Reference](https://ai.google.dev/tutorials/python_quickstart)
- [API Key Best Practices](https://cloud.google.com/docs/authentication/api-keys)

---

## Questions?

Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel or check [Troubleshooting Guide](../resources/troubleshooting.md)!

---

**Ready to build with Gemini? Let's go! 🚀**
