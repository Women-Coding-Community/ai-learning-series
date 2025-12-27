# Career Quick Coach - Implementation

This directory contains a complete implementation of the Career Quick Coach use case, demonstrating few-shot prompting, role-based prompting, and comprehensive security guardrails.

## 📁 Files

- **`chatbot.py`** - Main CareerCoachBot class with security pipeline
- **`prompt_patterns.py`** - Role-based and few-shot prompt templates
- **`security.py`** - Multi-layered security guardrails (PII detection, prompt injection, content moderation)
- **`config.py`** - API configuration and model settings
- **`demo.py`** - Demo script to test all features

## 🚀 Quick Start

1. **Set up environment variables:**
   ```bash
   # Create .env file in project root
   GOOGLE_API_KEY=your_api_key_here
   # OR
   GEMINI_API_KEY=your_api_key_here
   ```

2. **Run the demo:**
   ```bash
   cd sessions/session-02-prompt-eng/participants/Beloved1310
   python demo.py
   ```

3. **Use in your code:**
   ```python
   from chatbot import CareerCoachBot
   
   bot = CareerCoachBot()
   response = bot.chat("I'm interested in data science. What should I do?")
   print(response)
   ```

## ✨ Features Implemented

### 1. Role-Based Prompting
- **Jordan Hayes** persona: 15 years of experience, encouraging but realistic
- Consistent coaching voice across all interactions
- Personality traits: calm, honest, supportive

### 2. Few-Shot Examples
Four comprehensive examples covering:
- **Career Exploration** - Choosing between developer vs cybersecurity
- **Career Change** - Transitioning from biology to data analysis
- **Salary Negotiation** - Overcoming fear of negotiation
- **Professional Networking** - Starting from zero connections

### 3. Security Features

#### PII Detection & Redaction
- National Insurance numbers
- Phone numbers
- Email addresses
- Credit card numbers
- Physical addresses
- **Resume-specific patterns:**
  - Reference sections
  - Reference names with titles

#### Resume Protection
- Detects attempts to share resumes with PII
- Blocks requests to write entire resumes
- Redirects to safer advice-giving approach

#### Crisis Detection
- Detects career-related crisis language
- Provides appropriate support resources
- Escalates critical situations

#### Prompt Injection Protection
- Detects common injection patterns
- Blocks attempts to override instructions
- Maintains system integrity

### 4. Structured Output (Action Plans)
- JSON format for structured career action plans
- Includes:
  - Career goal
  - Immediate actions
  - 3-month and 6-month milestones
  - Skills to develop
  - Confidence level

## 🎯 Use Cases

### Standard Coaching
```python
bot = CareerCoachBot()
response = bot.chat("I'm not sure what career path to choose")
```

### Action Plan Mode
```python
result = bot.process_message(
    "I want to become a data scientist",
    mode="action_plan"
)
if "action_plan" in result:
    plan = result["action_plan"]
    print(f"Goal: {plan['career_goal']}")
    print(f"Immediate actions: {plan['immediate_actions']}")
```

### Full Processing (with security details)
```python
result = bot.process_message("Your question here")
print(result["response"])
print(result["processing_steps"])
print(result["security_events"])
```

## 🛡️ Security Pipeline

The bot processes messages through a 7-step security pipeline:

1. **Prompt Injection Detection** - Blocks malicious prompts
2. **Crisis Handling** - Detects and responds to crisis situations
3. **Resume PII Protection** - Blocks resumes with personal info
4. **PII Redaction** - Removes PII from messages before processing
5. **Content Moderation** - Filters inappropriate content
6. **AI Response Generation** - Generates safe, helpful responses
7. **Output Validation** - Ensures response quality and safety

## 📝 Prompt Patterns

The implementation includes multiple prompt patterns:
- `few_shot` - With examples (ensures consistent, on-brand career coaching voice)
- `role_based` - Persona-based responses (creates engaging, relatable persona)
- `structured` - JSON output for action plans
- `advanced` - Production-ready with all guardrails (default)

## 🎓 Learning Objectives Achieved

✅ **Few-shot prompting** - Ensures consistent, on-brand career coaching voice  
✅ **Role-based prompting** - Creates engaging, relatable persona  
✅ **Security handling** - Comprehensive PII and crisis detection  
✅ **Actionable advice** - Always provides concrete next steps (not generic motivation)  
✅ **Structured output** - JSON action plans for programmatic use  

## 🔧 Configuration

Edit `config.py` to customize:
- Model temperature and parameters
- Safety settings thresholds
- Maximum output tokens


## 🧪 Testing

Run the demo to see all features in action:
```bash
python demo.py
```

The demo tests:
- Career exploration queries
- Structured action plan generation
- PII detection and blocking
- Resume writing attempt blocking
- Professional networking advice

---

**Built for Session 02: Prompt Engineering**  
**Participant: Beloved1310**

