# Use Case Guide: WCC Info Bot

## Overview

Build a chatbot that answers frequently asked questions about the Women Coding Community. This bot will help new members learn about WCC events, membership, volunteering, and more.

## Problem Statement

**Challenge:** New WCC members repeatedly ask the same questions about:

- Upcoming events and sessions
- How to join and membership benefits
- Volunteering opportunities
- Community guidelines
- Technical resources

**Solution:** Create an intelligent chatbot that provides instant, consistent answers with personality and warmth.

## What You'll Build

A conversational AI assistant that:

- Answers FAQs about WCC
- Maintains conversation context
- Provides helpful links and resources
- Responds with personality and warmth
- Escalates complex questions to humans

## Tech Stack

- **Language:** Python 3.11+
- **AI Model:** Gemini API (via Vertex AI)
- **Interface:** CLI or Streamlit web app
- **Data:** JSON FAQ file or web scraping

## Step-by-Step Implementation

### Step 1: Create FAQ Data

Create a `wcc_faqs.json` file:

```json
{
  "faqs": [
    {
      "question": "What is WCC?",
      "answer": "Women Coding Community is a global community of women in tech..."
    },
    {
      "question": "How do I join WCC?",
      "answer": "Visit our website and sign up for free..."
    },
    {
      "question": "When are the sessions?",
      "answer": "Sessions are held every other Wednesday at 7 PM EST..."
    },
    {
      "question": "Can I volunteer?",
      "answer": "Absolutely! We're always looking for volunteers..."
    }
  ]
}
```

### Step 2: Enhance the Starter Template

Modify `chatbot.py` to include WCC context:

```python
import json
from chatbot import SimpleBot

# Load WCC FAQs
with open("wcc_faqs.json") as f:
    wcc_data = json.load(f)

# Create FAQ context
faq_text = "\n".join([
    f"Q: {faq['question']}\nA: {faq['answer']}"
    for faq in wcc_data["faqs"]
])

# Create system prompt with WCC knowledge
system_prompt = f"""You are a friendly WCC (Women Coding Community) assistant.
Your role is to help members learn about WCC, answer questions, and encourage participation.

Here are the FAQs you should reference:
{faq_text}

Be warm, encouraging, and inclusive. If you don't know something, suggest they contact the WCC team.
"""

bot = SimpleBot(system_prompt=system_prompt)
```

### Step 3: Add Web Interface (Optional)

Create `app.py` with Streamlit:

```python
import streamlit as st
import json
from chatbot import SimpleBot

st.set_page_config(page_title="WCC Info Bot", page_icon="🤖")

st.title("🤖 WCC Info Bot")
st.markdown("Ask me anything about Women Coding Community!")

# Load FAQs
with open("wcc_faqs.json") as f:
    wcc_data = json.load(f)

faq_text = "\n".join([
    f"Q: {faq['question']}\nA: {faq['answer']}"
    for faq in wcc_data["faqs"]
])

system_prompt = f"""You are a friendly WCC assistant...
{faq_text}"""

# Initialize bot
if "bot" not in st.session_state:
    st.session_state.bot = SimpleBot(system_prompt=system_prompt)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("Ask me about WCC..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    response = st.session_state.bot.chat(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
        st.markdown(response)
```

Run with:

```bash
streamlit run app.py
```

### Step 4: Add Web Scraping (Bonus)

Fetch real WCC data:

```bash
pip install beautifulsoup4 requests
```

Create `scraper.py`:

```python
import requests
from bs4 import BeautifulSoup
import json

def scrape_wcc_events():
    """Scrape upcoming events from WCC website"""
    # Replace with actual WCC website URL
    url = "https://womencoding.community/events"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        events = []
        for event in soup.find_all('div', class_='event'):
            events.append({
                "title": event.find('h3').text,
                "date": event.find('span', class_='date').text,
                "description": event.find('p').text
            })
        
        return events
    except Exception as e:
        print(f"Error scraping: {e}")
        return []

# Use in chatbot
events = scrape_wcc_events()
events_text = "\n".join([
    f"- {e['title']} on {e['date']}: {e['description']}"
    for e in events
])

system_prompt = f"""You are a WCC assistant.
Upcoming events:
{events_text}
"""
```

## Enhancements

### Add Personality

Customize the system prompt:

```python
system_prompt = """You are Maya, the enthusiastic WCC assistant!
You love helping women in tech and are passionate about community.
Always be encouraging and supportive.
Use emojis occasionally to add warmth.
"""
```

### Add Logging

Track conversations:

```python
import logging

logging.basicConfig(filename='chatbot.log', level=logging.INFO)

def log_conversation(user_msg, bot_response):
    logging.info(f"User: {user_msg}")
    logging.info(f"Bot: {bot_response}")
```

### Add Feedback Collection

```python
def get_feedback(rating: int, feedback_text: str):
    """Collect user feedback"""
    with open("feedback.json", "a") as f:
        json.dump({
            "rating": rating,
            "feedback": feedback_text,
            "timestamp": datetime.now().isoformat()
        }, f)
        f.write("\n")
```

## Deployment Options

### Option 1: Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your repo
4. Deploy!

### Option 2: Google Cloud Run

```bash
# Create Dockerfile
cat > Dockerfile << EOF
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
EOF

# Deploy
gcloud run deploy wcc-info-bot --source .
```

### Option 3: Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py" > Procfile

# Deploy
git push heroku main
```

## Testing

Create `test_bot.py`:

```python
from chatbot import SimpleBot

def test_wcc_bot():
    bot = SimpleBot(system_prompt="You are a WCC assistant.")
    
    # Test basic response
    response = bot.chat("What is WCC?")
    assert len(response) > 0
    
    # Test conversation memory
    bot.chat("I'm interested in AI")
    response = bot.chat("Can you recommend a session?")
    assert "AI" in response or "session" in response.lower()
    
    print("✅ All tests passed!")

if __name__ == "__main__":
    test_wcc_bot()
```

Run tests:

```bash
python test_bot.py
```

## Submission Checklist

- ✅ Chatbot responds to user input
- ✅ Conversation memory works
- ✅ WCC-specific knowledge is included
- ✅ Error handling is implemented
- ✅ Code is clean and documented
- ✅ README explains how to run it
- ✅ Deployed or runnable locally

## Resources

- [Starter Template](../starter-template/)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Prompt Engineering Guide](../../../resources/prompt-engineering-guide.md)
- [Streamlit Documentation](https://docs.streamlit.io/)

## Questions?

Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel or reach out to the instructors!

---

Happy building! 🚀
