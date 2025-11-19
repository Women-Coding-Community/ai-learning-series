# 🤖 WCC Info Bot

A smart, interactive chatbot that answers questions about the Women Coding Community (WCC) using:

- A local FAQ database
- Live event scraping from the WCC website
- Google Gemini AI
- A clean Streamlit web interface

This bot provides friendly, helpful, real-time information about WCC, including upcoming events, membership details, volunteering opportunities, and more.

## ✨ Features

### ✅ FAQ Answering
Uses `wcc_faqs.json` to instantly answer commonly asked WCC questions.

### ✅ Live Web Scraping
- Scrapes the WCC events page to fetch real-time events (workshops, webinars, meetups, etc.)
- This means the chatbot always has up-to-date event information

### ✅ AI-Powered Responses
When a question is not in the FAQ list, the chatbot falls back to Google Gemini, with a custom WCC personality.

### ✅ Conversation Memory (Optional)
The bot can remember earlier messages to give more natural responses.

### ✅ Logging + Error Handling
All actions and errors are stored in `app.log`.

### ✅ Simple Streamlit Chat UI
The entire chatbot runs in your browser.

## 📁 Project Structure

```
project/
│── app.py                 # Streamlit user interface
│── chatbot.py             # Gemini logic + FAQ + scraping integration
│── scraper.py             # Web scraper that fetches real WCC event data
│── wcc_faqs.json          # Local FAQ list
│── app.log                # Logging output
│── .env                   # Stores GEMINI_API_KEY
│── README.md
```

## 🛠️ Setup Instructions

### 1️⃣ Install Python 3.9+

Check with:

```bash
python3 --version
```

### 2️⃣ Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

**macOS / Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3️⃣ Install Required Packages

Install dependencies:

```bash
pip install streamlit google-generativeai python-dotenv beautifulsoup4 requests
```

If you have a `requirements.txt`, use:

```bash
pip install -r requirements.txt
```

### 4️⃣ Add Your Gemini API Key

Create a `.env` file:

```
GEMINI_API_KEY=your_key_here
```

Get a free API key here:  
👉 https://makersuite.google.com/app/apikey

### 5️⃣ Verify Your FAQ File

Your `wcc_faqs.json` should contain:

```json
{
  "faqs": [
    {
      "question": "What is WCC?",
      "answer": "Women Coding Community is a global community of women in tech..."
    }
  ]
}
```

## ▶️ How to Run the Chatbot

Run Streamlit:

```bash
streamlit run app.py
```

Open the link shown in the console:

```
http://localhost:8501
```

Start chatting!

## 🧠 How the Chatbot Works Internally

### 1. Loads FAQs
Reads structured Q&A from `wcc_faqs.json`.

### 2. Scrapes Live Events
`scraper.py` fetches:
- event title
- date
- description

from the WCC website.

### 3. Inserts Events Into System Prompt
The bot's system prompt includes the scraped events, so the AI can answer event-related questions accurately.

### 4. FAQ Matching
Before calling Gemini, the bot checks:

```python
if faq["question"].lower() in message.lower():
    return faq["answer"]
```

### 5. Gemini AI Response
If no FAQ matches, the chatbot uses:

```python
self.step_2_add_personality(message)
```

which includes the WCC personality and scraped events.

## 📌 NEW: Web Scraping Feature

*(Added as a bonus and requested by you)*

Your project now includes a fully functional scraper located in `scraper.py`.

### 🔍 What It Does
- Fetches live events from the WCC website
- Parses HTML using BeautifulSoup
- Extracts event titles, dates, and descriptions
- Injects the events into the chatbot's system prompt
- Keeps your chatbot's event info up-to-date automatically
- feedback collection feature for the WCC chatbot

### 📦 Packages Required

```bash
pip install beautifulsoup4 requests
```

### 🧩 How It Integrates with the Chatbot

`chatbot.py` imports and calls the scraper:

```python
from scraper import scrape_wcc_events
events = scrape_wcc_events()
```

Then builds event text:

```python
events_text = "\n".join([
    f"- {e['title']} on {e['date']}: {e['description']}"
    for e in events
])
```

Inserted into system prompt:

```python
system_prompt = f"""
You are a friendly WCC assistant.

Here are the upcoming WCC events:
{events_text}
"""
```

### 🎁 Result

Your chatbot can now answer:
- "What events are happening this month?"
- "When is the next WCC session?"
- "Tell me about upcoming workshops?"

With real live event data.

