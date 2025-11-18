# Career Quick Coach - Use Case Guide

## Overview

Build an AI-powered career coaching chatbot that provides quick career advice, resume tips, interview preparation, and career guidance between mentorship sessions.

---

## Problem Statement

**Challenge:** WCC members need quick career advice and guidance between formal mentorship sessions:

- Resume review and optimization tips
- Interview preparation and mock questions
- Career path guidance and skill development
- Confidence building for career transitions
- Quick answers to career questions

**Why it matters:** Career development is crucial for tech professionals, but personalized mentorship isn't always available when needed.

---

## What You'll Build

A conversational AI career coach that:

- Provides personalized career advice
- Maintains conversation context across sessions
- Offers resume and interview tips
- Suggests skill development paths
- Remembers user's career goals and background
- Provides encouragement and motivation

---

## Architecture

```text
┌─────────────────┐
│   User Input    │
│  (Career Q&A)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Gemini API with Career Persona    │
│  (System Prompt: Career Coach)      │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Conversation Memory                │
│  (User goals, background, history)  │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Formatted Response                │
│   (Advice, tips, resources)         │
└─────────────────────────────────────┘
```

---

## Step 1: Create Career Coach Data

Create a file `career_data.py` with career coaching knowledge:

```python
CAREER_COACHING_DATA = {
    "resume_tips": [
        "Use action verbs (developed, implemented, designed)",
        "Quantify achievements (increased by 25%, reduced time by 40%)",
        "Tailor to job description keywords",
        "Keep to 1 page for entry-level, 2 for mid-career",
        "Use consistent formatting and clear hierarchy"
    ],
    "interview_prep": [
        "STAR method: Situation, Task, Action, Result",
        "Practice common questions: Tell me about yourself, Why this role?",
        "Prepare questions to ask interviewer",
        "Research company culture and recent news",
        "Do a mock interview with a friend"
    ],
    "career_paths": {
        "frontend": ["HTML/CSS", "JavaScript", "React/Vue", "UI/UX basics"],
        "backend": ["Python/Node.js", "Databases", "APIs", "System Design"],
        "data": ["Python", "SQL", "Statistics", "Machine Learning"],
        "devops": ["Linux", "Docker", "Kubernetes", "CI/CD"]
    },
    "skill_resources": {
        "leetcode": "Practice coding problems",
        "system_design_primer": "Learn system design",
        "coursera": "Structured learning paths",
        "github": "Build portfolio projects"
    }
}
```

---

## Step 2: Enhance the Starter Template

Modify `chatbot.py` with a career coaching system prompt:

```python
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-project-id")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")

aiplatform.init(project=PROJECT_ID, location=LOCATION)

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
    """AI-powered career coaching chatbot"""

    def __init__(self):
        self.model = GenerativeModel("gemini-2.5-flash-lite")
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

            bot_response = response.text

            # Add to history
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
```

---

## Step 3: Add Conversation Memory (Optional Enhancement)

Save and load conversation history:

```python
import json
from datetime import datetime

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
```

---

## Step 4: Create Web Interface (Optional)

Use Streamlit for a web-based career coach:

```python
import streamlit as st
from career_coach import CareerCoachWithMemory

st.set_page_config(page_title="Career Quick Coach", layout="wide")

st.title("🎯 Career Quick Coach")
st.markdown("Your AI career mentor from Women Coding Community")

# Initialize coach
if "coach" not in st.session_state:
    st.session_state.coach = CareerCoachWithMemory(user_id="streamlit_user")

# Sidebar for profile
with st.sidebar:
    st.header("Your Profile")
    experience = st.selectbox(
        "Experience Level",
        ["Entry-level", "Mid-career", "Senior", "Career changer"]
    )
    target_role = st.text_input("Target Role (optional)")
    goal = st.text_area("Career Goal (optional)")

    if st.button("Update Profile"):
        st.session_state.coach.user_profile = {
            "experience_level": experience,
            "target_role": target_role,
            "goals": goal
        }
        st.success("Profile updated!")

# Main chat interface
st.subheader("Chat with Your Career Coach")

# Display conversation history
for msg in st.session_state.coach.conversation_history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Input
user_input = st.chat_input("Ask your career coach a question...")

if user_input:
    st.chat_message("user").write(user_input)
    response = st.session_state.coach.chat(user_input)
    st.chat_message("assistant").write(response)
    st.rerun()

# Resources sidebar
st.sidebar.markdown("---")
st.sidebar.header("📚 Resources")
st.sidebar.markdown("""
- [LinkedIn Learning](https://linkedin.com/learning)
- [Coursera](https://coursera.org)
- [LeetCode](https://leetcode.com)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
""")
```

---

## Step 5: Testing

Test different career scenarios:

```python
def test_career_coach():
    """Test the career coach with sample questions"""
    coach = CareerCoach()

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
        print(f"🎯 Coach: {response}\n")
        print("-" * 80)

if __name__ == "__main__":
    test_career_coach()
```

---

## Deployment Options

### Option 1: Local CLI

```bash
python career_coach.py
```

### Option 2: Streamlit Web App

```bash
streamlit run career_coach_web.py
```

### Option 3: Discord Bot

Integrate with WCC Discord for instant career advice

### Option 4: GitHub Pages

Deploy as a web app using GitHub Pages + Flask

---

## Enhancement Ideas

- **Mock Interview Mode:** Practice common interview questions
- **Resume Analyzer:** Analyze uploaded resumes and provide feedback
- **Skill Assessment:** Quiz on technical skills and suggest learning paths
- **Resource Recommendations:** Personalized learning resources based on goals
- **Progress Tracking:** Track career goals and celebrate milestones
- **Peer Matching:** Connect with mentors based on career goals
- **Job Search Helper:** Analyze job descriptions and suggest preparation
- **Salary Negotiation Guide:** Tips for negotiating offers

---

## Common Questions

**Q: Can the coach help with non-tech careers?**  
A: Yes! Modify the system prompt to include other career paths.

**Q: How do I make it remember my goals?**  
A: Use the `CareerCoachWithMemory` class to persist conversations.

**Q: Can I add more career resources?**  
A: Absolutely! Expand `career_data.py` with more tips and resources.

**Q: How do I deploy this?**  
A: Use Streamlit Cloud, Heroku, or Google Cloud Run for easy deployment.

---

## Submission Checklist

- ✅ Career coach responds to career questions
- ✅ Maintains conversation context
- ✅ Uses system prompts for coaching personality
- ✅ Handles errors gracefully
- ✅ README with setup and usage instructions
- ✅ Test cases or example conversations
- ✅ Optional: Web interface or persistence

---

## Resources

- [Gemini API Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini-api)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Career Development Resources](https://www.indeed.com/career-advice)
- [Interview Preparation Guide](https://www.techinterviewhandbook.org)

---

## Questions?

Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel or reach out to the instructors!

---

**Happy coaching! Help your peers grow their careers! 🚀**
