#!/usr/bin/env python3
"""
WCC AI Learning Series - Session 1 Live Demo
Progressive Chatbot Building - Modular Approach

INSTRUCTIONS FOR LIVE DEMO:
Comment/uncomment method calls at the bottom to show each step:

Step 1: step_1_basic_api_call()
Step 2: step_2_add_personality()
Step 3: step_3_conversation_memory()
Step 4: step_4_model_parameters()
Step 5: step_5_streamlit_interface()

Each step builds on the previous one, showing clear code differences!
"""

import os
import google.generativeai as genai
from datetime import datetime


MODEL_ID = 'gemini-2.5-flash-lite'

# Load .env if available (dev convenience)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Configure Gemini API (done once at startup)
api_key = os.getenv('GEMINI_API_KEY') or 'your-gemini-api-key-here'
genai.configure(api_key=api_key)

print("🚀 WCC AI Learning Series - Session 1 Demo")
print("=" * 50)

# =============================================================================
# SHARED SYSTEM PROMPT (Used by Steps 2-5)
# =============================================================================

WCC_SYSTEM_PROMPT = '''You are a helpful and enthusiastic assistant for the Women Coding Community (WCC).

ABOUT WCC:
- WCC is a vibrant community supporting women in technology
- We provide mentorship, networking, skill development workshops, and career guidance
- Our mission is to create an inclusive space for women to grow in tech careers
- We host regular events: technical workshops, mentorship sessions, networking meetups

PERSONALITY:
- Friendly, encouraging, and supportive
- Use inclusive language and be welcoming
- Be enthusiastic about WCC's mission
- Always try to connect answers back to community engagement

HOW TO HELP:
- Answer questions about WCC programs and events
- Encourage participation and community involvement
- Provide supportive advice for women in tech
- If you don't know something specific, suggest they check our Slack or website
'''


# =============================================================================
# STEP 1: BASIC API CALL
# =============================================================================

def step_1_basic_api_call():
    """
    STEP 1: Make a simple API call to Gemini
    
    What we're learning:
    - How to create a model instance
    - How to send a prompt and get a response
    """
    print("\n" + "=" * 60)
    print("STEP 1: Basic API Call")
    print("=" * 60)
    
    # Create the simplest possible model instance
    model = genai.GenerativeModel(MODEL_ID)
    
    # Make a simple request
    print("\n📝 Sending prompt: 'What is Women Coding Community (WCC)?'")
    response = model.generate_content("What is Women Coding Community (WCC)?")
    
    print(f"\n✅ Response:\n{response.text}")
    print("\n🎉 SUCCESS! You just talked to AI! 🎉\n")


# =============================================================================
# STEP 2: ADD PERSONALITY WITH SYSTEM PROMPTS
# =============================================================================

def step_2_add_personality():
    """
    STEP 2: Add personality using system prompts
    
    What we're learning:
    - How system prompts shape AI behavior
    - How to give the AI a specific role/personality
    - The difference between generic and specialized responses
    """
    print("\n" + "=" * 60)
    print("STEP 2: Adding Personality with System Prompts")
    print("=" * 60)
    
    # Create model WITH system prompt (compare to Step 1)
    model_with_personality = genai.GenerativeModel(
        MODEL_ID,
        system_instruction=WCC_SYSTEM_PROMPT
    )
    
    # Test questions
    test_questions = [
        "What is WCC?",
        "How can I join?", 
        "I'm new to coding, can WCC help me?"
    ]
    
    print("\n📝 Testing with WCC-specific system prompt:\n")
    for question in test_questions:
        print(f"Q: {question}")
        response = model_with_personality.generate_content(question)
        print(f"A: {response.text}\n")
        print("-" * 40)
    
    print("\n🌟 NOTICE: Responses are now WCC-focused and friendly! 🌟\n")


# =============================================================================
# STEP 3: ADD CONVERSATION MEMORY
# =============================================================================

def step_3_conversation_memory():
    """
    STEP 3: Add conversation memory
    
    What we're learning:
    - How to maintain conversation context
    - How to build multi-turn conversations
    - How memory improves user experience
    """
    print("\n" + "=" * 60)
    print("STEP 3: Adding Conversation Memory")
    print("=" * 60)
    
    class WCCChatBot:
        """Chatbot with conversation memory"""
        
        def __init__(self):
            self.model = genai.GenerativeModel(
                MODEL_ID,
                system_instruction=WCC_SYSTEM_PROMPT
            )
            self.conversation_history = []
        
        def chat(self, user_input):
            """Send message and get response with context"""
            # Add user message to history
            self.conversation_history.append({"role": "user", "parts": [user_input]})
            
            # Generate response with full history
            response = self.model.generate_content(self.conversation_history)
            
            # Add assistant response to history
            self.conversation_history.append({"role": "model", "parts": [response.text]})
            
            return response.text
    
    # Create chatbot instance
    chatbot = WCCChatBot()
    
    print("\n💬 Testing conversation memory:\n")
    
    # First message
    msg1 = "Hi, I'm Sarah and I'm new to programming"
    print(f"You: {msg1}")
    response1 = chatbot.chat(msg1)
    print(f"Bot: {response1}\n")
    
    # Second message (bot should remember Sarah)
    msg2 = "What programming language should I start with?"
    print(f"You: {msg2}")
    response2 = chatbot.chat(msg2)
    print(f"Bot: {response2}\n")
    
    # Third message (bot should remember name and context)
    msg3 = "Do you remember my name?"
    print(f"You: {msg3}")
    response3 = chatbot.chat(msg3)
    print(f"Bot: {response3}\n")
    
    print("🧠 NOTICE: Bot remembers Sarah and the conversation context! 🧠\n")


# =============================================================================
# STEP 4: EXPLORE MODEL PARAMETERS
# =============================================================================

def step_4_model_parameters():
    """
    STEP 4: Explore model parameters
    
    What we're learning:
    - How temperature affects creativity
    - How top_p affects diversity
    - How to tune parameters for different use cases
    """
    print("\n" + "=" * 60)
    print("STEP 4: Understanding Model Parameters")
    print("=" * 60)
    
    question = "Write a creative welcome message for new WCC members"
    
    print(f"\n📝 Question: {question}\n")
    print("🌡️ TEMPERATURE EXAMPLES (Creativity):\n")
    
    temperatures = [
        (0.0, "Deterministic - Same answer every time"),
        (0.7, "Balanced - Recommended for most use cases"),
        (1.5, "Very Creative - Different each time")
    ]
    
    for temp, description in temperatures:
        print(f"Temperature: {temp} ({description})")
        print("-" * 40)
        
        generation_config = genai.types.GenerationConfig(
            temperature=temp,
            max_output_tokens=100,
        )
        
        model_temp = genai.GenerativeModel(
            MODEL_ID,
            generation_config=generation_config
        )
        
        response = model_temp.generate_content(question)
        print(f"Response: {response.text}\n")
    
    print("⚙️ NOTICE: Higher temperature = more creative/varied responses! ⚙️\n")


# =============================================================================
# STEP 5: STREAMLIT WEB INTERFACE
# =============================================================================

def step_5_streamlit_interface():
    """
    STEP 5: Create web interface with Streamlit
    
    What we're learning:
    - How to build interactive web apps
    - How to manage UI state
    - How to create user-friendly interfaces
    """
    try:
        import streamlit as st
    except ImportError:
        print("\n❌ Streamlit not installed!")
        print("Install it with: pip install streamlit")
        return
    
    st.set_page_config(
        page_title="WCC Info Bot",
        page_icon="🌟",
        layout="centered"
    )
    
    st.title("🌟 WCC Info Bot")
    st.markdown("### Ask me anything about Women Coding Community!")
    
    # Sidebar with parameter controls
    st.sidebar.header("🎛️ Model Settings")
    temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.sidebar.slider("Max Tokens", 50, 500, 200, 50)
    top_p = st.sidebar.slider("Top-p", 0.1, 1.0, 0.9, 0.1)
    
    # Initialize session state for conversation history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Hello! I'm your WCC Info Bot. Ask me anything about the Women Coding Community! 🚀"
        })
    
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to know about WCC?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Configure model with user settings
                generation_config = genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    top_p=top_p
                )
                
                model_ui = genai.GenerativeModel(
                    MODEL_ID,
                    generation_config=generation_config,
                    system_instruction=WCC_SYSTEM_PROMPT
                )
                
                # Create conversation context
                context = "\n".join([
                    f"{msg['role']}: {msg['content']}" 
                    for msg in st.session_state.messages[-5:]  # Last 5 messages
                ])
                
                full_prompt = f"Conversation context:\n{context}\n\nUser: {prompt}"
                response = model_ui.generate_content(full_prompt)
                
                st.markdown(response.text)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    
    # Display current settings
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Current Settings:**")
    st.sidebar.write(f"🌡️ Temperature: {temperature}")
    st.sidebar.write(f"📝 Max Tokens: {max_tokens}")
    st.sidebar.write(f"🎯 Top-p: {top_p}")
    
    # Usage instructions
    with st.expander("💡 How to use this bot"):
        st.markdown('''
        **Try asking:**
        - What is WCC?
        - How can I join the community?
        - What events do you have?
        - I'm new to coding, can you help?
        - How can I volunteer or mentor?
        
        **Experiment with settings:**
        - 🌡️ **Temperature**: Higher = more creative responses
        - 📝 **Max Tokens**: Longer responses
        - 🎯 **Top-p**: Lower = more focused responses
        ''')


# =============================================================================
# MAIN: UNCOMMENT STEPS TO RUN
# =============================================================================

if __name__ == "__main__":
    # UNCOMMENT EACH STEP TO RUN IT
    # Each step builds on the previous one, showing clear code differences!
    
    # Step 1: Basic API integration with Gemini
    step_1_basic_api_call()
    
    # Step 2: AI personality with system prompts
    # step_2_add_personality()
    
    # Step 3: Conversation memory management
    # step_3_conversation_memory()
    
    # Step 4: Model parameter experimentation
    # step_4_model_parameters()
    
    # Step 5: Web interface with Streamlit
    # step_5_streamlit_interface()  # Run with: streamlit run wcc_demo.py
