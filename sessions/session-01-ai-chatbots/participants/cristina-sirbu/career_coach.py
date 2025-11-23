import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in environment variables. "
        "Please set it in your .env file or environment."
    )

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


genai.configure(api_key=API_KEY)


class CareerCoach:
    """AI-powered career coaching chatbot"""

    def __init__(self):
        """
        Initialize the chatbot.
        """
        self.model = genai.GenerativeModel("gemini-2.5-flash-lite")
        self.system_prompt = CAREER_COACH_PROMPT
        self.conversation_history = []
        self.user_profile = {
            "goals": None,
            "experience_level": None,
            "target_role": None
        }

    def chat(self, user_message: str) -> str:
        """Send a message and get career coaching advice"""
        try:
            # Add user message to history
            self.conversation_history.append(
                {"role": "user", "content": user_message}
            )

            # Build messages with system prompt
            messages = [
                {"role": "user", "content": self.system_prompt},
            ]

            # Add conversation history
            for msg in self.conversation_history:
                messages.append(msg)

            # Generate response
            response = self.model.generate_content(
                [msg["content"] for msg in messages]
            )

            # Extract response text
            bot_response = response.text

            # Add bot response to history
            self.conversation_history.append(
                {"role": "assistant", "content": bot_response}
            )

            return bot_response

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            return error_msg

    def get_profile(self):
        """Get user's career profile"""
        return self.user_profile

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


def main():
    """Run the career coach chatbot"""
    print("🎯 Welcome to Career Quick Coach!")
    print("Your AI career mentor from Women Coding Community")
    print("Type 'quit' to exit, 'clear' to clear history\n")

    coach = CareerCoach()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            print("Coach: Great talking with you! Keep growing! 🚀")
            break

        if user_input.lower() == "clear":
            coach.clear_history()
            print("Coach: Conversation cleared. Let's start fresh!\n")
            continue

        if not user_input:
            continue

        response = coach.chat(user_input)
        print(f"\nCoach: {response}\n")

if __name__ == "__main__":
    main()
