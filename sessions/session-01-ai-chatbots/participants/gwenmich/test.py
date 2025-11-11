from career_coach_bot import CareerCoachWithMemory

def test_career_coach():
    """Test the career coach with sample questions"""
    coach = CareerCoachWithMemory()

    test_questions = [
        "Hi! I'm looking to transition into tech. I have 5 years in marketing. Where should I start?",
        "Can you help me with my resume? I'm applying for junior developer roles.",
        "I have an interview next week. What should I prepare?",
        "I'm feeling imposter syndrome. How do I build confidence?",
        "What skills should I focus on for a data science role?"
    ]

    for question in test_questions:
        print(f"\n👤 User: {question}")
        response = coach.chat(question)
        print(f"🎯 Coachly: {response}\n")
        print("-" * 80)

if __name__ == "__main__":
    test_career_coach()