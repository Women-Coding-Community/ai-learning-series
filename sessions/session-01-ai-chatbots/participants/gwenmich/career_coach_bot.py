import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in environment variables. "
        "Please set it in your .env file or environment."
    )

genai.configure(api_key=API_KEY)


CAREER_COACH_PROMPT = """You are an experienced career coach at Women Coding Community. 
Your role is to provide personalized career guidance, resume tips, interview preparation, 
and encouragement to members.

Guidelines:
- Be supportive and encouraging
- Provide specific, actionable advice
- Ask clarifying questions about their goals and background
- Remember context from previous messages
- Suggest resources and next steps
- Be honest about challenges but focus on solutions
- Celebrate wins and progress

When giving advice:
1. Understand their current situation
2. Ask about their goals
3. Provide specific tips and examples
4. Suggest resources and next steps
5. Offer encouragement

Topics you can help with:
- Resume optimization and tailoring
- Interview preparation and mock questions
- Career path planning
- Skill development and learning resources
- Confidence building
- Salary negotiation basics
- Work-life balance and career growth
- Dealing with imposter syndrome"""


class CareerCoach:

    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash-lite")
        self.system_prompt = CAREER_COACH_PROMPT
        self.conversation_history = []
        self.user_profile = {
            "goals": None,
            "experience_level": None,
            "target_role": None
        }

    def chat(self, user_message: str) -> str:
        try:
            self.conversation_history.append(
                {"role": "user", "content": user_message}
            )

            messages = [
                {"role": "user", "content": self.system_prompt},
            ]

            for msg in self.conversation_history:
                messages.append(msg)

            response = self.model.generate_content(
                [msg["content"] for msg in messages]
            )

            bot_response = response.text

            self.conversation_history.append(
                {"role": "assistant", "content": bot_response}
            )

            return bot_response

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            return error_msg

    def get_profile(self):
        return self.user_profile

    def clear_history(self):
        self.conversation_history = []



class CareerCoachWithMemory(CareerCoach):

    def __init__(self, user_id: str = "default"):
        super().__init__()
        self.user_id = user_id
        self.memory_file = f"career_coach_{user_id}.json"
        self.load_memory()

    def save_memory(self):
        data = {
            "user_id": self.user_id,
            "timestamp": datetime.now().isoformat(),
            "profile": self.user_profile,
            "history": self.conversation_history
        }
        with open(self.memory_file, "w") as f:
            json.dump(data, f, indent=2)

    def load_memory(self):
        try:
            with open(self.memory_file, "r") as f:
                data = json.load(f)
                self.user_profile = data.get("profile", {})
                self.conversation_history = data.get("history", [])
                print(f"Welcome back! Loaded {len(self.conversation_history)} previous messages.")
        except FileNotFoundError:
            print("Starting fresh conversation!")

    def chat(self, user_message: str) -> str:
        response = super().chat(user_message)
        self.save_memory()
        return response



def main():
    print("🎯 Welcome to Coachly!")
    print("Your AI career mentor from Women Coding Community")
    print("Type 'quit' to exit, 'clear' to clear history\n")

    user_id = input("Enter your name: ").strip() or "default"
    coach = CareerCoachWithMemory(user_id=user_id)

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            print("Coachly: Great talking with you! Keep growing! 🚀")
            break

        if user_input.lower() == "clear":
            coach.clear_history()
            print("Coachly: Conversation cleared. Let's start fresh!\n")
            continue

        if not user_input:
            continue

        response = coach.chat(user_input)
        print(f"\nCoachly: {response}\n")


if __name__ == "__main__":
    main()