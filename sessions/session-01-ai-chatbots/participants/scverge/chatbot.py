"""
This is a simple chatbot that uses Gemini API and web scraping to respond to user input.
"""

import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv
import json
import requests
from bs4 import BeautifulSoup

global_encoding = 'utf-8'

sys.stdin.reconfigure(encoding=global_encoding) 
sys.stdout.reconfigure(encoding=global_encoding)

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in environment variables. "
        "Please set it in your .env file or environment."
    )

genai.configure(api_key=API_KEY)

# Load WCC FAQs
with open("wcc_faqs.json", encoding=global_encoding) as f:
    wcc_data = json.load(f)

# Create FAQ context
faq_text = "\n".join([
    f"Q: {faq['question']}\nA: {faq['answer']}"
    for faq in wcc_data["faqs"]
])



def scrape_wcc_events():
    """Scrape upcoming events from WCC website"""

    url = "https://www.womencodingcommunity.com/events"
    
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


#Store the latest events
events = scrape_wcc_events()
events_text = "\n".join([
    f"- {e['title']} on {e['date']}: {e['description']}"
    for e in events
])


class SimpleBot:
    """A simple chatbot using Gemini API"""

    def __init__(self, system_prompt: str = None):
        """
        Initialize the chatbot.

        Args:
            system_prompt: Optional system prompt to set bot personality
        """
        self.model = genai.GenerativeModel(
            "gemini-2.5-flash-lite",
            system_instruction=system_prompt or "You are a helpful assistant."
        )
        self.system_prompt = system_prompt or "You are a helpful assistant."
        self.conversation_history = []

    def chat(self, user_message: str) -> str:
        """
        Send a message and get a response.

        Args:
            user_message: The user's input message

        Returns:
            The bot's response
        """
        try:
            # Add user message to history
            self.conversation_history.append(
                {"role": "user", "parts": [user_message]}
            )

            # Generate response using conversation history
            response = self.model.generate_content(
                self.conversation_history
            )

            # Extract response text
            bot_response = response.text

            # Add bot response to history
            self.conversation_history.append(
                {"role": "model", "parts": [bot_response]}
            )

            return bot_response

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            return error_msg

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []




def main():
    """Main function to run the chatbot"""
    print("Hey :) Welcome to the WCC Chatbot! You can ask me about general info or upcoming events")
    print("Type 'quit' to exit, 'clear' to clear history\n")

    # Create bot with optional system prompt
    system_prompt = f"""You are CeCe, an enthousiastic WCC (Women Coding Community) assistant.
Your role is to help members learn about WCC, answer questions, and encourage participation.
You love helping women in tech and are passionate about community. 
You know their path may be difficult, and you don't want them to give up. 

Here are the FAQs you should reference:
{faq_text}

Here are the Upcoming events:
{events_text}

Always be encouraging and supportive.
Use emojis occasionally to add warmth.
If you don't know something, suggest they contact the WCC team.
"""
    
    bot = SimpleBot(system_prompt=system_prompt)

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "quit":
                print("Goodbye! ")
                break

            if user_input.lower() == "clear":
                bot.clear_history()
                print("Conversation history cleared.\n")
                continue

            # Get response from bot
            response = bot.chat(user_input)
            print(f"\nBot: {response}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye! ")
            break


if __name__ == "__main__":
    main()
