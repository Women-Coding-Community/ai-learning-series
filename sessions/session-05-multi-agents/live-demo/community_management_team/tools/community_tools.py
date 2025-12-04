"""
Shared tools for the WCC Community Management Multi-Agent System.

These tools are used by multiple agents to access community data,
manage content, and coordinate activities.
"""

import json
from datetime import datetime, timedelta
from typing import Optional

# =============================================================================
# Mock Data - In production, these would connect to real databases/APIs
# =============================================================================

WCC_INFO = {
    "name": "Women Coding Community",
    "mission": "Empowering women in tech through learning, mentorship, and community",
    "website": "https://womencodingcommunity.com",
    "slack": "https://womencodingcommunity.slack.com",
    "github": "https://github.com/Women-Coding-Community",
    "programs": [
        "AI Learning Series",
        "Mentorship Program",
        "Study Groups",
        "Career Development Workshops",
    ],
}

UPCOMING_EVENTS = [
    {
        "name": "Session 5: Multi-Agent Systems",
        "date": "December 3, 2025",
        "time": "6:00 PM GMT",
        "description": "Learn to build AI agents that work together",
        "type": "workshop",
    },
    {
        "name": "Python Study Group",
        "date": "December 5, 2025",
        "time": "7:00 PM GMT",
        "description": "Weekly Python practice session",
        "type": "study_group",
    },
    {
        "name": "Career Panel: Breaking into AI",
        "date": "December 10, 2025",
        "time": "6:30 PM GMT",
        "description": "Industry experts share their AI career journeys",
        "type": "panel",
    },
]

FAQ_DATABASE = {
    "mentorship": "Our mentorship program pairs experienced developers with learners. Sign up at #mentorship channel on Slack.",
    "join": "Join WCC by visiting our website and signing up for our Slack community. It's free!",
    "events": "Check our #events channel on Slack or our website calendar for upcoming events.",
    "contribute": "You can contribute by joining study groups, mentoring others, or contributing to our GitHub repos.",
    "ai_series": "The AI Learning Series is a 6-session program covering chatbots, prompt engineering, RAG, and AI agents.",
}

CONTENT_TEMPLATES = {
    "event_announcement": "🎉 Join us for {event_name}!\n\n📅 {date}\n⏰ {time}\n\n{description}\n\n#WomenInTech #WCC",
    "workshop_reminder": "⏰ Reminder: {event_name} is happening {when}!\n\nDon't miss out on learning {topic}.\n\nSee you there! 💪",
    "welcome_post": "👋 Welcome to Women Coding Community!\n\nWe're so glad you're here. Here's how to get started:\n1️⃣ Introduce yourself in #introductions\n2️⃣ Check out #events for upcoming sessions\n3️⃣ Join a study group that interests you\n\n#WCC #WomenInTech",
}

CONTENT_GUIDELINES = [
    "Be respectful and inclusive",
    "No spam or self-promotion without approval",
    "Keep discussions professional",
    "No harassment or discrimination",
    "Protect member privacy",
]

# In-memory storage for drafts
DRAFTS_STORAGE = []


# =============================================================================
# Tool Functions
# =============================================================================

def get_wcc_info() -> str:
    """
    Get information about Women Coding Community.
    
    Returns:
        str: JSON string with WCC information including mission, programs, and links.
    """
    return json.dumps(WCC_INFO, indent=2)


def get_upcoming_events(event_type: Optional[str] = None) -> str:
    """
    Get list of upcoming WCC events.
    
    Args:
        event_type: Optional filter for event type (workshop, study_group, panel).
        
    Returns:
        str: JSON string with list of upcoming events.
    """
    events = UPCOMING_EVENTS
    if event_type:
        events = [e for e in events if e.get("type") == event_type]
    
    if not events:
        return "No upcoming events found matching the criteria."
    
    return json.dumps(events, indent=2)


def search_faq(query: str) -> str:
    """
    Search the FAQ database for answers to common questions.
    
    Args:
        query: The search query or topic to look up.
        
    Returns:
        str: The FAQ answer if found, or a message indicating no match.
    """
    query_lower = query.lower()
    
    for keyword, answer in FAQ_DATABASE.items():
        if keyword in query_lower:
            return f"FAQ Answer: {answer}"
    
    return "I couldn't find a specific FAQ for that topic. Please ask in our Slack community for help!"


def get_content_templates(template_type: str) -> str:
    """
    Get content templates for social media posts.
    
    Args:
        template_type: Type of template (event_announcement, workshop_reminder, welcome_post).
        
    Returns:
        str: The template string or list of available templates.
    """
    if template_type in CONTENT_TEMPLATES:
        return f"Template for '{template_type}':\n\n{CONTENT_TEMPLATES[template_type]}"
    
    available = ", ".join(CONTENT_TEMPLATES.keys())
    return f"Template '{template_type}' not found. Available templates: {available}"


def check_content_guidelines(content: str) -> str:
    """
    Check if content adheres to community guidelines.
    
    Args:
        content: The content to check.
        
    Returns:
        str: Assessment of whether content follows guidelines.
    """
    issues = []
    content_lower = content.lower()
    
    # Simple checks (in production, use more sophisticated moderation)
    inappropriate_words = ["spam", "buy now", "click here", "free money"]
    for word in inappropriate_words:
        if word in content_lower:
            issues.append(f"Potential spam detected: '{word}'")
    
    if len(content) < 10:
        issues.append("Content is too short")
    
    if len(content) > 2000:
        issues.append("Content exceeds recommended length (2000 chars)")
    
    if issues:
        return f"⚠️ Content Review Issues:\n" + "\n".join(f"- {issue}" for issue in issues)
    
    return "✅ Content passes guidelines check. Ready to post!"


def get_optimal_posting_times(platform: str = "general") -> str:
    """
    Get optimal posting times for different platforms.
    
    Args:
        platform: The social media platform (twitter, linkedin, slack, general).
        
    Returns:
        str: Recommended posting times.
    """
    posting_times = {
        "twitter": "Best times: 9 AM, 12 PM, 5 PM (local time). Weekdays perform better.",
        "linkedin": "Best times: Tuesday-Thursday, 10 AM - 12 PM. Professional content works best.",
        "slack": "Best times: 10 AM - 2 PM on weekdays. Avoid weekends and late evenings.",
        "general": "Best times across platforms: Weekdays 10 AM - 2 PM. Tuesday and Wednesday are optimal.",
    }
    
    return posting_times.get(platform.lower(), posting_times["general"])


def save_draft(title: str, content: str, author: str = "agent") -> str:
    """
    Save a content draft for later review or posting.
    
    Args:
        title: Title or identifier for the draft.
        content: The draft content.
        author: Who created the draft.
        
    Returns:
        str: Confirmation message with draft ID.
    """
    draft = {
        "id": len(DRAFTS_STORAGE) + 1,
        "title": title,
        "content": content,
        "author": author,
        "created_at": datetime.now().isoformat(),
        "status": "draft",
    }
    DRAFTS_STORAGE.append(draft)
    
    return f"✅ Draft saved successfully!\nDraft ID: {draft['id']}\nTitle: {title}"


def get_drafts(status: str = "all") -> str:
    """
    Get list of saved drafts.
    
    Args:
        status: Filter by status (draft, approved, posted, all).
        
    Returns:
        str: JSON string with list of drafts.
    """
    if not DRAFTS_STORAGE:
        return "No drafts found."
    
    drafts = DRAFTS_STORAGE
    if status != "all":
        drafts = [d for d in drafts if d.get("status") == status]
    
    if not drafts:
        return f"No drafts found with status '{status}'."
    
    return json.dumps(drafts, indent=2)
