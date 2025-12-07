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