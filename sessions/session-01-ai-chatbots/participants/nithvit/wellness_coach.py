import os
import google.generativeai as genai
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
from wellness_data import WELLNESS_DATA


load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if(api_key is None):
    raise ValueError("GEMINI_API_KEY not found in environment variables")
genai.configure(api_key=api_key)
MODEL_ID = 'gemini-2.5-flash-lite'


WELLNESS_COACH_PROMPT = f"""You are Wellness Coach, a supportive AI assistant helping tech professionals maintain their mental and physical health.

ABOUT WELLNESS IN TECH:
{WELLNESS_DATA}

Your personality:
- Empathetic and non-judgmental
- Encouraging but realistic about tech industry challenges
- Focus on small, achievable steps
- Warm and understanding of burnout, deadlines, and screen time

Help with:
- Daily wellness check-ins and motivation
- Stress management for coding sessions
- Work-life balance strategies
- Healthy habits for programmers (sleep, exercise, breaks)
- Self-care routines and mindfulness
- Connecting wellness to career success

Guidelines:
- Ask about their current stress level or habits
- Provide specific, actionable tips from the data
- Suggest resources when relevant
- Encourage progress tracking
- If serious issues arise, suggest professional help
- Always end with encouragement

Remember: Tech work is demanding—celebrate their efforts!"""

class WellnessCoach:
    def __init__(self):
        generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            max_output_tokens=100,
        )
        self.model = genai.GenerativeModel(MODEL_ID, system_instruction=WELLNESS_COACH_PROMPT, generation_config=generation_config)
        self.conversation_history = []
    
    def chat(self, user_input):
        self.conversation_history.append({"role": "user", "parts": [user_input]})

        response = self.model.generate_content(self.conversation_history)
        
        bot_response = response.text
        
        self.conversation_history.append({"role": "model", "parts": [response.text]})
        
        return bot_response


def main():
    coach = WellnessCoach()
    st.title("Tech Wellness Coach")
    st.write("Ask me anything about wellness in tech!")
    user_input = st.text_input("You:")
    if user_input:
        bot_response = coach.chat(user_input)
        st.write("Coach:", bot_response)
        st.write("\n")  

if __name__ == "__main__":
    main()

