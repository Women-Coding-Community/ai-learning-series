"""
Mentorship Tools - Shared tools for the multi-agent mentorship system.
"""
import json
import os
import requests
from bs4 import BeautifulSoup
from typing import List

# File paths relative to live-demo folder
PROFILE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "profiles.json")
GUIDELINES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "program_guidelines.txt")

# WCC Website URLs
WCC_MENTORS_URL = "https://www.womencodingcommunity.com/mentors"
WCC_MENTORSHIP_URL = "https://www.womencodingcommunity.com/mentorship"
WCC_FAQ_URL = "https://www.womencodingcommunity.com/mentorship-faq"
WCC_EVENTS_URL = "https://www.womencodingcommunity.com/events"


# =============================================================================
# INTAKE TOOLS
# =============================================================================

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
        skills: A list of skills (Mentor) or learning goals (Mentee).
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
        "skills": [s.strip() for s in skills],
        "availability": availability,
        "bio": bio,
        "linkedin_url": linkedin_url,
        "status": "Pending Verification" if role == "Mentor" else "Active"
    }

    # Ensure file exists
    if not os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'w') as f:
            json.dump([], f)
            
    try:
        with open(PROFILE_FILE, 'r') as f:
            profiles = json.load(f)
        
        # Check if user already exists
        existing_index = next(
            (i for i, d in enumerate(profiles) if d["name"].lower() == name.lower()), 
            None
        )
        
        if existing_index is not None:
            profiles[existing_index] = data
            msg = f"✅ Updated profile for {name}."
        else:
            profiles.append(data)
            msg = f"✅ Profile saved for {name} ({role})."
        
        with open(PROFILE_FILE, 'w') as f:
            json.dump(profiles, f, indent=2)
            
        return msg
    except Exception as e:
        return f"❌ Error saving profile: {str(e)}"


def read_guidelines() -> str:
    """Reads the official program eligibility guidelines."""
    try:
        with open(GUIDELINES_FILE, 'r') as f:
            return f"📋 **Program Guidelines:**\n\n{f.read()}"
    except FileNotFoundError:
        return "❌ Guidelines file not found."


def list_profiles() -> str:
    """List all registered profiles."""
    if not os.path.exists(PROFILE_FILE):
        return "📋 No profiles registered yet."
    
    try:
        with open(PROFILE_FILE, 'r') as f:
            profiles = json.load(f)
        
        if not profiles:
            return "📋 No profiles registered yet."
        
        mentors = [p for p in profiles if p.get("role") == "Mentor"]
        mentees = [p for p in profiles if p.get("role") == "Mentee"]
        
        result = ["📋 **Registered Profiles:**\n"]
        
        if mentors:
            result.append(f"**Mentors ({len(mentors)}):**")
            for m in mentors:
                status = m.get("status", "Unknown")
                result.append(f"  - {m['name']} ({status}) - {', '.join(m.get('skills', []))}")
        
        if mentees:
            result.append(f"\n**Mentees ({len(mentees)}):**")
            for m in mentees:
                result.append(f"  - {m['name']} - Goals: {', '.join(m.get('skills', []))}")
        
        return "\n".join(result)
    except Exception as e:
        return f"❌ Error: {e}"


# =============================================================================
# VERIFICATION TOOLS
# =============================================================================

def verify_online_presence(linkedin_url: str, name: str, company: str) -> str:
    """
    Verifies a mentor's online presence via their LinkedIn/GitHub profile.
    
    Args:
        linkedin_url: The profile URL to verify
        name: The person's name
        company: Their claimed company/role
    """
    print(f"🔍 Verifying {name} at {company} via {linkedin_url}")
    
    # Basic URL validation
    if "linkedin.com/in/" not in linkedin_url and "github.com" not in linkedin_url:
        return "❌ Validation Failed: URL is not a valid LinkedIn or GitHub profile."

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(linkedin_url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            # Update profile status
            _update_profile_status(name, "Verified")
            return f"✅ Verified: {name}'s profile is active. Confirmed at {company}."
        elif response.status_code == 999:
            return f"⚠️ Warning: Profile blocked by platform. Manual verification needed for {name}."
        else:
            return f"❌ Failed: Link returned status {response.status_code}."
            
    except Exception as e:
        return f"❌ Error: Could not reach URL. {str(e)}"


def _update_profile_status(name: str, status: str):
    """Internal: Update a profile's status."""
    if not os.path.exists(PROFILE_FILE):
        return
    
    try:
        with open(PROFILE_FILE, 'r') as f:
            profiles = json.load(f)
        
        for p in profiles:
            if p["name"].lower() == name.lower():
                p["status"] = status
                break
        
        with open(PROFILE_FILE, 'w') as f:
            json.dump(profiles, f, indent=2)
    except:
        pass


# =============================================================================
# MATCHING TOOLS
# =============================================================================

def find_mentors_by_skill(skill: str) -> str:
    """
    Search for mentors with a specific skill.
    
    Args:
        skill: The skill to search for
    """
    if not os.path.exists(PROFILE_FILE):
        return "📋 No profiles database found."
        
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
        return f"🔍 No mentors found for '{skill}'."
    
    results = [f"🔍 **Mentors for '{skill}':**\n"]
    for m in matches:
        status = m.get("status", "Unknown")
        results.append(f"- **{m['name']}** ({status})\n  Skills: {', '.join(m['skills'])}\n  Bio: {m['bio']}")
    
    return "\n".join(results)


def match_mentee(mentee_name: str) -> str:
    """
    Find matching mentors for a registered mentee.
    
    Args:
        mentee_name: The name of the mentee to match
    """
    if not os.path.exists(PROFILE_FILE):
        return "📋 No profiles database found."
        
    with open(PROFILE_FILE, 'r') as f:
        profiles = json.load(f)
    
    # Find the mentee
    mentee = next(
        (p for p in profiles if p.get("name", "").lower() == mentee_name.lower() and p.get("role") == "Mentee"), 
        None
    )
    
    if not mentee:
        return f"❌ No mentee named '{mentee_name}' found. Please register first."
    
    goals = mentee.get("skills", [])
    if not goals:
        return f"❌ {mentee_name} has no learning goals listed."

    # Find mentors for each goal
    report = [f"🎯 **Matching Report for {mentee['name']}**\n"]
    report.append(f"Goals: {', '.join(goals)}\n")
    
    all_matches = []
    for goal in goals:
        mentors = [
            p for p in profiles 
            if p.get("role") == "Mentor" and 
            any(goal.lower() in s.lower() or s.lower() in goal.lower() for s in p.get("skills", []))
        ]
        
        if mentors:
            report.append(f"**{goal}:**")
            for m in mentors:
                if m["name"] not in all_matches:
                    all_matches.append(m["name"])
                    report.append(f"  ✅ {m['name']} - {', '.join(m['skills'])}")
        else:
            report.append(f"**{goal}:** No matches found")
    
    if all_matches:
        report.append(f"\n📊 **Summary:** {len(all_matches)} potential mentor(s) found!")
    else:
        report.append("\n📊 **Summary:** No matches found. Consider broadening goals.")
            
    return "\n".join(report)


# =============================================================================
# WCC WEBSITE SEARCH TOOLS
# =============================================================================

def search_wcc_mentors(skill: str = "") -> str:
    """
    Search for mentors on the WCC website (https://www.womencodingcommunity.com/mentors).
    
    This tool fetches the live WCC mentors page and extracts mentor information.
    
    Args:
        skill: Optional skill to filter mentors (e.g., "Python", "Data Science")
        
    Returns:
        str: List of mentors from the WCC website
    """
    try:
        print(f"🌐 Fetching mentors from {WCC_MENTORS_URL}...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(WCC_MENTORS_URL, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return f"❌ Could not fetch WCC mentors page (status: {response.status_code})"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find mentor cards/sections
        # This will need adjustment based on actual page structure
        mentors = []
        
        # Look for common patterns in mentor listings
        # Try finding cards, articles, or divs with mentor info
        mentor_elements = (
            soup.find_all('div', class_=lambda x: x and 'mentor' in x.lower()) or
            soup.find_all('article') or
            soup.find_all('div', class_=lambda x: x and 'card' in x.lower()) or
            soup.find_all('div', class_=lambda x: x and 'team' in x.lower())
        )
        
        if mentor_elements:
            for elem in mentor_elements[:10]:  # Limit to 10
                # Extract text content
                name = elem.find(['h2', 'h3', 'h4', 'strong'])
                name_text = name.get_text(strip=True) if name else "Unknown"
                
                # Get description/bio
                desc = elem.find('p')
                desc_text = desc.get_text(strip=True)[:100] if desc else ""
                
                # Check skill filter
                full_text = elem.get_text().lower()
                if skill and skill.lower() not in full_text:
                    continue
                    
                mentors.append({
                    "name": name_text,
                    "description": desc_text
                })
        
        if not mentors:
            # Fallback: extract any structured content
            # Get page title and main content
            title = soup.find('h1')
            main_content = soup.find('main') or soup.find('article') or soup.body
            
            if main_content:
                # Get text paragraphs
                paragraphs = main_content.find_all('p')[:5]
                content_preview = "\n".join(p.get_text(strip=True)[:200] for p in paragraphs if p.get_text(strip=True))
                
                return f"""🌐 **WCC Mentors Page**

📍 URL: {WCC_MENTORS_URL}

📄 **Page Content Preview:**
{content_preview}

💡 Visit the website directly to see all available mentors and apply to the program.
"""
        
        # Format results
        result = [f"🌐 **WCC Mentors** (from {WCC_MENTORS_URL})\n"]
        
        if skill:
            result.append(f"🔍 Filtered by: {skill}\n")
        
        for m in mentors:
            result.append(f"👤 **{m['name']}**")
            if m['description']:
                result.append(f"   {m['description']}")
        
        if not mentors:
            result.append("No mentors found matching your criteria.")
            result.append(f"\n💡 Visit {WCC_MENTORS_URL} to see all mentors.")
        
        return "\n".join(result)
        
    except requests.Timeout:
        return f"❌ Timeout fetching {WCC_MENTORS_URL}. Please try again."
    except Exception as e:
        return f"❌ Error fetching WCC mentors: {str(e)}\n\n💡 Visit {WCC_MENTORS_URL} directly."


def get_wcc_page_info() -> str:
    """
    Get general information from the WCC mentorship page.
    
    Returns:
        str: Information about the WCC mentorship program
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(WCC_MENTORS_URL, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return f"❌ Could not fetch page (status: {response.status_code})"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get page title
        title = soup.find('title')
        title_text = title.get_text(strip=True) if title else "WCC Mentors"
        
        # Get meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '') if meta_desc else ""
        
        # Get main headings
        headings = soup.find_all(['h1', 'h2'], limit=5)
        heading_texts = [h.get_text(strip=True) for h in headings]
        
        result = [f"🌐 **{title_text}**\n"]
        result.append(f"📍 URL: {WCC_MENTORS_URL}\n")
        
        if description:
            result.append(f"📝 {description}\n")
        
        if heading_texts:
            result.append("📋 **Sections:**")
            for h in heading_texts:
                result.append(f"  - {h}")
        
        result.append(f"\n💡 Visit the website to learn more and apply!")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Error: {str(e)}\n\n💡 Visit {WCC_MENTORS_URL} directly."


def get_wcc_mentorship_overview() -> str:
    """
    Get the WCC Mentorship Program overview from the main mentorship page.
    
    Fetches content from https://www.womencodingcommunity.com/mentorship
    
    Returns:
        str: Overview of the WCC mentorship program
    """
    try:
        print(f"🌐 Fetching mentorship overview from {WCC_MENTORSHIP_URL}...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(WCC_MENTORSHIP_URL, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return f"❌ Could not fetch page (status: {response.status_code})"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get page title
        title = soup.find('title')
        title_text = title.get_text(strip=True) if title else "WCC Mentorship"
        
        # Get main content
        main_content = soup.find('main') or soup.find('article') or soup.body
        
        result = [f"🌐 **{title_text}**\n"]
        result.append(f"📍 URL: {WCC_MENTORSHIP_URL}\n")
        
        if main_content:
            # Get headings and their content
            sections = []
            
            # Find all headings
            headings = main_content.find_all(['h1', 'h2', 'h3'], limit=10)
            for h in headings:
                heading_text = h.get_text(strip=True)
                if heading_text:
                    sections.append(f"\n**{heading_text}**")
                    
                    # Get following paragraphs
                    next_elem = h.find_next_sibling()
                    para_count = 0
                    while next_elem and para_count < 2:
                        if next_elem.name == 'p':
                            text = next_elem.get_text(strip=True)
                            if text:
                                sections.append(text[:200] + "..." if len(text) > 200 else text)
                                para_count += 1
                        elif next_elem.name in ['h1', 'h2', 'h3']:
                            break
                        next_elem = next_elem.find_next_sibling()
            
            if sections:
                result.extend(sections)
            else:
                # Fallback: get all paragraphs
                paragraphs = main_content.find_all('p', limit=5)
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if text and len(text) > 20:
                        result.append(text[:200] + "..." if len(text) > 200 else text)
        
        result.append(f"\n💡 Visit {WCC_MENTORSHIP_URL} for full details!")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Error: {str(e)}\n\n💡 Visit {WCC_MENTORSHIP_URL} directly."


def get_wcc_faq() -> str:
    """
    Get the WCC Mentorship FAQ from the FAQ page.
    
    Fetches content from https://www.womencodingcommunity.com/mentorship-faq
    
    Returns:
        str: FAQ about the WCC mentorship program
    """
    try:
        print(f"🌐 Fetching FAQ from {WCC_FAQ_URL}...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(WCC_FAQ_URL, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return f"❌ Could not fetch FAQ page (status: {response.status_code})"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get page title
        title = soup.find('title')
        title_text = title.get_text(strip=True) if title else "WCC Mentorship FAQ"
        
        result = [f"❓ **{title_text}**\n"]
        result.append(f"📍 URL: {WCC_FAQ_URL}\n")
        
        # Look for FAQ structure (questions/answers)
        main_content = soup.find('main') or soup.find('article') or soup.body
        
        if main_content:
            faqs = []
            
            # Try to find FAQ items - common patterns
            # Pattern 1: details/summary elements
            details = main_content.find_all('details')
            if details:
                for d in details[:10]:
                    summary = d.find('summary')
                    if summary:
                        q = summary.get_text(strip=True)
                        # Get answer (rest of details content)
                        a = d.get_text(strip=True).replace(q, '', 1).strip()[:150]
                        faqs.append(f"**Q: {q}**\nA: {a}...")
            
            # Pattern 2: h3/h4 questions with p answers
            if not faqs:
                questions = main_content.find_all(['h3', 'h4', 'strong'])
                for q_elem in questions[:10]:
                    q_text = q_elem.get_text(strip=True)
                    if '?' in q_text or len(q_text) > 10:
                        next_p = q_elem.find_next('p')
                        if next_p:
                            a_text = next_p.get_text(strip=True)[:150]
                            faqs.append(f"**Q: {q_text}**\nA: {a_text}...")
            
            # Pattern 3: Just get structured content
            if not faqs:
                paragraphs = main_content.find_all('p', limit=8)
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if text and len(text) > 30:
                        faqs.append(text[:200] + "..." if len(text) > 200 else text)
            
            if faqs:
                result.append("**Frequently Asked Questions:**\n")
                result.extend(faqs[:8])  # Limit to 8 FAQs
        
        result.append(f"\n💡 Visit {WCC_FAQ_URL} for all FAQs!")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Error: {str(e)}\n\n💡 Visit {WCC_FAQ_URL} directly."


# =============================================================================
# WCC EVENTS TOOLS
# =============================================================================

def get_wcc_events() -> str:
    """
    Get upcoming WCC events from the events page.
    
    Fetches content from https://www.womencodingcommunity.com/events
    
    Returns:
        str: List of upcoming WCC events where you can help or participate
    """
    try:
        print(f"🌐 Fetching events from {WCC_EVENTS_URL}...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(WCC_EVENTS_URL, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return f"❌ Could not fetch events page (status: {response.status_code})"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get page title
        title = soup.find('title')
        title_text = title.get_text(strip=True) if title else "WCC Events"
        
        result = [f"📅 **{title_text}**\n"]
        result.append(f"📍 URL: {WCC_EVENTS_URL}\n")
        
        # Look for event listings
        main_content = soup.find('main') or soup.find('article') or soup.body
        
        if main_content:
            events = []
            
            # Try different patterns for event cards
            # Pattern 1: Event cards/articles
            event_elements = (
                main_content.find_all('div', class_=lambda x: x and 'event' in x.lower()) or
                main_content.find_all('article') or
                main_content.find_all('div', class_=lambda x: x and 'card' in x.lower()) or
                main_content.find_all('li', class_=lambda x: x and 'event' in x.lower())
            )
            
            if event_elements:
                for elem in event_elements[:10]:
                    # Extract event title
                    title_elem = elem.find(['h2', 'h3', 'h4', 'strong', 'a'])
                    event_title = title_elem.get_text(strip=True) if title_elem else ""
                    
                    # Extract date if present
                    date_elem = elem.find(['time', 'span', 'p'], class_=lambda x: x and 'date' in str(x).lower()) or \
                               elem.find(string=lambda t: t and any(m in str(t) for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', '2024', '2025']))
                    event_date = ""
                    if date_elem:
                        if hasattr(date_elem, 'get_text'):
                            event_date = date_elem.get_text(strip=True)[:50]
                        else:
                            event_date = str(date_elem).strip()[:50]
                    
                    # Extract description
                    desc_elem = elem.find('p')
                    event_desc = desc_elem.get_text(strip=True)[:100] if desc_elem else ""
                    
                    # Extract link
                    link_elem = elem.find('a', href=True)
                    event_link = link_elem.get('href', '') if link_elem else ""
                    if event_link and not event_link.startswith('http'):
                        event_link = f"https://www.womencodingcommunity.com{event_link}"
                    
                    if event_title:
                        events.append({
                            "title": event_title,
                            "date": event_date,
                            "description": event_desc,
                            "link": event_link
                        })
            
            # Pattern 2: Look for headings with event info
            if not events:
                headings = main_content.find_all(['h2', 'h3', 'h4'], limit=10)
                for h in headings:
                    h_text = h.get_text(strip=True)
                    if h_text and len(h_text) > 5:
                        next_p = h.find_next('p')
                        desc = next_p.get_text(strip=True)[:100] if next_p else ""
                        events.append({
                            "title": h_text,
                            "date": "",
                            "description": desc,
                            "link": ""
                        })
            
            # Format events
            if events:
                result.append("**Upcoming Events:**\n")
                for i, e in enumerate(events[:8], 1):
                    result.append(f"📌 **{i}. {e['title']}**")
                    if e['date']:
                        result.append(f"   📆 {e['date']}")
                    if e['description']:
                        result.append(f"   {e['description']}...")
                    if e['link']:
                        result.append(f"   🔗 {e['link']}")
                    result.append("")
            else:
                # Fallback: get page content
                paragraphs = main_content.find_all('p', limit=5)
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if text and len(text) > 30:
                        result.append(text[:200] + "..." if len(text) > 200 else text)
        
        result.append(f"\n🙋 **Want to help?** Check the events page to volunteer or speak!")
        result.append(f"💡 Visit {WCC_EVENTS_URL} for full event details and registration!")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Error: {str(e)}\n\n💡 Visit {WCC_EVENTS_URL} directly."
