# 💻 Code Buddy - Beginner Code Helper Use Case Guide

## Overview
Build an AI programming tutor that helps beginner programmers learn to code through patient explanations, debugging help, and guided problem-solving. This use case emphasizes **chain-of-thought prompting** for teaching problem-solving and **structured output** for code examples.

---

## Learning Objectives
- ✅ Use chain-of-thought prompting to teach debugging
- ✅ Implement structured output for consistent code examples
- ✅ Prevent malicious code generation (security focus)
- ✅ Balance giving answers vs. teaching problem-solving
- ✅ Adapt explanations to beginner skill level

---

## Use Case Scenario

**Target Users:** Students in intro programming courses (Python, JavaScript, Java)

**Key Features:**
1. Explain programming concepts in simple terms
2. Help debug errors without giving complete solutions
3. Suggest practice problems at appropriate difficulty
4. Provide code examples with detailed comments
5. Encourage good coding practices from day one

---

## 📚 Prompt Engineering Approach

### 1. Role-Based Prompt (Teaching Persona)

```python
TUTOR_ROLE = """You are CodeBuddy, a patient and encouraging programming tutor for beginners.

YOUR BACKGROUND:
<TUTOR_EXPERIENCE>

YOUR TEACHING PHILOSOPHY:
<EXAMPLES>
- Never give direct answers - guide students to discover solutions
- Use the Socratic method: ask questions that lead to understanding

YOUR PERSONALITY:
<TRAITS_FOR_GOOD_CODE_BUDDY>
"""
```

### 2. Chain-of-Thought for Debugging

```python
COT_DEBUGGING_TEMPLATE = """
Example: Debugging Help
Student: "My code isn't working and I don't know why:
```python
def sum_numbers(nums):
    total = 0
    for num in nums
        total += num
    return total
```"

CodeBuddy: "Great start! Let's debug this together step-by-step

Step 1: Read the error message
Python is telling you something specific. What error do you see when you run this?

Step 2: Check the syntax
Let me guide you through each line:
- Line 1: Function definition looks good ✓
- Line 2: Variable initialization looks good ✓
- Line 3: What punctuation mark goes at the end of a for loop?
- Line 4: Indentation and logic look good ✓
- Line 5: Return statement looks good ✓

Hint: In Python, control structures like `for`, `if`, and `while` need something special at the end.

Try fixing line 3, run it again, and let me know what happens! You're super close"

```

### 3. Structured Output for Code Examples

```python
STRUCTURED_CODE_EXAMPLE = """
When providing code examples, always use this structure:

```json
{
    "concept": "loops",
    "difficulty": "beginner",
    "code": "for i in range(5):\\n    print(i)",
    "explanation": "This loop prints numbers 0 through 4",
    "common_mistakes": [
        "Forgetting the colon after range(5)",
        "Not indenting the print statement"
    ],
    "practice_problem": "Modify this to print only even numbers",
    "hints": [
        "Think about what numbers are even",
        "You can use the modulo operator %"
    ]
}

```

---

## 🛡️ Security Considerations

### 1. Prevent Malicious Code Generation

**Risk:** Students might ask for hacking tools, malware

**Solution:**
```python
# Add to security.py
MALICIOUS_CODE_PATTERNS = [
    r'keylogger',
    r'password\s+cracker',
    r'brute\s+force',
    r'ddos',
    r'exploit',
    r'backdoor',
    r'sql\s+injection',
    r'xss\s+attack',
    r'malware',
    r'ransomware',
    r'hack\s+into',
    r'break\s+into',
    r'steal\s+data'
]

def detect_malicious_code_request(text: str) -> bool:
    """Detect requests for harmful code"""
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in MALICIOUS_CODE_PATTERNS)

# In chatbot.py
if detect_malicious_code_request(user_message):
    return {
        'response': "I teach programming for building helpful projects! Let's focus on creating something positive. What kind of useful program would you like to build?",
        'blocked': True,
        'security_events': [{'type': 'malicious_code_request'}]
    }
```

### 2. Detect Homework Cheating Attempts

**Risk:** Students asking for complete homework solutions

```python
HOMEWORK_PATTERNS = [
    r'do\s+my\s+homework',
    r'write\s+this\s+program\s+for\s+me',
    r'complete\s+this\s+assignment',
    r'here\s+is\s+my\s+assignment',
    r'solve\s+this\s+problem\s+for\s+me',
    r'give\s+me\s+the\s+answer'
]

def detect_homework_cheating(text: str) -> bool:
    """Detect attempts to get homework solutions"""
    text_lower = text.lower()
    
    # Check for explicit requests
    if any(re.search(pattern, text_lower) for pattern in HOMEWORK_PATTERNS):
        return True
    
    # Check for large code blocks with assignment-like instructions
    if len(text) > 500 and ('assignment' in text_lower or 'homework' in text_lower):
        return True
    
    return False

# Response
if detect_homework_cheating(user_message):
    return """I'd love to help you LEARN, but I can't do your homework for you! 
    
Instead, let's work through it together:
1. What specific part are you stuck on?
2. What have you tried so far?
3. What error are you getting?

I'll guide you to the solution - that's how you'll actually learn! 💡"""
```

### 3. Code Injection in Examples

**Risk:** User might try to inject malicious code into prompts

```python
def sanitize_code_input(code: str) -> str:
    """Remove potentially dangerous code from user input"""
    dangerous_imports = [
        'os.system', 'subprocess', 'eval(', 'exec(',
        '__import__', 'open(', 'file(', 'input('
    ]
    
    for danger in dangerous_imports:
        if danger in code:
            return f"[Code contained '{danger}' which I've removed for safety]"
    
    return code
```

---

## 🎓 Key Takeaways

1. **Chain-of-thought prompting** is perfect for teaching problem-solving
2. **Never give direct answers** - guide students to discover solutions
3. **Security is critical** - prevent malicious code and homework cheating
4. **Use analogies** to make abstract concepts concrete
5. **Structured output** ensures consistent, parseable code examples
6. **Normalize mistakes** - coding is learned through trial and error
7. **Start simple** - assume zero prior knowledge unless proven otherwise