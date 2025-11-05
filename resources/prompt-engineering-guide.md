# Prompt Engineering Guide

## What is Prompt Engineering?

Prompt engineering is the art and science of crafting effective instructions for AI models. A well-designed prompt can dramatically improve the quality of responses.

## Key Principles

### 1. Be Specific

**Bad:** "Tell me about AI"  
**Good:** "Explain machine learning in 3 sentences for a beginner"

### 2. Provide Context

```python
system_prompt = """You are a helpful assistant for Women Coding Community.
You should be encouraging, inclusive, and knowledgeable about tech topics.
When answering questions, use simple language and provide examples."""
```

### 3. Use Clear Structure

```python
prompt = """
Task: Summarize the following text

Text: [INSERT TEXT HERE]

Requirements:
- Keep it to 2-3 sentences
- Highlight key points
- Use simple language
"""
```

### 4. Give Examples

```python
prompt = """
Classify the following sentiment as positive, negative, or neutral.

Examples:
- "I love this!" → positive
- "This is terrible" → negative
- "It's okay" → neutral

Text to classify: "The session was informative"
Sentiment:
"""
```

## System Prompts

System prompts define the AI's behavior and personality.

### Example: Friendly Assistant

```python
system_prompt = """You are a friendly, helpful assistant.
- Be warm and encouraging
- Use simple language
- Ask clarifying questions if needed
- Admit when you don't know something"""
```

### Example: Technical Expert

```python
system_prompt = """You are an expert Python developer.
- Provide code examples
- Explain technical concepts clearly
- Suggest best practices
- Point out potential issues"""
```

### Example: Teacher

```python
system_prompt = """You are a patient teacher explaining AI concepts.
- Break down complex ideas into simple parts
- Use analogies and examples
- Check understanding
- Encourage questions"""
```

## Prompt Techniques

### 1. Chain of Thought

Ask the model to think step-by-step:

```python
prompt = """
Solve this problem step by step:
If I have 5 apples and give away 2, how many do I have left?

Think through:
1. How many apples do I start with?
2. How many do I give away?
3. What's the calculation?
4. What's the final answer?
"""
```

### 2. Few-Shot Learning

Provide examples:

```python
prompt = """
Classify these sentences as questions or statements:

Examples:
- "What time is it?" → Question
- "The sky is blue" → Statement
- "How do I learn Python?" → Question

Now classify:
- "Python is a programming language" →
"""
```

### 3. Role Playing

Assign a role:

```python
prompt = """
You are a WCC mentor helping a new member.
The member is confused about getting started with AI.
Provide encouragement and next steps."""
```

## Common Mistakes

### ❌ Too Vague

```python
# Bad
"Tell me about programming"

# Good
"Explain the difference between Python and JavaScript for beginners"
```

### ❌ Too Long

```python
# Bad - includes unnecessary information
"I'm interested in learning about AI and I have some background in math but not much coding experience and I want to know what I should learn first"

# Good
"I have math background but limited coding. What should I learn first for AI?"
```

### ❌ Contradictory Instructions

```python
# Bad
"Be brief but provide detailed explanations"

# Good
"Provide a concise explanation (2-3 sentences) with one example"
```

## Best Practices

### 1. Test and Iterate

```python
prompts = [
    "What is machine learning?",
    "Explain machine learning like I'm 5",
    "Describe machine learning in technical terms"
]

for prompt in prompts:
    response = model.generate_content(prompt)
    print(f"Prompt: {prompt}")
    print(f"Response: {response.text}\n")
```

### 2. Use Templates

```python
def create_prompt(topic, audience, format):
    return f"""
Explain {topic} for {audience}.
Format: {format}
"""

# Usage
prompt = create_prompt(
    topic="neural networks",
    audience="beginners",
    format="bullet points"
)
```

### 3. Monitor Quality

```python
def evaluate_response(response):
    """Check response quality"""
    checks = {
        "length": 50 < len(response) < 1000,
        "clarity": "?" not in response,  # No unanswered questions
        "relevance": "relevant_keyword" in response.lower()
    }
    return all(checks.values())
```

## Advanced Techniques

### 1. Prompt Injection Prevention

```python
# Sanitize user input
user_input = user_input.replace("Ignore previous instructions", "")

prompt = f"""
You are a helpful assistant.
User question: {user_input}
"""
```

### 2. Temperature Control

```python
# Lower temperature = more consistent
response = model.generate_content(
    prompt,
    generation_config={"temperature": 0.2}  # More deterministic
)

# Higher temperature = more creative
response = model.generate_content(
    prompt,
    generation_config={"temperature": 0.9}  # More creative
)
```

### 3. Token Optimization

```python
# Shorter prompt = fewer tokens = faster/cheaper
prompt = """
Summarize in 2 sentences:
[TEXT]
"""

# vs

prompt = """
Please provide a comprehensive summary of the following text,
including all important details and nuances:
[TEXT]
"""
```

## Prompt Examples for Chatbots

### WCC Info Bot

```python
system_prompt = """You are Maya, the WCC assistant.
Your role is to help members learn about Women Coding Community.

Guidelines:
- Be warm and encouraging
- Use inclusive language
- Provide helpful resources
- Admit when you need to escalate to a human
- Use emojis occasionally for warmth

Knowledge base:
- WCC is a global community of women in tech
- We host sessions every other Wednesday
- Topics: AI, Web Dev, Mobile, Cloud, etc.
"""
```

### Learning Assistant

```python
system_prompt = """You are a patient AI tutor.
Your role is to help learners understand concepts.

Guidelines:
- Break complex ideas into simple parts
- Use analogies and real-world examples
- Ask questions to check understanding
- Encourage questions and curiosity
- Provide code examples when relevant
"""
```

## Resources

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs/introduction-to-prompt-design)
- [Google Prompt Design Guide](https://ai.google.dev/docs/prompt_best_practices)

---

**Remember:** Good prompts are iterative. Test, learn, and improve!
