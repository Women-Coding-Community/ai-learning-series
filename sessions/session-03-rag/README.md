# Session 3: Introduction to RAG (Retrieval Augmented Generation)

**Date:** November 19, 2025  
**Instructor:** Sonika  
**Duration:** 60 minutes (15 min theory + 30 min live demo + 15 min wrap-up)

## 🎯 Learning Objectives

- Understand embeddings and semantic similarity
- Build a complete RAG pipeline
- Use Vertex AI embeddings and ChromaDB
- Implement source attribution
- Experiment with chunking strategies

## 📁 Folder Structure

```text
session-03-rag/
├── README.md                    # This file
├── QUICK_START.md               # 30-second setup guide
├── DEMO_PREP_SUMMARY.md         # Full prep context
├── live-demo/                   # Live coding demo
│   ├── rag_demo.py
│   ├── streamlit_app.py
│   ├── requirements.txt
│   ├── README.md
│   └── SPEAKER_NOTES.md
├── starter-template/            # Template for participants
│   ├── rag_pipeline.py
│   ├── requirements.txt
│   └── README.md
├── use-case-guides/             # Use case implementations
│   ├── wcc-blog-search.md
│   ├── event-archive-qa.md
│   └── mentorship-kb.md
└── participants/                # Participant submissions
    ├── username1/
    └── ...
```

## 🚀 Quick Start

### Setup (5 min)

```bash
cd sessions/session-03-rag/live-demo
pip install -r requirements.txt
gcloud auth application-default login
# Edit line 27: PROJECT_ID = "your-gcp-project-id"
python rag_demo.py --reset
```

### Run Demo (30 min)

```bash
python rag_demo.py --all          # Full demo
python rag_demo.py --search       # Search only
python rag_demo.py --rag          # RAG only
streamlit run streamlit_app.py    # Interactive UI
```

See [QUICK_START.md](./QUICK_START.md) for details.

## 📚 What's Included

- **Live Demo:** Complete RAG pipeline with 5 WCC blog posts pre-loaded
- **Starter Template:** Minimal code to build your own RAG system
- **Use Case Guides:** 3 concrete implementations (Blog Search, Event Archive, Mentorship KB)
- **Speaker Notes:** Minute-by-minute script for instructors

## 🎓 Use Cases

Pick one for your homework:

| Use Case | Difficulty | Data Source | Best For |
|----------|-----------|-------------|----------|
| **Mentorship KB** | Easy | Manual FAQ | Learning, privacy-first |
| **Event Archive** | Medium | Meetup/CSV | Structured data |
| **Blog Search** | Hard | Web scraping | Real-world data |

See [use-case-guides/](./use-case-guides/) for detailed implementations.

## 📝 Homework

1. **Collect data:** 10-20 documents for your chosen use case
2. **Build pipeline:** Follow starter template
3. **Experiment:** Try chunk_size = 200, 400, 800 and compare
4. **Submit:** GitHub repo with code + README + example queries

**Submission:** `sessions/session-03-rag/participants/[your-username]/`

## 📖 Resources

- [Live Demo README](./live-demo/README.md) - Full documentation
- [Starter Template](./starter-template/README.md) - Getting started
- [Vertex AI Embeddings](https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-text-embeddings)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [RAG Best Practices](https://cloud.google.com/vertex-ai/docs/generative-ai/rag/overview)

---

**Questions?** Ask in [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7)!
