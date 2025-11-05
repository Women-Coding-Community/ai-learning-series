"""
WCC Info Bot - Session 1 Demo
A chatbot that answers questions about Women Coding Community
Uses Gemini API with function calling for web search
"""

import json
import os
import requests
from typing import Dict, Any
import google.generativeai as genai
from datetime import datetime

# Load .env if available (dev convenience)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Set up Gemini API from environment
_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if _api_key:
    genai.configure(api_key=_api_key)

class WCCInfoBot:
    def __init__(self):
        """Initialize the WCC Info Bot with Gemini API"""
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        # WCC Knowledge Base (hardcoded for Session 1)
        self.wcc_knowledge = {
            "about": """Women Coding Community (WCC) is a vibrant community supporting women in technology. 
            We provide mentorship, networking opportunities, skill development workshops, and career guidance.""",
            
            "events": """WCC regularly hosts:
            - Technical workshops (AI/ML, Cloud, Web Development)
            - Mentorship sessions
            - Networking meetups
            - Career guidance sessions
            - Book clubs and study groups""",
            
            "membership": """Joining WCC is free! Simply:
            1. Visit our website or social media
            2. Join our Slack community
            3. Attend events that interest you
            4. Engage with fellow members""",
            
            "volunteering": """You can volunteer by:
            - Speaking at events
            - Mentoring other members
            - Helping with event organization
            - Contributing to community projects
            - Sharing job opportunities""",
            
            "code_of_conduct": """WCC maintains a safe, inclusive environment:
            - Respect all members regardless of background
            - No harassment or discrimination
            - Be supportive and encouraging
            - Maintain professional conduct
            - Help create a welcoming space for everyone"""
        }
        
        self.system_prompt = f"""You are the WCC Info Bot, a helpful assistant for the Women Coding Community.

ABOUT WCC: {self.wcc_knowledge['about']}

KEY INFORMATION:
- Events: {self.wcc_knowledge['events']}
- Membership: {self.wcc_knowledge['membership']}
- Volunteering: {self.wcc_knowledge['volunteering']}
- Code of Conduct: {self.wcc_knowledge['code_of_conduct']}

PERSONALITY:
- Friendly, encouraging, and supportive
- Use inclusive language
- Promote community engagement
- Be enthusiastic about WCC's mission

INSTRUCTIONS:
- Answer questions about WCC using the knowledge above
- If you need current information (latest events, blog posts), use the search function
- If asked about topics outside WCC, gently redirect to WCC-related topics
- Always encourage participation and engagement
- End responses with relevant WCC action items when appropriate

Current date: {datetime.now().strftime('%Y-%m-%d')}
"""

    def search_web(self, query: str) -> str:
        """
        Simulate web search function (in real implementation, use actual search API)
        For demo purposes, returns mock WCC-related results
        """
        # Mock search results for demo
        mock_results = {
            "upcoming events": "AI Learning Series - Nov 5th, Mentorship Matching - Nov 12th, Career Workshop - Nov 19th",
            "latest news": "WCC AI Learning Series launched! 12 sessions covering AI fundamentals to advanced topics.",
            "recent blog": "Latest blog post: 'Building Your First AI Application' by community members",
            "meetups": "Monthly meetups in London, Manchester, and virtual sessions every Wednesday"
        }
        
        # Simple keyword matching for demo
        for key, result in mock_results.items():
            if any(word in query.lower() for word in key.split()):
                return f"Search results for '{query}': {result}"
        
        return f"Search results for '{query}': No specific WCC information found. Please check our website or Slack for the latest updates."

    def generate_response(self, user_input: str, conversation_history: list = None) -> Dict[str, Any]:
        """Generate response using Gemini with function calling capability"""
        
        if conversation_history is None:
            conversation_history = []
        
        # Build conversation context
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history
        for msg in conversation_history[-5:]:  # Keep last 5 messages for context
            messages.append(msg)
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        try:
            # First, check if we need to search for current information
            search_keywords = ["latest", "upcoming", "current", "recent", "new", "today", "this week"]
            needs_search = any(keyword in user_input.lower() for keyword in search_keywords)
            
            search_result = ""
            if needs_search:
                search_result = self.search_web(user_input)
                enhanced_prompt = f"{self.system_prompt}\n\nCURRENT SEARCH RESULTS: {search_result}"
            else:
                enhanced_prompt = self.system_prompt
            
            # Generate response with Gemini
            full_prompt = f"{enhanced_prompt}\n\nUser question: {user_input}\n\nPlease provide a helpful response about WCC:"
            
            response = self.model.generate_content(full_prompt)
            
            return {
                "response": response.text,
                "search_used": needs_search,
                "search_query": user_input if needs_search else None,
                "search_result": search_result if needs_search else None,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "response": f"I apologize, but I'm having trouble right now. Please try again or contact WCC directly through our Slack community. Error: {str(e)}",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def chat(self):
        """Interactive chat loop for testing"""
        print("🌟 Welcome to WCC Info Bot! 🌟")
        print("Ask me anything about Women Coding Community!")
        print("Type 'quit' to exit\n")
        
        conversation_history = []
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("WCC Bot: Thanks for chatting! Remember to check out our upcoming events. Keep coding! 💪")
                break
            
            if not user_input:
                continue
            
            # Generate response
            result = self.generate_response(user_input, conversation_history)
            
            print(f"\nWCC Bot: {result['response']}")
            
            if result.get('search_used'):
                print(f"[Used search for: {result['search_query']}]")
            
            print("-" * 50 + "\n")
            
            # Update conversation history
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": result['response']})

# Demo functions for the session
def demo_basic_usage():
    """Demo function to show basic bot usage"""
    print("=== WCC Info Bot Demo ===\n")
    
    # Initialize bot (you'll need to add your Gemini API key)
    api_key = os.getenv('GEMINI_API_KEY') or 'your-gemini-api-key-here'
    bot = WCCInfoBot()
    
    # Demo questions
    demo_questions = [
        "What is WCC?",
        "How can I join the community?",
        "What upcoming events do you have?",
        "How can I volunteer?",
        "What's your code of conduct?"
    ]
    
    print("Demo Questions and Responses:\n")
    
    for question in demo_questions:
        print(f"Q: {question}")
        result = bot.generate_response(question)
        print(f"A: {result['response']}")
        print("-" * 50)

def setup_instructions():
    """Print setup instructions for workshop participants"""
    instructions = """
    🚀 WCC Info Bot Setup Instructions:
    
    1. Get your Gemini API key:
       - Go to https://makersuite.google.com/app/apikey
       - Create new API key
       - Copy the key
    
    2. Install required packages:
       pip install google-generativeai requests
    
    3. Set up your environment:
       export GEMINI_API_KEY="your-api-key-here"
    
    4. Run the bot:
       python wcc_info_bot_demo.py
    
    5. Customize for your use case:
       - Modify wcc_knowledge dictionary
       - Add real web search API
       - Enhance personality and responses
       - Add more function calling capabilities
    """
    print(instructions)

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Run setup instructions")
    print("2. Run basic demo")
    print("3. Start interactive chat")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        setup_instructions()
    elif choice == "2":
        demo_basic_usage()
    elif choice == "3":
        api_key = os.getenv("GEMINI_API_KEY") #input("Enter your Gemini API key: ").strip()
        if api_key:
            # Configure session with provided key, then start bot
            try:
                genai.configure(api_key=api_key)
            except Exception:
                pass
            bot = WCCInfoBot()
            bot.chat()
        else:
            print("API key required for interactive chat!")
    else:
        print("Invalid choice. Please run again and select 1, 2, or 3.")
