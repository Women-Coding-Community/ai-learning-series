#!/usr/bin/env python3
"""
WCC AI Learning Series - Session 1 Live Demo
Progressive Chatbot Building - Uncomment sections step by step!

INSTRUCTIONS FOR LIVE DEMO:
1. Start with SECTION 1 (already active)
2. To activate SECTION 2: Delete the triple quotes
3. To activate SECTION 3: Delete the triple quotes
4. To activate SECTION 4: Delete the triple quotes
5. To activate SECTION 5: Delete the triple quotes

Demo Flow:
1. Basic API call (START HERE - ACTIVE)
2. Add personality with system prompt (SECTION 2)
3. Add conversation memory (SECTION 3)
4. Explore model parameters (SECTION 4)
5. Create web interface (SECTION 5)
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

# Set up Gemini API from environment
_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if _api_key:
    genai.configure(api_key=_api_key)
    
# Define WCC knowledge and personality
wcc_system_prompt = '''You are a helpful and enthusiastic assistant for the Women Coding Community (WCC).

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
# SECTION 5: STREAMLIT WEB INTERFACE
# =============================================================================


import streamlit as st

print("STEP 5: Creating Web Interface with Streamlit")
print("-" * 45)

# Streamlit Web App
def create_streamlit_app():
    '''
    To run this section:
    1. Delete the triple quotes around this entire section
    2. Save this file as 'wcc_demo.py'
    3. Run: streamlit run wcc_demo.py
    '''
    
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
                    system_instruction=wcc_system_prompt
                )
                
                # Create conversation context
                context = "\\n".join([
                    f"{msg['role']}: {msg['content']}" 
                    for msg in st.session_state.messages[-5:]  # Last 5 messages
                ])
                
                full_prompt = f"Conversation context:\\n{context}\\n\\nUser: {prompt}"
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

# Instructions for running Streamlit
print('''
🌐 TO CREATE WEB INTERFACE:
========================
1. Delete the triple quotes around SECTION 5 above
2. Save this file as 'wcc_demo.py'  
3. Install Streamlit: pip install streamlit
4. Run: streamlit run wcc_demo.py
5. Your browser will open with the web app!

📱 FEATURES OF THE WEB APP:
- Interactive chat interface
- Adjustable model parameters
- Conversation history
- Mobile-friendly design
''')

# Only run Streamlit if this section is uncommented and file is run with streamlit
if __name__ == "__main__" and "streamlit" in os.environ.get("_", ""):
    create_streamlit_app()


# =============================================================================
# DEMO COMPLETION
# =============================================================================

print("🎓 SESSION 1 DEMO COMPLETE!")
print("=" * 30)
print("""
WHAT WE BUILT TODAY:
✅ Basic API integration with Gemini
✅ AI personality with system prompts  
✅ Conversation memory management
✅ Model parameter experimentation
✅ Web interface with Streamlit

NEXT STEPS:
1. Uncomment sections one by one as you follow along
2. Experiment with different prompts and parameters
3. Customize the WCC knowledge base
4. Deploy your bot and share with the community!

HOMEWORK:
- Enhance your bot with more WCC information
- Try different model parameters
- Add your bot to GitHub
- Come to Session 2 with questions!

Happy coding! 💪🌟
""")
