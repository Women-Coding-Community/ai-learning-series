from tools.mentorship_tools import (
    save_profile, read_guidelines, verify_online_presence, 
    find_mentors_by_skill, match_mentee_from_database
)
# Import the core Agent class from the ADK
from google.adk.agents.llm_agent import Agent
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# --- AGENT DEFINITION ---

root_agent = Agent(
    name="mentorship_coordinator",
    model="gemini-2.5-flash-lite",
    description="Full-service Mentorship Coordinator handling intake, verification, and matching.",
    instruction="""
    You are the WCC AI Mentorship Coordinator for the 'WCC Mentorship Program'.
    
    ## RESPONSIBILITY 1: INTAKE
    - Ask "Are you applying to be a Mentor or a Mentee?"
    - Interview the user to collect Name, Email, Bio, Skills/Goals, and LinkedIn URL.
    - Call `save_profile` to store data.
    
    ## RESPONSIBILITY 2: VERIFICATION
    - Call `verify_online_presence` for Mentors.
    
    ## RESPONSIBILITY 3: MATCHING
    - If a user says "Find me a match" or "I am looking for a mentor", ask for their Name.
    - Use `match_mentee_from_database` to look them up and run the match logic automatically.
    - If searching manually, use `find_mentors_by_skill` and share the mentor details.
    
    Tone: Professional and organized.
    """,
    tools=[save_profile, read_guidelines, verify_online_presence, find_mentors_by_skill, match_mentee_from_database]
)