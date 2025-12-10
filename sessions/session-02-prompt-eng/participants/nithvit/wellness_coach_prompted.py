import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from wellness_data import WELLNESS_DATA


load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if(api_key is None):
    raise ValueError("GEMINI_API_KEY not found in environment variables")
genai.configure(api_key=api_key)
MODEL_ID = 'gemini-2.5-flash-lite'

PROMPT_PERSONA = """You are Wellness Coach, a supportive AI assistant helping tech professionals maintain 
their mental and physical health.
Tone: warm, encouraging, gently directive.
Core lenses:
- Understand the user's current context before advising.
- Offer micro-habits tied to their developer lifestyle.
- Encourage reflection, celebrate effort, and suggest professional help when issues are severe.
"""

PROMPT_COT_TEMPLATE = """Follow this plan:
1. Briefly restate the user's concern.
2. Think through possible causes or considerations (keep this reasoning internal).
3. Pick 2-3 tailored suggestions from the wellness playbook.
4. End with encouragement + optional follow-up question.

"""

SENSITIVE_TOPICS = ["professional help", "suicide", "self-harm", "emergency", "urgent care"]
def apply_guardrails(prompt: str) -> tuple[bool, str | None]:
    lowered = prompt.lower()
    for phrase in SENSITIVE_TOPICS:
        if phrase in lowered:
            return False, (
                "I’m here for general wellness support only. "
                "For immediate or clinical assistance, please reach out to a licensed professional or emergency services."
            )
    return True, None

def build_prompt(user_input: str, conversation_state: list[str]) -> list[str]:
    return [
        PROMPT_PERSONA,
        PROMPT_COT_TEMPLATE,
        f"Conversation so far: {conversation_state[-4:]}",
        f"User: {user_input}"
    ]

FORBIDDEN_PHRASES = ["prescribe", "diagnose", "take medication"]

def scrub_output(text: str) -> str:
    if any(phrase in text.lower() for phrase in FORBIDDEN_PHRASES):
        return ("I’m here for general wellness support only. "
                "Please consult a licensed professional for specific medical guidance.")
    return text    

class WellnessCoachPrompted:
    def __init__(self):
        generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            max_output_tokens=1000,
        )
        self.model = genai.GenerativeModel(MODEL_ID,
         generation_config=generation_config)

        self.conversation_history = []

    def chat(self, user_input):
        self.conversation_history.append({"role": "user", "parts": [user_input]})
        
        ok, guardrail_msg = apply_guardrails(user_input)
        if not ok:
            self.conversation_history.append({"role": "model", "parts": [guardrail_msg]})
            return guardrail_msg

        prompt = build_prompt(user_input, self.conversation_history)
        bot_response = self.model.generate_content(prompt)
        clean_response = scrub_output(bot_response.text)

        self.conversation_history.append({"role": "model", "parts": [clean_response]})
        return clean_response


        
def main():
    st.set_page_config(page_title="Tech Wellness Coach", page_icon="🌿")

    if "coach" not in st.session_state:
        st.session_state.coach = WellnessCoachPrompted()
        st.session_state.messages = []

    st.title("🌿 Tech Wellness Coach")
    st.caption("Share how you’re feeling and get gentle, actionable support tailored for developers.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I support your wellness today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = st.session_state.coach.chat(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)


if __name__ == "__main__":
    main()
            

    



