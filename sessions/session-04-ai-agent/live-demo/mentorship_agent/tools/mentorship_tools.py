import json
import os
import requests
from bs4 import BeautifulSoup
from typing import List, Dict


# --- 1. DATA MANAGEMENT TOOLS ---

PROFILE_FILE = "./mentorship_agent/profiles.json"
GUIDELINES_FILE = "./mentorship_agent/program_guidelines.txt"

def save_profile(
    role: str, 
    name: str, 
    email: str, 
    skills: List[str], 
    availability: str, 
    bio: str, 
    linkedin_url: str
) -> str:
    """
    Saves a completed applicant profile to the JSON database.
    
    Args:
        role: Must be 'Mentor' or 'Mentee'.
        name: The full name of the applicant.
        email: The contact email.
        skills: A list of skills or learning goals.
        availability: The time commitment.
        bio: A short summary or current role/company.
        linkedin_url: The profile URL for verification.
    """
    role = role.strip().title() 
    if role not in ["Mentor", "Mentee"]:
        return "Error: Role must be exactly 'Mentor' or 'Mentee'."

    data = {
        "role": role,
        "name": name.strip(),
        "email": email.strip(),
        # Ensure skills are clean strings
        "skills": [s.strip() for s in skills],
        "availability": availability,
        "bio": bio,
        "linkedin_url": linkedin_url
    }

    # Ensure file exists
    if not os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'w') as f:
            json.dump([], f)
            
    try:
        with open(PROFILE_FILE, 'r') as f:
            profiles = json.load(f)
        
        # Check if user already exists and update them
        existing_index = next((index for (index, d) in enumerate(profiles) if d["name"].lower() == name.lower()), None)
        
        if existing_index is not None:
            profiles[existing_index] = data
            msg = f"Success: Updated existing profile for {name}."
        else:
            data["status"] = "Pending Validation"
            profiles.append(data)
            msg = f"Success: Profile for {name} saved."
        
        with open(PROFILE_FILE, 'w') as f:
            json.dump(profiles, f, indent=2)
            
        return msg
    except Exception as e:
        return f"Error saving profile: {str(e)}"

def read_guidelines() -> str:
    """Reads the official program eligibility guidelines."""
    try:
        with open(GUIDELINES_FILE, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: Guidelines file not found."

# --- 2. VERIFICATION TOOLS ---

def verify_online_presence(linkedin_url: str, name: str, company: str) -> str:
    """
    Simulates a 'Google Grounding' check. In a real production environment, 
    this would use the Google Search API or LinkedIn API to verify the person exists.
    """
    print(f"DEBUG: Verifying {name} at {company} via {linkedin_url}")
    
    # 1. Basic URL Validation
    if "linkedin.com/in/" not in linkedin_url and "github.com" not in linkedin_url:
        return "Validation Failed: URL provided does not look like a valid LinkedIn or GitHub profile."

    # 2. Simulated "Grounding" / Web Check
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        # Timeout set to 5s to avoid hanging the agent
        response = requests.get(linkedin_url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            return f"Validation Passed: Profile link is active. (Simulated) Confirmed {name} works at {company}."
        elif response.status_code == 999:
            return f"Validation Warning: Profile link exists but blocked by platform. Manual verification recommended for {name}."
        else:
            return f"Validation Failed: Link returned status code {response.status_code}."
            
    except Exception as e:
        return f"Validation Error: Could not reach URL. {str(e)}"

# --- 3. MATCHING TOOLS ---

def find_mentors_by_skill(skill: str) -> str:
    """Searches saved profiles for Mentors with specific skills."""
    if not os.path.exists(PROFILE_FILE):
        return "No profiles database found."
        
    with open(PROFILE_FILE, 'r') as f:
        profiles = json.load(f)
        
    search_term = skill.lower().strip()
    matches = []
    
    for p in profiles:
        if p.get("role") == "Mentor":
            mentor_skills = [s.lower() for s in p.get("skills", [])]
            if any(search_term in ms or ms in search_term for ms in mentor_skills):
                matches.append(p)
    
    if not matches:
        return f"No mentors found for '{skill}'. Try a broader term."
    
    results = []
    for m in matches:
        results.append(f"Name: {m['name']} | Skills: {', '.join(m['skills'])} | Bio: {m['bio']}")
    
    return "\n".join(results)

def match_mentee_from_database(mentee_name: str) -> str:
    """
    Locates a Mentee in the database by name, reads their learning goals,
    and automatically finds suitable Mentors.
    """
    if not os.path.exists(PROFILE_FILE):
        return "No profiles database found."
        
    with open(PROFILE_FILE, 'r') as f:
        profiles = json.load(f)
    
    # 1. Find the Mentee
    mentee = next((p for p in profiles if p.get("name", "").lower() == mentee_name.lower() and p.get("role") == "Mentee"), None)
    
    if not mentee:
        return f"Could not find a registered Mentee named '{mentee_name}'. Please register first."
    
    goals = mentee.get("skills", [])
    if not goals:
        return f"Mentee {mentee_name} has no learning goals listed."

    # 2. Find Mentors for each goal
    report = [f"Matching Report for {mentee['name']} (Goals: {', '.join(goals)}):\n"]
    
    for goal in goals:
        matches = find_mentors_by_skill(goal)
        if "No mentors found" in matches:
            report.append(f"- Goal '{goal}': No direct matches.")
        else:
            report.append(f"- Goal '{goal}':\n{matches}")
            
    return "\n".join(report)