# Content Production Pipeline - Use Case Guide

## Overview

Build a sequential multi-agent pipeline that automates content creation from research to publication, with each agent handling one stage of the process.

## Problem Statement

**Challenge**: Creating quality content involves multiple distinct stages:
- Researching information and sources
- Writing the first draft
- Editing and improving content
- Optimizing for search (SEO)
- Creating promotional social media posts

**Why it matters**: Quality content drives community engagement and growth. A pipeline ensures consistency and quality at each stage.

## What You'll Build

A content production pipeline with:
- **Researcher Agent**: Gathers information and sources
- **Writer Agent**: Creates the first draft
- **Editor Agent**: Reviews and improves content
- **SEO Agent**: Optimizes for search engines
- **Social Media Agent**: Creates promotional posts
- **Pipeline Coordinator**: Manages the sequential workflow

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Content Request                           │
│        "Write a blog post about getting started with AI"     │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  PIPELINE COORDINATOR                        │
│              Manages sequential workflow                     │
└─────────────────────────────┬───────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   ┌─────────┐          ┌─────────┐          ┌─────────┐
   │Research │    →     │ Writer  │    →     │ Editor  │
   │ Agent   │          │ Agent   │          │ Agent   │
   └─────────┘          └─────────┘          └─────────┘
        │                     │                     │
        │    Research         │    Draft           │    Polished
        │    Notes            │    Content         │    Content
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   ┌─────────┐          ┌─────────┐          ┌─────────┐
   │   SEO   │    →     │ Social  │    →     │  Final  │
   │ Agent   │          │ Media   │          │ Output  │
   └─────────┘          └─────────┘          └─────────┘
```

## Implementation Guide

### Step 1: Define Your Pipeline Structure

```text
content_pipeline/
├── __init__.py
├── agent.py                 # Pipeline Coordinator
├── agents/
│   ├── __init__.py
│   ├── researcher.py
│   ├── writer.py
│   ├── editor.py
│   ├── seo.py
│   └── social_media.py
├── tools/
│   ├── __init__.py
│   └── content_tools.py
├── shared_state.py          # Shared memory between agents
└── requirements.txt
```

### Step 2: Create Shared State

```python
# shared_state.py

"""
Shared state that passes through the pipeline.
Each agent adds to or modifies this state.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class ContentState:
    """State object that flows through the pipeline."""
    
    # Initial request
    topic: str = ""
    target_audience: str = "WCC community members"
    content_type: str = "blog_post"
    
    # Research stage
    research_notes: str = ""
    sources: List[str] = field(default_factory=list)
    key_points: List[str] = field(default_factory=list)
    
    # Writing stage
    draft: str = ""
    word_count: int = 0
    
    # Editing stage
    edited_content: str = ""
    edit_suggestions: List[str] = field(default_factory=list)
    
    # SEO stage
    seo_title: str = ""
    meta_description: str = ""
    keywords: List[str] = field(default_factory=list)
    
    # Social media stage
    twitter_post: str = ""
    linkedin_post: str = ""
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    current_stage: str = "research"
    
    def to_dict(self) -> dict:
        return {
            "topic": self.topic,
            "research_notes": self.research_notes,
            "draft": self.draft,
            "edited_content": self.edited_content,
            "seo_title": self.seo_title,
            "social_posts": {
                "twitter": self.twitter_post,
                "linkedin": self.linkedin_post,
            },
            "current_stage": self.current_stage,
        }

# Global state instance (in production, use proper state management)
pipeline_state = ContentState()
```

### Step 3: Create Content Tools

```python
# tools/content_tools.py

import json
from typing import List

def research_topic(topic: str) -> str:
    """Research a topic and gather information."""
    # Mock research results
    research = {
        "ai": {
            "key_points": [
                "AI is transforming how we work and learn",
                "Getting started with AI doesn't require a PhD",
                "Practical applications include chatbots, automation, and analysis",
                "Python is the most popular language for AI development",
            ],
            "sources": [
                "Google AI Documentation",
                "OpenAI Guides",
                "WCC AI Learning Series",
            ],
            "statistics": [
                "85% of enterprises will use AI by 2025",
                "AI market expected to reach $190B by 2025",
            ]
        },
        "python": {
            "key_points": [
                "Python is beginner-friendly with readable syntax",
                "Extensive libraries for any use case",
                "Strong community support",
            ],
            "sources": [
                "Python.org Documentation",
                "Real Python Tutorials",
            ],
        }
    }
    
    for key, data in research.items():
        if key in topic.lower():
            return json.dumps(data, indent=2)
    
    return json.dumps({
        "key_points": [f"Research needed for: {topic}"],
        "sources": ["Community knowledge base"],
    })

def check_grammar(text: str) -> str:
    """Check text for grammar and style issues."""
    issues = []
    
    # Simple checks (in production, use proper grammar API)
    if text.count("  ") > 0:
        issues.append("Double spaces detected")
    if not text[0].isupper():
        issues.append("First letter should be capitalized")
    if len(text.split()) < 100:
        issues.append("Content might be too short for a blog post")
    
    if issues:
        return f"Issues found:\n" + "\n".join(f"- {i}" for i in issues)
    return "✅ No grammar issues detected"

def analyze_seo(content: str, topic: str) -> str:
    """Analyze content for SEO optimization."""
    word_count = len(content.split())
    
    suggestions = {
        "title_suggestion": f"Getting Started with {topic.title()}: A Beginner's Guide",
        "meta_description": f"Learn how to get started with {topic}. This comprehensive guide covers everything beginners need to know.",
        "recommended_keywords": [topic.lower(), f"{topic} tutorial", f"{topic} for beginners", "women in tech"],
        "word_count": word_count,
        "seo_score": min(100, word_count // 10),  # Simple scoring
        "recommendations": [
            "Include keywords in first paragraph",
            "Add subheadings every 300 words",
            "Include internal links to related content",
            "Add alt text to any images",
        ]
    }
    
    return json.dumps(suggestions, indent=2)

def generate_social_posts(title: str, summary: str, link: str = "#") -> str:
    """Generate social media posts for content promotion."""
    posts = {
        "twitter": f"📝 New on the WCC Blog!\n\n{title}\n\n{summary[:100]}...\n\nRead more: {link}\n\n#WomenInTech #TechBlog #WCC",
        "linkedin": f"🎉 Excited to share our latest blog post!\n\n{title}\n\n{summary}\n\nWhether you're just starting out or looking to level up, this guide has something for you.\n\nRead the full post: {link}\n\n#WomenInTech #TechCommunity #Learning #CareerGrowth",
        "slack": f"📢 *New Blog Post Alert!*\n\n*{title}*\n\n{summary}\n\n🔗 Read it here: {link}\n\nLet us know what you think! 💬",
    }
    
    return json.dumps(posts, indent=2)

def save_content(stage: str, content: str) -> str:
    """Save content at each pipeline stage."""
    return f"✅ Content saved at {stage} stage ({len(content)} characters)"
```

### Step 4: Create Pipeline Agents

**Researcher Agent:**

```python
# agents/researcher.py

from google.adk.agents import Agent
from ..tools.content_tools import research_topic

researcher_agent = Agent(
    name="researcher",
    model="gemini-2.0-flash",
    instruction="""You are the Research Agent in the content pipeline.

YOUR ROLE:
- Gather information on the requested topic
- Identify key points to cover
- Find credible sources
- Create research notes for the writer

OUTPUT FORMAT:
Provide structured research notes including:
1. Key points to cover (5-7 main ideas)
2. Supporting facts and statistics
3. Source references
4. Suggested angle/approach

Pass your research to the next stage (Writer) with clear, organized notes.
""",
    tools=[research_topic],
)
```

**Writer Agent:**

```python
# agents/writer.py

from google.adk.agents import Agent
from ..tools.content_tools import save_content

writer_agent = Agent(
    name="writer",
    model="gemini-2.0-flash",
    instruction="""You are the Writer Agent in the content pipeline.

YOUR ROLE:
- Take research notes and create a first draft
- Write engaging, informative content
- Target the WCC community audience
- Follow blog post best practices

WRITING GUIDELINES:
- Start with a compelling hook
- Use clear, accessible language
- Include practical examples
- Break up text with subheadings
- End with a call-to-action

OUTPUT:
A complete first draft ready for editing.
Aim for 800-1200 words for blog posts.
""",
    tools=[save_content],
)
```

**Editor Agent:**

```python
# agents/editor.py

from google.adk.agents import Agent
from ..tools.content_tools import check_grammar, save_content

editor_agent = Agent(
    name="editor",
    model="gemini-2.0-flash",
    instruction="""You are the Editor Agent in the content pipeline.

YOUR ROLE:
- Review and improve the draft
- Check for clarity and flow
- Fix grammar and style issues
- Ensure consistent tone
- Strengthen weak sections

EDITING CHECKLIST:
- [ ] Clear introduction
- [ ] Logical flow between sections
- [ ] No jargon without explanation
- [ ] Active voice preferred
- [ ] Strong conclusion with CTA

OUTPUT:
Polished content ready for SEO optimization.
Include a list of changes made.
""",
    tools=[check_grammar, save_content],
)
```

**SEO Agent:**

```python
# agents/seo.py

from google.adk.agents import Agent
from ..tools.content_tools import analyze_seo, save_content

seo_agent = Agent(
    name="seo",
    model="gemini-2.0-flash",
    instruction="""You are the SEO Agent in the content pipeline.

YOUR ROLE:
- Optimize content for search engines
- Create compelling title and meta description
- Identify target keywords
- Suggest improvements for discoverability

SEO BEST PRACTICES:
- Title: 50-60 characters, include main keyword
- Meta description: 150-160 characters
- Keywords: 3-5 relevant terms
- Headings: Use H2, H3 with keywords
- Internal linking opportunities

OUTPUT:
- SEO-optimized title
- Meta description
- Target keywords
- Any content modifications for SEO
""",
    tools=[analyze_seo, save_content],
)
```

**Social Media Agent:**

```python
# agents/social_media.py

from google.adk.agents import Agent
from ..tools.content_tools import generate_social_posts

social_media_agent = Agent(
    name="social_media",
    model="gemini-2.0-flash",
    instruction="""You are the Social Media Agent in the content pipeline.

YOUR ROLE:
- Create promotional posts for the content
- Adapt messaging for each platform
- Maximize engagement potential

PLATFORM GUIDELINES:
- Twitter: 280 chars max, punchy, hashtags
- LinkedIn: Professional, detailed, industry hashtags
- Slack: Community-focused, conversational

OUTPUT:
Ready-to-post content for:
1. Twitter
2. LinkedIn  
3. Slack announcement
""",
    tools=[generate_social_posts],
)
```

### Step 5: Create Pipeline Coordinator

```python
# agent.py

from google.adk.agents import Agent
from .agents import (
    researcher_agent,
    writer_agent,
    editor_agent,
    seo_agent,
    social_media_agent,
)

root_agent = Agent(
    name="content_pipeline_coordinator",
    model="gemini-2.0-flash",
    instruction="""You coordinate the Content Production Pipeline.

PIPELINE STAGES (in order):
1. @researcher → Gathers information and sources
2. @writer → Creates first draft from research
3. @editor → Reviews and polishes content
4. @seo → Optimizes for search engines
5. @social_media → Creates promotional posts

WORKFLOW:
Execute stages sequentially, passing output from each stage to the next.

For each stage:
1. Explain what's happening
2. Execute the agent
3. Summarize the output
4. Pass to next stage

FINAL OUTPUT:
Compile all outputs into a complete content package:
- Final blog post
- SEO metadata
- Social media posts

You can also run individual stages if requested.
""",
    sub_agents=[
        researcher_agent,
        writer_agent,
        editor_agent,
        seo_agent,
        social_media_agent,
    ],
)
```

## Example Workflows

### Workflow 1: Full Pipeline

**User**: "Create a blog post about getting started with Python"

**Flow**:
1. Researcher → Gathers Python learning resources
2. Writer → Creates 1000-word beginner guide
3. Editor → Polishes and improves clarity
4. SEO → Adds title, meta, keywords
5. Social Media → Creates promo posts

### Workflow 2: Partial Pipeline

**User**: "I have a draft, just need editing and SEO"

**Flow**:
1. Skip Research and Writing
2. Editor → Reviews provided draft
3. SEO → Optimizes the edited content

### Workflow 3: Single Stage

**User**: "Generate social media posts for this article"

**Flow**:
1. Social Media Agent only
2. Creates platform-specific posts

## Submission Checklist

- [ ] 5 pipeline agents implemented
- [ ] Sequential workflow demonstrated
- [ ] State passed between agents
- [ ] Full pipeline execution working
- [ ] README with pipeline diagram
- [ ] Example content package documented

## Resources

- [Google ADK Multi-Agent Docs](https://google.github.io/adk-docs/agents/multi-agents/)
- [Starter Template](../starter-template/)

---

## Questions?

Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel
