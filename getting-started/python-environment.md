# Python Environment Setup

## Prerequisites

- Python 3.11 or higher installed
- pip (Python package manager)
- Git installed

## Check Your Python Version

```bash
python --version
```

Should output: `Python 3.11.x` or higher

If you need to install Python, download from [python.org](https://www.python.org/downloads/)

## Create a Virtual Environment

It's best practice to use a virtual environment for each project.

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Windows (Git Bash)

```bash
python -m venv venv
source venv/Scripts/activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

## Install Required Packages

Create a `requirements.txt` file in your project directory if you haven't already:

```bash
google-cloud-aiplatform>=1.26.0
vertexai>=0.1.0
python-dotenv>=1.0.0
streamlit>=1.28.0
requests>=2.31.0
```

Install all packages:

```bash
pip install -r requirements.txt
```

## Verify Installation

Create a test script `test_setup.py`:

```python
import sys
print(f"Python version: {sys.version}")

try:
    from google.cloud import aiplatform
    print("✅ google-cloud-aiplatform installed")
except ImportError:
    print("❌ google-cloud-aiplatform not found")

try:
    import streamlit
    print("✅ streamlit installed")
except ImportError:
    print("❌ streamlit not found")

try:
    import dotenv
    print("✅ python-dotenv installed")
except ImportError:
    print("❌ python-dotenv not found")

print("\n✅ All packages installed successfully!")
```

Run it:

```bash
python test_setup.py
```

## Environment Variables

Create a `.env` file in your project root if you haven't already:

```bash
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/key.json
```

Load it in your Python code:

```python
from dotenv import load_dotenv
import os

load_dotenv()

project_id = os.getenv("GCP_PROJECT_ID")
location = os.getenv("GCP_LOCATION")
```

## Deactivate Virtual Environment

When you're done working:

```bash
deactivate
```

## Troubleshooting

### "python: command not found"

- Python is not installed or not in PATH
- Try `python3` instead of `python`

### "Permission denied" when activating venv

- On Windows, you may need to run PowerShell as Administrator
- Or use Git Bash instead

### "Module not found" errors

- Ensure virtual environment is activated (you should see `(venv)` in prompt)
- Run `pip install -r requirements.txt` again

## IDE Setup

### VS Code

1. Install Python extension
2. Select interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
3. Choose the one in your `venv` folder

### PyCharm

1. Go to Settings → Project → Python Interpreter
2. Click gear icon → Add
3. Select "Existing Environment"
4. Navigate to `venv/Scripts/python.exe` (Windows) or `venv/bin/python` (macOS/Linux)

## Next Steps

- [GCP Setup Guide](./gcp-setup.md)
- [Vertex AI Quickstart](./vertex-ai-quickstart.md)
- Start coding!

---

**Documentation:**

- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [pip Documentation](https://pip.pypa.io/en/latest/)
