import streamlit as st
from career_coach_bot import CareerCoachWithMemory

st.set_page_config(page_title="Coachly", layout="wide")

st.title("🎯 Coachly")
st.markdown("Your AI career mentor from Women Coding Community")

if "coach" not in st.session_state:
    st.session_state.coach = CareerCoachWithMemory(user_id="streamlit_user")

with st.sidebar:
    st.header("Your Profile")
    experience = st.selectbox(
        "Experience Level",
        ["Entry-level", "Mid-career", "Senior", "Career changer"]
    )
    target_role = st.text_input("Target Role (optional)")
    goal = st.text_area("Career Goal (optional)")

    if st.button("Update Profile"):
        st.session_state.coach.user_profile = {
            "experience_level": experience,
            "target_role": target_role,
            "goals": goal
        }
        st.success("Profile updated!")

st.subheader("Chat with Coachly")

for msg in st.session_state.coach.conversation_history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

user_input = st.chat_input("Ask your career coach a question...")

if user_input:
    st.chat_message("user").write(user_input)
    response = st.session_state.coach.chat(user_input)
    st.chat_message("assistant").write(response)
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("📚 Resources")
st.sidebar.markdown("""
- [LinkedIn Learning](https://linkedin.com/learning)
- [Coursera](https://coursera.org)
- [LeetCode](https://leetcode.com)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
""")