# Troubleshooting Guide

## Common Issues and Solutions

### GCP & Vertex AI

#### "Permission denied" Error

**Symptoms:** `google.api_core.exceptions.PermissionDenied`

**Causes:**

- Service account lacks required roles
- Wrong project ID
- Credentials not set up

**Solutions:**

1. Verify service account has correct roles:
   - Go to GCP Console → IAM & Admin
   - Find your service account
   - Ensure it has "Vertex AI User" and "Vertex AI Service Agent" roles

2. Check environment variable:

   ```bash
   echo $GOOGLE_APPLICATION_CREDENTIALS
   ```

3. Verify project ID:

   ```python
   import os
   print(os.getenv("GCP_PROJECT_ID"))
   ```

#### "API not enabled" Error

**Symptoms:** `google.api_core.exceptions.NotFound`

**Solution:**

1. Go to GCP Console → APIs & Services → Library
2. Search for "Vertex AI API"
3. Click and press "ENABLE"
4. Wait 1-2 minutes for activation

#### "Model not found" Error

**Symptoms:** Model name not recognized

**Solution:**
Use valid model names:

- `gemini-2.5-flash-lite` (recommended for free tier)
- `gemini-2.5-flash`
- `gemini-2.5-pro`

```python
# Verify model name
from vertexai.generative_models import GenerativeModel

try:
    model = GenerativeModel("gemini-2.5-flash-lite")
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Error: {e}")
```

#### "Project not found" Error

**Symptoms:** `google.api_core.exceptions.NotFound: 404`

**Solutions:**

1. Verify project ID is correct:

   ```bash
   gcloud config get-value project
   ```

2. Check `.env` file:

   ```bash
   GCP_PROJECT_ID=your-actual-project-id
   ```

3. Ensure project exists:

   ```bash
   gcloud projects list
   ```

---

### Python Environment

#### "ModuleNotFoundError: No module named 'google'"

**Symptoms:** `ModuleNotFoundError`

**Solutions:**

1. Ensure virtual environment is activated:

   ```bash
   source venv/Scripts/activate  # Windows Git Bash
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Verify installation:

   ```bash
   python -c "import google; print(google.__version__)"
   ```

#### "No module named 'dotenv'"

**Solution:**

```bash
pip install python-dotenv
```

#### "Python: command not found"

**Solutions:**

1. Python not installed - download from [python.org](https://python.org)
2. Try `python3` instead of `python`
3. Add Python to PATH (Windows):
   - Control Panel → System → Environment Variables
   - Add Python installation path to PATH

---

### API Issues

#### Rate Limiting (429 Error)

**Symptoms:** Too many requests

**Solutions:**

1. Implement exponential backoff:

   ```python
   import time
   from google.api_core import exceptions

   def call_with_retry(func, max_retries=3):
       for attempt in range(max_retries):
           try:
               return func()
           except exceptions.TooManyRequests:
               wait_time = 2 ** attempt
               print(f"Rate limited. Waiting {wait_time}s...")
               time.sleep(wait_time)
   ```

2. Reduce request frequency
3. Check free tier limits

#### Timeout Error

**Symptoms:** Request takes too long

**Solutions:**

1. Increase timeout:

   ```python
   response = model.generate_content(
       prompt,
       generation_config={"timeout": 60}
   )
   ```

2. Use streaming for long responses:

   ```python
   response = model.generate_content(prompt, stream=True)
   for chunk in response:
       print(chunk.text, end="", flush=True)
   ```

3. Check internet connection

#### "Invalid API Key" Error

**Symptoms:** Authentication fails

**Solutions:**

1. Verify credentials file exists:

   ```bash
   ls -la $GOOGLE_APPLICATION_CREDENTIALS
   ```

2. Regenerate credentials:
   - GCP Console → APIs & Services → Credentials
   - Delete old key
   - Create new JSON key

3. Check file permissions:

   ```bash
   chmod 600 /path/to/key.json
   ```

---

### Chatbot Issues

#### Bot Not Responding

**Symptoms:** No response or empty response

**Debugging:**

```python
# Add logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check response
response = model.generate_content("Hello")
print(f"Response text: {response.text}")
print(f"Finish reason: {response.finish_reason}")
print(f"Token count: {response.usage_metadata}")
```

#### Conversation Memory Not Working

**Symptoms:** Bot doesn't remember previous messages

**Solution:**
Ensure you're maintaining conversation history:

```python
class SimpleBot:
    def __init__(self):
        self.conversation_history = []  # Initialize!
    
    def chat(self, user_message):
        # Add to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Include history in prompt
        messages = [msg["content"] for msg in self.conversation_history]
        response = model.generate_content(messages)
        
        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response.text
        })
        
        return response.text
```

#### Bot Giving Wrong Answers

**Symptoms:** Responses are inaccurate or off-topic

**Solutions:**

1. Improve system prompt:

   ```python
   system_prompt = """You are a helpful assistant.
   - Be accurate and factual
   - Admit when you don't know
   - Ask clarifying questions
   """
   ```

2. Add context:

   ```python
   system_prompt = f"""You are a WCC assistant.
   Here's our knowledge base:
   {knowledge_base}
   """
   ```

3. Use lower temperature for consistency:

   ```python
   response = model.generate_content(
       prompt,
       generation_config={"temperature": 0.2}
   )
   ```

---

### Deployment Issues

#### Streamlit App Won't Start

**Symptoms:** Error when running `streamlit run app.py`

**Solutions:**

1. Install Streamlit:

   ```bash
   pip install streamlit
   ```

2. Check for syntax errors:

   ```bash
   python -m py_compile app.py
   ```

3. Run with verbose output:

   ```bash
   streamlit run app.py --logger.level=debug
   ```

#### Environment Variables Not Loading

**Symptoms:** `.env` variables not accessible

**Solutions:**

1. Ensure `.env` file exists in project root
2. Load before using:

   ```python
   from dotenv import load_dotenv
   load_dotenv()  # Call this first!
   ```

3. Verify file format:

   ```bash
   KEY=value
   ANOTHER_KEY=another_value
   ```

4. Add to `.gitignore`:

   ```bash
   .env
   .env.local
   ```

---

### Git & GitHub Issues

#### "Permission denied (publickey)"

**Solution:**
Set up SSH keys:

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
cat ~/.ssh/id_ed25519.pub  # Copy this
# Add to GitHub Settings → SSH Keys
```

#### "Rejected: cannot push to repository"

**Solutions:**

1. Ensure you have push access
2. Check remote URL:

   ```bash
   git remote -v
   ```

3. Update if needed:

   ```bash
   git remote set-url origin https://github.com/username/repo.git
   ```

---

## Debug Checklist

Before asking for help, verify:

- ✅ Virtual environment is activated
- ✅ Dependencies installed: `pip list`
- ✅ Environment variables set: `echo $GOOGLE_APPLICATION_CREDENTIALS`
- ✅ GCP project ID correct
- ✅ Vertex AI API enabled
- ✅ Service account has correct roles
- ✅ No typos in code
- ✅ Latest package versions: `pip install --upgrade -r requirements.txt`

## Getting Help

1. **Check documentation:**
   - [Vertex AI Docs](https://cloud.google.com/vertex-ai/docs)
   - [Google Cloud Python Client](https://cloud.google.com/python/docs/reference)

2. **Search for similar issues:**
   - Stack Overflow
   - GitHub Issues
   - Google Cloud Community

3. **Ask in [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7):**
   - Describe the problem clearly
   - Share error message
   - Include relevant code snippet
   - Mention what you've already tried

4. **Create a minimal reproduction:**

   ```python
   # Minimal example that shows the problem
   from google.cloud import aiplatform
   aiplatform.init(project="YOUR_PROJECT_ID")
   # ... minimal code to reproduce issue
   ```

---

**Still stuck?** Reach out to the instructors or the WCC community!
