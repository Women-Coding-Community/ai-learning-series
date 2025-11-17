# 🎯 Career Quick Coach - Use Case Guide

## Overview
Build an AI-powered career counselor that helps students explore career paths, understand job market trends, and prepare for interviews. This use case focuses on **few-shot prompting** and **role-based prompting** to maintain a consistent, encouraging coaching voice.

---

## Learning Objectives
- ✅ Master few-shot prompting for consistent brand voice
- ✅ Implement role-based prompting with personality
- ✅ Handle sensitive career/personal information securely
- ✅ Provide actionable, step-by-step career guidance

---

## Use Case Scenario

**Target Users:** College students exploring careers, preparing for interviews, or making major decisions

**Key Features:**
1. Career path exploration based on interests/skills
2. Resume and interview tips
3. Job market insights
4. Next-step action plans
5. Motivational support for career anxiety

---

## 📚 Prompt Engineering Approach

### 1. Role-Based Prompt (Base Persona)

```python
COACH_ROLE = """You are Jordan Hayes, a career counselor with 15 years of experience.

YOUR BACKGROUND:
<COACH_EXPERIENCE>

YOUR PERSONALITY: 
<Examples>
- Encouraging and motivational (but not cheesy)
- Direct and honest about job market realities

YOUR COACHING STYLE:
<MENTION_CHOACHING_STYLES>
"""
```

### 2. Few-Shot Examples (Teach Response Style)

```python
FEW_SHOT_EXAMPLES = """
Example 1: Career Exploration
Student: "I like technology but I'm not sure if I should be a developer or go into cybersecurity."
Jordan: "Great question! Let's think through this together. Both paths are strong, but they're quite different day-to-day.

<BE CREATIVE HERE>
"""
```

### 3. Complete Production Prompt

```python
def create_career_coach_prompt(user_query: str) -> str:
    return f"""{COACH_ROLE}

{FEW_SHOT_EXAMPLES}

RESPONSE GUIDELINES:
✓ Ask 1-2 follow-up questions to understand context
✓ Provide specific, actionable advice (not generic platitudes)
✓ Include 2-3 concrete next steps

TOPICS YOU HELP WITH:
• Career exploration and decision-making
• Resume and cover letter optimization
• Interview preparation and practice

BOUNDARIES (DO NOT):
✗ Make promises about job placement or salary
✗ Review actual resumes with PII

Student: {user_query}

Jordan:"""
```

---

## 🛡️ Security Considerations

### 1. PII Handling

**Risk:** Students might share resumes with NI Number, addresses, or references

**Solution:**
```python
# Add to security.py
RESUME_PII_PATTERNS = [
    (r'\bReference:.*', '[REFERENCE_REDACTED]', 'Reference'),
    (r'\b\d{1,5}\s+\w+\s+(Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)', 
     '[ADDRESS_REDACTED]', 'Address'),
]

# In chatbot.py
def handle_resume_request(self, message: str):
    if 'resume' in message.lower() and any(pii in message for pii in ['SSN', '@', 'phone']):
        return {
            'response': "I'd love to help with resume tips, but please don't paste your actual resume here with personal information. Instead, describe your experience and I'll give you specific advice on how to improve it!",
            'blocked': True
        }
```

### 2. Sensitive Topics

**Risk:** Career anxiety can trigger mental health crises

```python
CAREER_CRISIS_KEYWORDS = [
    'giving up on life',
    'not worth living',
    'failed at everything',
    'want to disappear'
]

# Enhanced crisis detection
if any(keyword in message.lower() for keyword in CAREER_CRISIS_KEYWORDS):
    return """I'm really concerned about what you're sharing. Career setbacks can feel overwhelming, but this sounds like more than job stress."""
```

---

## 🎯 Practice Exercises

### Exercise 1: Enhance the Prompt
**Task:** Add more few-shot examples for:
- Career change scenarios
- Salary negotiation
- Professional networking

**Hint:** Follow the pattern: situation → advice → action steps

---

### Exercise 2: Add Custom Security
**Task:** Implement detection for students trying to get the bot to write their entire resume

```python
def detect_resume_writing_attempt(self, message: str) -> bool:
    """Detect if student wants bot to write entire resume"""
    writing_requests = [
        'write my resume',
        'create my resume',
        'make a resume for me',
        'generate my cv'
    ]
    return any(req in message.lower() for req in writing_requests)
```

---

### Exercise 3: Structured Output
**Task:** Add a "Career Action Plan" mode that returns JSON:

```json
{
    "career_goal": "Data Scientist",
    "immediate_actions": [
        "Complete Python basics course",
        "Build 2 portfolio projects",
        "Network with 5 data scientists"
    ],
    "3_month_milestones": [...],
    "6_month_milestones": [...],
    "skills_to_develop": [...],
    "confidence_level": 0.75
}
```

---

## 🎓 Key Takeaways

1. **Few-shot prompting** ensures consistent, on-brand career coaching voice
2. **Role-based prompting** creates an engaging, relatable persona
3. **Security is crucial** when handling career-related PII and sensitive topics
4. **Actionable advice > Generic motivation** - always provide next steps
5. **Balance optimism with realism** - prepare students for real job market