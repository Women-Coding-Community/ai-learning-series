"""
Configuration and API Setup for Career Coach Bot
"""
import os
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv

MODEL_ID = 'gemini-2.5-flash-lite'

def initialize_api():
    """Initialize Gemini API with key"""
    try:
        load_dotenv()
    except Exception:
        pass

    # Set up Gemini API from environment
    _api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if _api_key:
        genai.configure(api_key=_api_key)
        print("✓ Gemini API initialized successfully")
    else:
        print("⚠️ Warning: No API key found. Please set GOOGLE_API_KEY or GEMINI_API_KEY in your .env file")

# Model Configuration
MODEL_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 2048,  # Increased for longer career guidance responses
}

# Safety Settings
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

