import json
from datetime import datetime
from career_coach import CareerCoach

class CareerCoachWithMemory(CareerCoach):
    """Career coach with persistent conversation memory"""

    def __init__(self, user_id: str = "default"):
        super().__init__()
        self.user_id = user_id
        self.memory_file = f"career_coach_{user_id}.json"
        self.load_memory()

    def save_memory(self):
        """Save conversation to file"""
        data = {
            "user_id": self.user_id,
            "timestamp": datetime.now().isoformat(),
            "profile": self.user_profile,
            "history": self.conversation_history
        }
        with open(self.memory_file, "w") as f:
            json.dump(data, f, indent=2)

    def load_memory(self):
        """Load previous conversations"""
        try:
            with open(self.memory_file, "r") as f:
                data = json.load(f)
                self.user_profile = data.get("profile", {})
                self.conversation_history = data.get("history", [])
                print(f"Welcome back! Loaded {len(self.conversation_history)} previous messages.")
        except FileNotFoundError:
            print("Starting fresh conversation!")

    def chat(self, user_message: str) -> str:
        """Chat and auto-save"""
        response = super().chat(user_message)
        self.save_memory()
        return response
