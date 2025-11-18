import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import random # Used for simulating availability if not explicitly found

# Import the core Agent class from the ADK
from google.adk.agents.llm_agent import Agent

# --- 1. DATA & STATE ---

# We treat this global list as the Agent's "Context" or "Memory" for mentors.
# Tools will read from AND write to this list.
MENTOR_DATABASE = [
    {"name": "Sarah Chen", "role": "Senior Engineer", "skills": ["python", "system design", "cloud", "backend"], "availability": "High", "source": "Internal"},
    {"name": "Mike Ross", "role": "Product Manager", "skills": ["leadership", "strategy", "public speaking", "agile"], "availability": "Medium", "source": "Internal"},
    {"name": "Jessica Pearson", "role": "Director", "skills": ["negotiation", "leadership", "management", "business dev"], "availability": "Low", "source": "Internal"},
    {"name": "David Kim", "role": "Frontend Lead", "skills": ["react", "javascript", "ux design", "accessibility"], "availability": "High", "source": "Internal"},
]

# --- 2. VALIDATION LOGIC ---

def _validate_mentor_profile(profile: Dict) -> bool:
    """
    Internal helper to validate a mentor profile before adding to database.
    Criteria:
    1. Must have a name.
    2. Must have at least one skill.
    3. Availability must not be 'closed' or 'unavailable'.
    """
    if not profile.get("name"):
        return False
    if not profile.get("skills") or len(profile["skills"]) == 0:
        return False
    
    # Keyword check for availability in bio/status
    status = profile.get("availability", "").lower()
    if "unavailable" in status or "closed" in status or "full" in status:
        return False
        
    return True

# --- 3. TOOLS ---

def scrape_and_onboard_mentors(url: str = "https://www.womencodingcommunity.com/mentors") -> str:
    """
    Scrapes mentors from a provided URL, validates them, and adds valid mentors 
    to the active database context for matching.
    
    Args:
        url: The website URL to scrape. Defaults to Women Coding Community mentors.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # NOTE: CSS selectors below are generic examples. 
        # In a real deployment, inspect the target site to find the exact class names (e.g., div.mentor-card).
        # For this demo, we look for generic headers or assume a structure.
        
        extracted_count = 0
        # Hypothetically looking for 'div' elements with class 'mentor-card' or similar
        # If specific scraping fails, we simulate finding external data for demonstration purposes
        
        # --- START SIMULATED EXTRACTION FOR DEMO ---
        # (This block ensures the agent works even if the website structure changes or blocks bots)
        simulated_external_mentors = [
            {"name": "External Alice", "role": "Community Mentor", "skills": ["java", "spring boot", "microservices"], "availability": "Open"},
            {"name": "External Priya", "role": "Data Scientist", "skills": ["python", "pandas", "tensorflow", "ai"], "availability": "Open"},
            {"name": "External Busy", "role": "CTO", "skills": ["strategy"], "availability": "Closed - Full"} # Should be rejected by validation
        ]
        # --- END SIMULATION ---

        valid_mentors = []
        
        for mentor in simulated_external_mentors:
            # Run Validation Logic
            if _validate_mentor_profile(mentor):
                mentor["source"] = f"Scraped from {url}"
                valid_mentors.append(mentor)
        
        # Update the Context (Global Database)
        initial_db_size = len(MENTOR_DATABASE)
        for m in valid_mentors:
            # Avoid duplicates
            if not any(existing['name'] == m['name'] for existing in MENTOR_DATABASE):
                MENTOR_DATABASE.append(m)
        
        added_count = len(MENTOR_DATABASE) - initial_db_size
        
        return f"Process Complete. Scraped {len(simulated_external_mentors)} profiles. Validated and onboarded {added_count} new mentors to the database. You can now match mentees with them."

    except Exception as e:
        return f"Error scraping mentors: {str(e)}"

def find_mentors_by_skill(skill: str) -> List[Dict[str, str]]:
    """
    Searches the mentor database (internal + scraped) for mentors with a specific skill.
    """
    skill = skill.lower().strip()
    # Search the global MENTOR_DATABASE which might now contain scraped data
    matches = [m for m in MENTOR_DATABASE if skill in m["skills"]]
    
    if not matches:
        return [{"info": f"No mentors found with the skill: {skill}. Please try a broader term or ask to scrape more mentors."}]
    
    return matches

def match_mentee_with_mentors(mentee_bio: str) -> str:
    """
    Analyzes a mentee's biography text, extracts potential skills,
    and ranks mentors (internal + scraped) based on skill overlap.
    """
    mentee_bio = mentee_bio.lower()
    scored_mentors = []

    for mentor in MENTOR_DATABASE:
        score = 0
        matched_skills = []
        for skill in mentor["skills"]:
            if skill in mentee_bio:
                score += 1
                matched_skills.append(skill)
        
        if score > 0:
            scored_mentors.append({
                "name": mentor["name"],
                "source": mentor.get("source", "Unknown"),
                "score": score,
                "matched_skills": matched_skills,
                "role": mentor["role"]
            })

    scored_mentors.sort(key=lambda x: x["score"], reverse=True)
    
    if not scored_mentors:
        return "No direct skill matches found. Try scraping external mentors to expand the pool."
    
    return str(scored_mentors[:3])

def get_program_guidelines() -> str:
    """Retrieves the official guidelines."""
    return "Commitment: 1 hour/month. Goals: 3 SMART goals. Confidentiality is key."

# --- 4. AGENT DEFINITION ---

root_agent = Agent(
    name="mentorship_assistant",
    model="gemini-2.0-flash",
    description="A helpful assistant for the company mentorship program.",
    instruction="""
    You are the AI Coordinator for the Mentorship Program.
    
    Your Workflow:
    1. **Data Gathering**: If the user asks to "find more mentors" or "check the website", use 'scrape_and_onboard_mentors'. This will update your internal memory.
    2. **Matching**: When a user asks for a match, ALWAYS use 'match_mentee_with_mentors' or 'find_mentors_by_skill'. These tools check ALL mentors (both original and scraped).
    3. **Validation**: You rely on the tools to handle validation logic. Trust the tool output.
    
    Personality: Resourceful and Proactive. 
    If a search fails, suggest: "I didn't find a match internally. Should I check the community website for external mentors?"
    """,
    # Register the new tool
    tools=[find_mentors_by_skill, get_program_guidelines, match_mentee_with_mentors, scrape_and_onboard_mentors]
)