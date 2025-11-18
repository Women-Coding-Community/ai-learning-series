import streamlit as st
import pandas as pd
from agent import root_agent, MENTOR_DATABASE

# --- NEW IMPORTS FOR RUNTIME ---
from google.adk.runners import InMemoryRunner
from google.genai import types

# Page Config
st.set_page_config(page_title="Mentorship Coordinator AI", layout="wide")

st.title("🚀 Future Leaders: Mentorship Coordinator")

# --- INITIALIZE RUNNER (The missing piece) ---
# We use @st.cache_resource to ensure we don't recreate the runner 
# (and wipe the session memory) every time you click a button.
@st.cache_resource
def get_runner():
    return InMemoryRunner(agent=root_agent)

runner = get_runner()
# We need a persistent session ID for the conversation history
if "session_id" not in st.session_state:
    # Create a session once and store the ID
    import uuid
    st.session_state.session_id = str(uuid.uuid4())

# --- SIDEBAR: LIVE DATA VIEW ---
with st.sidebar:
    st.header("📂 Mentor Database")
    st.caption("Live view of the agent's memory")
    
    if MENTOR_DATABASE:
        df = pd.DataFrame(MENTOR_DATABASE)
        cols = ["name", "role", "availability", "source", "skills"]
        # Filter columns safely
        display_cols = [c for c in cols if c in df.columns]
        st.dataframe(df[display_cols], hide_index=True)
        st.metric("Total Mentors", len(MENTOR_DATABASE))
    else:
        st.info("Database is empty.")

# --- MAIN CHAT INTERFACE ---
st.subheader("💬 Chat with the Coordinator Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex: 'Find a mentor for Python' or 'Scrape mentors from the community site'"):
    # 1. Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Get Agent Response via RUNNER
    with st.chat_message("assistant"):
        with st.spinner("Agent is working..."):
            try:
                # Prepare the input content object required by ADK
                user_content = types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)]
                )
                
                # The runner returns a stream of events (thoughts, tool calls, answers)
                # We loop through them to find the final text answer.
                response_text = ""
                
                # 'run' is the correct method on the Runner, not the Agent
                for event in runner.run(
                    user_id="streamlit_user",
                    session_id=st.session_state.session_id,
                    new_message=user_content
                ):
                    # Check if this event is a text response from the model
                    if event.content and event.content.parts:
                        part = event.content.parts[0]
                        if part.text:
                            response_text += part.text
                            
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
                # Force refresh to update sidebar if tools modified the database
                st.rerun()
                
            except Exception as e:
                error_msg = f"⚠️ Runtime Error: {str(e)}"
                st.error(error_msg)