# Alternative Platforms Guide

While we recommend GCP/Vertex AI for this course, you can use any of these platforms. The concepts remain the same!

## AWS - Bedrock & SageMaker

### Setup

1. Create an AWS account at [aws.amazon.com](https://aws.amazon.com)
2. Enable Bedrock in your region
3. Install AWS SDK:

```bash
pip install boto3
```

### Basic Usage

```python
import boto3

client = boto3.client('bedrock-runtime', region_name='us-east-1')

response = client.invoke_model(
    modelId='anthropic.claude-3-sonnet-20240229-v1:0',
    body=json.dumps({
        "prompt": "What is AI?",
        "max_tokens": 1024
    })
)

print(response['body'].read().decode())
```

### Pros

- Tight AWS ecosystem integration
- Strong enterprise support
- Multiple model options (Claude, Llama, Titan)

### Cons

- Steeper learning curve for beginners
- Less generous free tier than GCP

---

## Azure - OpenAI Service

### Setup

1. Create Azure account at [azure.microsoft.com](https://azure.microsoft.com)
2. Create OpenAI resource
3. Install SDK:

```bash
pip install openai
```

### Basic Usage

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="your-api-key",
    api_version="2024-02-15-preview",
    azure_endpoint="https://your-resource.openai.azure.com/"
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What is AI?"}]
)

print(response.choices[0].message.content)
```

### Pros

- Direct access to GPT-4
- Enterprise-grade security
- Good for organizations already using Azure

### Cons

- Higher pricing than GCP free tier
- Requires Azure account setup

---

## OpenAI - Direct API

### Setup

1. Create account at [openai.com](https://openai.com)
2. Generate API key
3. Install SDK:

```bash
pip install openai
```

### Basic Usage

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What is AI?"}]
)

print(response.choices[0].message.content)
```

### Pros

- Simple, straightforward API
- Excellent documentation
- Most popular choice

### Cons

- Pay-as-you-go pricing (no free tier)
- Can get expensive quickly

---

## Anthropic - Claude

### Setup

1. Create account at [console.anthropic.com](https://console.anthropic.com)
2. Generate API key
3. Install SDK:

```bash
pip install anthropic
```

### Basic Usage

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

response = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1024,
    messages=[{"role": "user", "content": "What is AI?"}]
)

print(response.content[0].text)
```

### Pros

- Excellent reasoning capabilities
- Strong safety features
- Good documentation

### Cons

- No free tier
- Smaller ecosystem than OpenAI

---

## Cohere

### Setup

1. Create account at [cohere.com](https://cohere.com)
2. Generate API key
3. Install SDK:

```bash
pip install cohere
```

### Basic Usage

```python
import cohere

client = cohere.ClientV2(api_key="your-api-key")

response = client.chat(
    model="command-r-plus",
    messages=[{"role": "user", "content": "What is AI?"}]
)

print(response.message.content[0].text)
```

### Pros

- Good for enterprise use cases
- Strong multilingual support
- Competitive pricing

### Cons

- Smaller community than OpenAI
- Less documentation

---

## Platform Comparison

| Feature | GCP/Vertex AI | AWS Bedrock | Azure OpenAI | OpenAI | Claude | Cohere |
|---------|---------------|-------------|--------------|--------|--------|--------|
| Free Tier | $300 credits | Limited | No | No | No | Limited |
| Ease of Setup | Easy | Medium | Medium | Easy | Easy | Easy |
| Model Variety | Good | Excellent | Good | Excellent | Good | Good |
| Documentation | Excellent | Good | Good | Excellent | Excellent | Good |
| Enterprise Support | Excellent | Excellent | Excellent | Good | Good | Excellent |
| Cost | Low (free tier) | Medium | High | Medium | High | Medium |

---

## Adapting Your Code

Most concepts work across platforms. Here's how to adapt:

### Conversation Memory

All platforms support conversation history - just maintain a list of messages and send them with each request.

### Error Handling

Each platform has different error types, but the pattern is the same:

```python
try:
    response = call_api()
except PlatformSpecificError as e:
    print(f"Error: {e}")
```

### Rate Limiting

All platforms have rate limits. Implement exponential backoff:

```python
import time

def call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait_time = 2 ** attempt
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
```

---

## Recommendation for This Course

**Start with GCP/Vertex AI** because:

- Free $300 credits = no cost to learn
- Simple, Pythonic API
- Great for beginners
- Easy to scale to production

Once comfortable, try other platforms to see the differences!

---

**Need Help Choosing?**

- Ask in the WCC Slack channel
- Check platform documentation
- Start with free tier options
