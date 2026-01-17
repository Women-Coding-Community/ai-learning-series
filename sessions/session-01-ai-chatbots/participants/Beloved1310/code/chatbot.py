# chatbot.py

import os
import json
import logging
from datetime import datetime
import google.generativeai as genai
from scraper import scrape_wcc_events   # LIVE SCRAPER IMPORT
from dotenv import load_dotenv

# ---------------------------------------------------------
# Setup Logging
# ---------------------------------------------------------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("chatbot.py loaded successfully.")

# ---------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------
try:
    load_dotenv()
    logging.info(".env loaded successfully.")
except Exception as e:
    logging.warning(f"Could not load .env file: {e}")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    logging.error("❌ GEMINI_API_KEY is missing.")
    api_key = "your-gemini-api-key-here"

# ---------------------------------------------------------
# Configure Gemini API
# ---------------------------------------------------------
MODEL_ID = "gemini-2.5-flash-lite"

try:
    genai.configure(api_key=api_key)
    logging.info("Gemini API configured successfully.")
except Exception as e:
    logging.error(f"Error configuring Gemini API: {e}")

# ---------------------------------------------------------
# Load FAQs
# ---------------------------------------------------------
try:
    with open("wcc_faqs.json") as f:
        wcc_data = json.load(f)
        faqs = wcc_data.get("faqs", [])
    logging.info("FAQs loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load wcc_faqs.json: {e}")
    faqs = []

faq_text = "\n".join([
    f"Q: {faq['question']}\nA: {faq['answer']}"
    for faq in faqs
])

# ---------------------------------------------------------
# SCRAPE LIVE EVENTS
# ---------------------------------------------------------
try:
    events = scrape_wcc_events()
    logging.info(f"Scraped {len(events)} events from website.")
except Exception as e:
    logging.error(f"Event scraping failed: {e}")
    events = []

events_text = "\n".join([
    f"- {e['title']} on {e['date']}: {e['description']}"
    for e in events
]) or "No upcoming events available right now."

# ---------------------------------------------------------
# FINAL SYSTEM PROMPT (FAQs + Live Events)
# ---------------------------------------------------------
system_prompt = f"""
You are Maya, the enthusiastic WCC assistant!
You love helping women in tech and are passionate about community.
Always be encouraging and supportive.
------------------------------------
📌 OFFICIAL WCC FAQs
------------------------------------
{faq_text}

------------------------------------
📅 LIVE UPCOMING WCC EVENTS
------------------------------------
{events_text}

Use emojis occasionally to add warmth, inclusive, and helpful.
If you don’t know something, advise the user to contact the WCC team.
"""

# ---------------------------------------------------------
# Gemini Bot Class
# ---------------------------------------------------------
class SimpleBot:
    def __init__(self, system_prompt, faqs):
        self.system_prompt = system_prompt
        self.faqs = faqs
        self.memory = []
        logging.info("SimpleBot initialized successfully.")

    # -------------------------
    # Step 1: Basic API Call
    # -------------------------
    def step_1_basic_api_call(self, user_msg):
        try:
            model = genai.GenerativeModel(MODEL_ID)
            response = model.generate_content(user_msg)
            return response.text
        except Exception as e:
            logging.error(f"Gemini Step 1 Error: {e}")
            return "⚠️ I’m having trouble generating a response right now."

    # -------------------------
    # Step 2: With system prompt
    # -------------------------
    def step_2_add_personality(self, user_msg):
        try:
            model = genai.GenerativeModel(
                MODEL_ID,
                system_instruction=self.system_prompt
            )
            response = model.generate_content(user_msg)
            return response.text
        except Exception as e:
            logging.error(f"Gemini Step 2 Error: {e}")
            return "⚠️ I couldn't process that, please try again."

    # -------------------------
    # Step 3: Memory conversation
    # -------------------------
    def step_3_conversation_memory(self, user_msg):
        try:
            self.memory.append({"role": "user", "content": user_msg})
            history = "\n".join(f"{m['role']}: {m['content']}" for m in self.memory)

            prompt = f"""
Conversation so far:
{history}

User: {user_msg}
Assistant:
"""

            model = genai.GenerativeModel(MODEL_ID)
            response = model.generate_content(prompt)
            reply = response.text

            self.memory.append({"role": "assistant", "content": reply})
            return reply

        except Exception as e:
            logging.error(f"Gemini Step 3 Error: {e}")
            return "⚠️ I'm having trouble remembering the conversation right now."

    # -------------------------
    # Step 4: Model parameters tuning
    # -------------------------
    def step_4_model_parameters(self, user_msg):
        try:
            model = genai.GenerativeModel(MODEL_ID)
            response = model.generate_content(
                user_msg,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_output_tokens": 300
                }
            )
            return response.text
        except Exception as e:
            logging.error(f"Gemini Step 4 Error: {e}")
            return "⚠️ Unable to generate a detailed response right now."

    # -----------------------------------------------------
    # Main Chat Function
    # -----------------------------------------------------
    def chat(self, message):
        logging.info(f"User asked: {message}")

        try:
            msg_lower = message.lower()

            # FAQ match
            for faq in self.faqs:
                if faq["question"].lower() in msg_lower:
                    logging.info("FAQ match found.")
                    return faq["answer"]

            logging.info("No FAQ match. Using Gemini.")
            return self.step_2_add_personality(message)

        except Exception as e:
            logging.error(f"Chat method error: {e}")
            return "⚠️ Something went wrong while processing your message."
# ---------------------------------------------------------
# User Feedback Storage
# ---------------------------------------------------------
def get_feedback(rating: int, feedback_text: str):
    """Collect and save user feedback."""
    try:
        data = {
            "rating": rating,
            "feedback": feedback_text,
            "timestamp": datetime.now().isoformat()
        }

        with open("feedback.json", "a") as f:
            json.dump(data, f)
            f.write("\n")

        logging.info(f"Feedback saved: rating={rating}")
        return True

    except Exception as e:
        logging.error(f"Failed to save feedback: {e}")
        return False
