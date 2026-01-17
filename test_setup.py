import sys
print(f"Python version: {sys.version}")

try:
    from google.cloud import aiplatform
    print("Good: google-cloud-aiplatform installed")
except ImportError:
    print("Bad: google-cloud-aiplatform not found")

try:
    import streamlit
    print("Good: streamlit installed")
except ImportError:
    print("Bad: streamlit not found")

try:
    import dotenv
    print("Good: python-dotenv installed")
except ImportError:
    print("Bad: python-dotenv not found")

print("\nGood: All packages installed successfully!")