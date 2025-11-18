# Code Buddy - Beginner Code Helper Use Case Guide

## Overview

Build a friendly AI assistant that helps beginners understand code, debug issues, and learn programming concepts through conversational explanations and code analysis.

---

## Problem Statement

**Challenge:** Beginner programmers struggle with:

- Understanding complex code snippets
- Debugging errors without clear explanations
- Learning programming concepts in isolation
- Getting quick help without waiting for mentors
- Understanding error messages and stack traces

**Why it matters:** Quick, friendly code help accelerates learning and builds confidence for beginners.

---

## What You'll Build

A conversational code helper that:

- Explains code in beginner-friendly language
- Analyzes code snippets and identifies issues
- Suggests debugging strategies
- Explains error messages
- Teaches programming concepts
- Provides code examples and best practices
- Maintains conversation context for learning

---

## Architecture

```text
┌──────────────────────┐
│   Code Input         │
│  (Snippet/Error)     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────────────┐
│   Gemini API with Code Buddy Persona │
│  (System Prompt: Beginner-friendly)  │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│   Code Analysis                      │
│  (Syntax, logic, best practices)     │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│   Formatted Response                 │
│  (Explanation, fixes, resources)     │
└──────────────────────────────────────┘
```

---

## Step 1: Create Code Helper Data

Create `code_helper_data.py` with programming knowledge:

```python
PROGRAMMING_CONCEPTS = {
    "variables": "Containers that store data values",
    "loops": "Repeat code blocks multiple times",
    "functions": "Reusable blocks of code",
    "conditionals": "Make decisions based on conditions",
    "lists": "Collections of items",
    "dictionaries": "Key-value pairs for organizing data",
    "classes": "Blueprints for creating objects",
    "errors": "Messages telling you what went wrong"
}

COMMON_ERRORS = {
    "NameError": "Variable or function not defined",
    "TypeError": "Wrong data type for operation",
    "IndexError": "Accessing list index that doesn't exist",
    "KeyError": "Dictionary key doesn't exist",
    "SyntaxError": "Code structure is incorrect",
    "IndentationError": "Incorrect spacing/indentation",
    "AttributeError": "Object doesn't have that attribute",
    "ValueError": "Value is wrong type or format"
}

DEBUGGING_TIPS = [
    "Read the error message carefully - it tells you what's wrong",
    "Check the line number where the error occurred",
    "Print variables to see their values",
    "Use a debugger to step through code",
    "Check for typos in variable names",
    "Verify data types match what you expect",
    "Test with simple examples first",
    "Break complex code into smaller pieces"
]

BEST_PRACTICES = {
    "naming": "Use clear, descriptive variable names",
    "comments": "Explain WHY, not WHAT",
    "functions": "Keep functions small and focused",
    "testing": "Test your code with different inputs",
    "readability": "Write code others can understand",
    "dry": "Don't Repeat Yourself - use functions",
    "error_handling": "Handle errors gracefully"
}
```

---

## Step 2: Enhance the Starter Template

Modify `chatbot.py` with a code buddy system prompt:

```python
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-project-id")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")

aiplatform.init(project=PROJECT_ID, location=LOCATION)

CODE_BUDDY_PROMPT = """You are Code Buddy, a friendly AI assistant helping beginner programmers learn and debug code.

Your personality:
- Encouraging and patient
- Explain concepts simply without jargon
- Celebrate small wins
- Never make beginners feel bad about mistakes

When helping with code:
1. Read the code carefully
2. Identify the issue or question
3. Explain in simple terms
4. Provide a corrected version if needed
5. Explain WHY the fix works
6. Suggest how to prevent similar issues

When explaining concepts:
- Use analogies and real-world examples
- Break down complex ideas
- Provide simple code examples
- Ask if they understand before moving on

When debugging:
- Read error messages together
- Explain what the error means
- Help them find the root cause
- Guide them to the solution

Topics you can help with:
- Python basics (variables, loops, functions)
- Understanding error messages
- Debugging code
- Code structure and organization
- Best practices for beginners
- Common programming mistakes
- How to approach problem-solving

Remember: There are no stupid questions! Learning to code takes practice."""

class CodeBuddy:
    """Friendly AI code helper for beginners"""

    def __init__(self):
        self.model = GenerativeModel("gemini-2.5-flash-lite")
        self.system_prompt = CODE_BUDDY_PROMPT
        self.conversation_history = []
        self.learning_topics = []

    def chat(self, user_message: str) -> str:
        """Help with code questions"""
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

    def explain_error(self, error_message: str) -> str:
        """Explain what an error means"""
        prompt = f"I got this error: {error_message}. Can you explain what it means?"
        return self.chat(prompt)

    def debug_code(self, code_snippet: str) -> str:
        """Help debug a code snippet"""
        prompt = f"Can you help me debug this code?\n\n{code_snippet}"
        return self.chat(prompt)

    def explain_concept(self, concept: str) -> str:
        """Explain a programming concept"""
        prompt = f"Can you explain {concept} in simple terms?"
        return self.chat(prompt)

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


def main():
    """Run Code Buddy chatbot"""
    print("👨‍💻 Welcome to Code Buddy!")
    print("Your friendly AI code helper")
    print("Type 'quit' to exit, 'clear' to clear history\n")

    buddy = CodeBuddy()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            print("Buddy: Great learning with you! Keep coding! 🚀")
            break

        if user_input.lower() == "clear":
            buddy.clear_history()
            print("Buddy: Conversation cleared. Let's start fresh!\n")
            continue

        if not user_input:
            continue

        response = buddy.chat(user_input)
        print(f"\nBuddy: {response}\n")


if __name__ == "__main__":
    main()
```

---

## Step 3: Add Code Analysis Features

Enhance with code-specific analysis:

```python
import re

class CodeBuddyWithAnalysis(CodeBuddy):
    """Code Buddy with code analysis features"""

    def analyze_code(self, code_snippet: str) -> dict:
        """Analyze code for common issues"""
        analysis = {
            "syntax_issues": [],
            "style_issues": [],
            "suggestions": []
        }

        lines = code_snippet.split('\n')

        # Check for common issues
        for i, line in enumerate(lines, 1):
            # Check indentation
            if line and line[0] == ' ' and not line.startswith('    '):
                analysis["style_issues"].append(
                    f"Line {i}: Inconsistent indentation"
                )

            # Check for print statements (debugging)
            if 'print(' in line:
                analysis["suggestions"].append(
                    f"Line {i}: Consider using a debugger instead of print()"
                )

            # Check for undefined variables
            if '=' in line and not any(x in line for x in ['==', '!=']):
                var_name = line.split('=')[0].strip()
                if var_name and not var_name.startswith('#'):
                    analysis["suggestions"].append(
                        f"Line {i}: Variable '{var_name}' defined"
                    )

        return analysis

    def format_code_response(self, code_snippet: str, explanation: str) -> str:
        """Format response with code highlighting"""
        response = f"""
**Explanation:**
{explanation}

**Code:**
```python
{code_snippet}
```

**Tips:**

- Read error messages carefully
- Test with different inputs
- Use comments to explain your logic
"""
        return response

    def suggest_improvements(self, code_snippet: str) -> str:
        """Suggest code improvements"""
        prompt = f"""Review this code and suggest improvements for readability and best practices:

python
{code_snippet}

```

Focus on:

1. Naming conventions
2. Code organization
3. Comments and documentation
4. Error handling
5. Performance"""
        return self.chat(prompt)
```

---

## Step 4: Create Web Interface (Optional)

Use Streamlit for interactive code help:

```python
import streamlit as st
from code_buddy import CodeBuddyWithAnalysis

st.set_page_config(page_title="Code Buddy", layout="wide")

st.title("👨‍💻 Code Buddy - Beginner Code Helper")
st.markdown("Your friendly AI assistant for learning and debugging code")

# Initialize buddy
if "buddy" not in st.session_state:
    st.session_state.buddy = CodeBuddyWithAnalysis()

# Tabs for different features
tab1, tab2, tab3 = st.tabs(["Chat", "Debug Code", "Explain Error"])

with tab1:
    st.subheader("Chat with Code Buddy")

    # Display conversation
    for msg in st.session_state.buddy.conversation_history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    # Input
    user_input = st.chat_input("Ask Code Buddy a question...")
    if user_input:
        st.chat_message("user").write(user_input)
        response = st.session_state.buddy.chat(user_input)
        st.chat_message("assistant").write(response)
        st.rerun()

with tab2:
    st.subheader("Debug Your Code")
    code_input = st.text_area("Paste your code here:", height=200)

    if st.button("Debug This Code"):
        if code_input:
            response = st.session_state.buddy.debug_code(code_input)
            st.write(response)
        else:
            st.warning("Please paste some code first!")

with tab3:
    st.subheader("Explain an Error")
    error_input = st.text_area("Paste your error message here:", height=100)

    if st.button("Explain This Error"):
        if error_input:
            response = st.session_state.buddy.explain_error(error_input)
            st.write(response)
        else:
            st.warning("Please paste an error message first!")

# Sidebar with resources
st.sidebar.header("📚 Learning Resources")
st.sidebar.markdown("""
**Python Basics:**
- [Python.org Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com)
- [Codecademy](https://codecademy.com)

**Practice:**
- [HackerRank](https://hackerrank.com)
- [Codewars](https://codewars.com)
- [LeetCode Easy](https://leetcode.com)

**Debugging:**
- [Python Debugger Guide](https://docs.python.org/3/library/pdb.html)
- [Stack Overflow](https://stackoverflow.com)
""")

if st.sidebar.button("Clear Conversation"):
    st.session_state.buddy.clear_history()
    st.success("Conversation cleared!")
```

---

## Step 5: Testing

Test with common beginner scenarios:

```python
def test_code_buddy():
    """Test Code Buddy with sample questions"""
    buddy = CodeBuddyWithAnalysis()

    test_cases = [
        "What's the difference between = and ==?",
        """I got this error: NameError: name 'x' is not defined
What does it mean?""",
        """Can you explain this code?
for i in range(5):
    print(i)""",
        """I'm trying to add items to a list but it's not working:
my_list = [1, 2, 3]
my_list.add(4)
print(my_list)""",
        "How do I write a function?"
    ]

    for question in test_cases:
        print(f"\n👤 You: {question}")
        response = buddy.chat(question)
        print(f"👨‍💻 Buddy: {response}\n")
        print("-" * 80)

if __name__ == "__main__":
    test_code_buddy()
```

---

## Deployment Options

### Option 1: Local CLI

```bash
python code_buddy.py
```

### Option 2: Streamlit Web App

```bash
streamlit run code_buddy_web.py
```

### Option 3: Discord Bot

Integrate with WCC Discord for instant code help

### Option 4: VS Code Extension

Create an extension for inline code help

---

## Enhancement Ideas

- **Syntax Highlighting:** Format code with proper syntax highlighting
- **Code Formatter:** Auto-format messy code
- **Error Database:** Common errors with explanations
- **Code Snippets:** Library of common patterns
- **Progress Tracking:** Track topics learned
- **Quiz Mode:** Test understanding of concepts
- **Video Tutorials:** Link to relevant tutorials
- **Peer Review:** Get feedback from other learners

---

## Common Questions

**Q: Can it help with languages other than Python?**  
A: Yes! Modify the system prompt to include JavaScript, Java, etc.

**Q: How accurate are the explanations?**  
A: Very accurate for common beginner issues. Always verify with official docs.

**Q: Can I use this for advanced code?**  
A: It's designed for beginners, but can help with intermediate code too.

**Q: How do I make it better at explaining?**  
A: Provide feedback and refine the system prompt based on what works.

---

## Submission Checklist

- ✅ Code Buddy responds to code questions
- ✅ Can explain errors and debug code
- ✅ Uses beginner-friendly language
- ✅ Maintains conversation context
- ✅ Handles code snippets properly
- ✅ README with setup and usage
- ✅ Test cases with example interactions
- ✅ Optional: Web interface with syntax highlighting

---

## Resources

- [Gemini API Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini-api)
- [Python Documentation](https://docs.python.org)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Real Python Tutorials](https://realpython.com)
- [Python Error Messages](https://docs.python.org/3/tutorial/errors.html)

---

## Questions?

Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel or reach out to the instructors!

---

**Happy coding! Help your peers learn! 🚀**
