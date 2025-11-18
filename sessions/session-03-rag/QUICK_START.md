# Session 3 RAG - Quick Start Guide

## 🚀 30-Second Setup

```bash
# 1. Install dependencies
cd sessions/session-03-rag/live-demo
pip install -r requirements.txt

# 2. Authenticate with GCP
gcloud auth application-default login

# 3. Update PROJECT_ID in rag_demo.py (line 27)
# Edit: PROJECT_ID = "your-gcp-project-id"

# 4. Pre-populate ChromaDB (do this before session!)
python rag_demo.py --reset
```

---

## 🎯 During Session (30 minutes)

### Terminal 1 - Main Demo

```bash
cd sessions/session-03-rag/live-demo
source venv/bin/activate  # or venv\Scripts\activate on Windows
python rag_demo.py --reset     # Pre-run before session (takes ~2-3 min)
python rag_demo.py --search    # Show search results
python rag_demo.py --rag       # Show RAG answers
```

### Terminal 2 - Streamlit (if time allows)

```bash
cd sessions/session-03-rag/live-demo
source venv/bin/activate
streamlit run streamlit_app.py
```

### Backup - Quick Demo (if issues)

```bash
python vertex_ai_quick_demo.py --interactive
```

### Full Demo (All Steps)

```bash
python rag_demo.py --all
```

---

## 📊 What You'll See

### Step 1: Chunking

```text
📄 STEP 1: Chunking Documents
✓ Created 50 chunks from 5 blog posts
  First chunk preview: "Title: Introduction to Python..."
```

### Step 2: Embeddings

```text
🧮 STEP 2: Generating Embeddings
  Processed 10/50 chunks...
  Processed 20/50 chunks...
✓ Generated 50 embeddings
  Embedding dimension: 768
```

### Step 3: Storage

```text
💾 STEP 3: Storing in ChromaDB
✓ Stored 50 chunks in ChromaDB
  Collection size: 50
```

### Step 4: Search

```text
🔍 Query: "How do I start learning Python?"
  Result 1: "Introduction to Python for Beginners" (distance: 0.243)
  Result 2: "Career Transitions: From Backend to AI" (distance: 0.287)
  Result 3: "Django Web Development Workshop" (distance: 0.301)
```

### Step 5: RAG

```text
❓ Question: "What Python topics has WCC covered?"
💬 Answer:
WCC has covered several Python topics [Source 1]:
- Introduction to Python for beginners [Source 1]
- Django web development [Source 2]
- Career transitions to AI engineering [Source 3]

📚 Sources:
• Introduction to Python for Beginners
  https://womencodingcommunity.com/blog/python-intro
• Django Web Development Workshop Recap
  https://womencodingcommunity.com/blog/django-workshop-recap
```

---

## 🔧 Troubleshooting

| Error | Solution |
|-------|----------|
| `PROJECT_ID not set` | Edit line 27 in `rag_demo.py` |
| `Authentication failed` | Run `gcloud auth application-default login` |
| `ModuleNotFoundError: chromadb` | Run `pip install -r requirements.txt` |
| `Collection is empty` | Run `python rag_demo.py --reset` |
| Slow embeddings | Normal on first run (~1 min). Subsequent queries are instant. |

---

## 📁 Files You Need

```text
sessions/session-03-rag/live-demo/
├── rag_demo.py              ← Main demo script
├── streamlit_app.py         ← Interactive UI
├── requirements.txt         ← Dependencies
├── README.md                ← Full documentation
└── SPEAKER_NOTES.md         ← Minute-by-minute script
```

---

## 🎓 Key Concepts (Cheat Sheet)

**Chunking:** Break documents into ~400-token pieces with 50-token overlap

**Embeddings:** 768-dimensional vectors representing text meaning

**Vector DB:** Database optimized for similarity search (not exact match)

**Semantic Search:** Find similar meaning, not just keywords

**RAG:** Retrieve context → Generate answer → Cite sources

---

## 💡 Pro Tips

- Pre-run `--reset` before session (takes ~1 min)
- Have slides open in another window
- Test internet connection (Vertex AI API calls)
- Keep terminal visible for output
- Have speaker notes handy for talking points

---

## 📞 Need Help?

- Check `SPEAKER_NOTES.md` for Q&A
- Check `README.md` for detailed troubleshooting
- Check `DEMO_PREP_SUMMARY.md` for full context

---

**You're ready! 🚀**
