# Session 3 Documentation Structure

## Overview

Clean, non-repetitive documentation organized by audience and purpose.

---

## 📋 Main Files

### `README.md` (Main Entry Point)

**Audience:** Everyone  
**Purpose:** Session overview + quick links  
**Content:**

- Session date, duration, objectives
- Folder structure
- Quick setup (5 min)
- Demo commands
- Use case comparison table
- Homework requirements
- Links to detailed docs

**Length:** ~100 lines (concise)

---

### `QUICK_START.md` (30-Second Setup)

**Audience:** Instructors + participants  
**Purpose:** Copy-paste commands to get running  
**Content:**

- Setup commands
- Demo commands
- Expected output
- Troubleshooting table

**Length:** ~160 lines

---

### `DEMO_PREP_SUMMARY.md` (Full Context)

**Audience:** Instructors  
**Purpose:** Complete prep guide for live demo  
**Content:**

- Pre-demo checklist
- 30-min timeline
- Key teaching points
- Tech stack choices
- Cost estimates
- Sample data overview
- Potential issues & solutions
- Homework details

**Length:** ~320 lines

---

## 📁 Subdirectories

### `live-demo/`

**Purpose:** Complete working example for live session

- `rag_demo.py` - Full RAG pipeline (5 steps)
- `streamlit_app.py` - Interactive UI
- `requirements.txt` - Dependencies
- `README.md` - Full documentation (45-min breakdown)
- `SPEAKER_NOTES.md` - Minute-by-minute script

**Not repeated in:** Main README, QUICK_START

---

### `starter-template/`

**Purpose:** Minimal template for participants to start building

- `rag_pipeline.py` - Simplified RAG class (to be created)
- `requirements.txt` - Dependencies
- `README.md` - Quick start + customization examples

**Content:**

- Setup instructions
- Core RAG pipeline code example
- Customization options (chunk size, k, model)
- Links to use-case guides

**Not repeated in:** Main README, live-demo/README

---

### `use-case-guides/`

**Purpose:** Concrete implementations for each use case

#### `mentorship-kb.md`

- Data collection (30 min)
- Implementation (2-3 hours)
- Experimentation (1 hour)
- Submission checklist
- Tips

#### `event-archive-qa.md`

- Data collection (1 hour)
- CSV format example
- Implementation (2-3 hours)
- Streamlit interface
- Experimentation

#### `wcc-blog-search.md`

- Data collection (2-3 hours)
- Web scraping code
- Manual collection option
- Implementation (2-3 hours)
- Full Streamlit app
- Challenges & solutions table

**Not repeated in:** Main README, starter-template

---

## 🔗 Navigation

```text
README.md (Main entry)
├── QUICK_START.md (Setup)
├── DEMO_PREP_SUMMARY.md (Instructor prep)
├── live-demo/
│   ├── README.md (Full demo docs)
│   └── SPEAKER_NOTES.md (Live script)
├── starter-template/
│   └── README.md (Getting started)
└── use-case-guides/
    ├── mentorship-kb.md (Easy)
    ├── event-archive-qa.md (Medium)
    └── wcc-blog-search.md (Hard)
```

---

## 📊 Content Distribution

| File | Audience | Length | Purpose |
|------|----------|--------|---------|
| README.md | Everyone | ~100 | Overview + links |
| QUICK_START.md | Instructors | ~160 | Copy-paste commands |
| DEMO_PREP_SUMMARY.md | Instructors | ~320 | Full prep context |
| live-demo/README.md | Developers | ~470 | Complete demo docs |
| live-demo/SPEAKER_NOTES.md | Instructors | ~320 | Live script |
| starter-template/README.md | Participants | ~80 | Quick start |
| use-case-guides/*.md | Participants | 150-200 each | Concrete examples |

**Total:** ~1,500 lines across 8 files (no significant repetition)

---

## ✅ No Repetition Principles

1. **Main README** - Links only, no detailed instructions
2. **QUICK_START** - Commands only, no explanations
3. **DEMO_PREP_SUMMARY** - Instructor context only
4. **live-demo/README** - Full technical details for demo
5. **live-demo/SPEAKER_NOTES** - Talking points for instructors
6. **starter-template/README** - Minimal code + customization
7. **use-case-guides** - Concrete implementations, not theory

---

## 🎯 User Journeys

### Instructor (Pre-Session)

1. README.md (overview)
2. QUICK_START.md (setup)
3. DEMO_PREP_SUMMARY.md (full context)
4. live-demo/SPEAKER_NOTES.md (during session)

### Participant (During Session)

1. README.md (overview)
2. Watch live demo
3. Follow along with live-demo/README.md

### Participant (After Session - Homework)

1. README.md (homework requirements)
2. starter-template/README.md (getting started)
3. Pick use case: mentorship-kb.md | event-archive-qa.md | wcc-blog-search.md
4. Build and submit

---

## 🚀 Ready for Session

✅ Main README - Concise, links-based  
✅ Quick Start - Copy-paste commands  
✅ Demo Prep - Full instructor context  
✅ Live Demo - Complete working code + docs  
✅ Starter Template - Minimal entry point  
✅ Use Case Guides - 3 concrete implementations  

**No significant repetition across files.**
