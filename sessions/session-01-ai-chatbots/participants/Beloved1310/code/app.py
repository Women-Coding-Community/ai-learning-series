import streamlit as st
import logging
from chatbot import SimpleBot, system_prompt, faqs

# -----------------------------------
# Configure Logging
# -----------------------------------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("🚀 WCC Info Bot app started.")

st.set_page_config(page_title="WCC Info Bot", page_icon="🤖")

st.title("🤖 WCC Info Bot")
st.markdown("Ask me anything about Women Coding Community!")

# -----------------------------------
# Initialize bot once
# -----------------------------------
if "bot" not in st.session_state:
    try:
        st.session_state.bot = SimpleBot(system_prompt, faqs)
        logging.info("Chatbot initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize chatbot: {e}")
        st.error("⚠️ Failed to initialize the chatbot.")
        st.stop()

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------------
# Chat Input
# -----------------------------------
if user_input := st.chat_input("Ask me about WCC..."):

    logging.info(f"User asked: {user_input}")

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate bot response safely
    try:
        response = st.session_state.bot.chat(user_input)
        logging.info(f"Bot response: {response}")
    except Exception as e:
        logging.error(f"Error generating bot response: {e}")
        response = "⚠️ Sorry, something went wrong while processing your request."

    # Save bot message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.markdown(response)
