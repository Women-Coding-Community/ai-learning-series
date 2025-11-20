# Use Case: Event Archive Q&A

**Difficulty:** Medium | **Time:** 4-5 hours | **Data:** Meetup/CSV

Build a RAG system over WCC event history.

## Problem

Members want to search past events: "What events covered Python?" "Who spoke about cloud?"

## Solution

RAG system over event descriptions, speakers, and topics.

## Data Collection (1 hour)

Export from Meetup or create CSV:

```csv
title,date,speaker,description,url
"Python Basics Workshop","2024-10-15","Sarah Chen","Introduction to Python for beginners...","https://meetup.com/..."
"Django Web Development","2024-09-22","Maria K.","Building web apps with Django...","https://meetup.com/..."
```

Convert to documents:

```python
import csv

documents = []
with open("data/events.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        documents.append({
            "title": row['title'],
            "date": row['date'],
            "speaker": row['speaker'],
            "url": row['url'],
            "content": f"{row['title']}\nSpeaker: {row['speaker']}\n{row['description']}"
        })
```

## Implementation (2-3 hours)

### 1. Load and Chunk

```python
from rag_pipeline import RAGPipeline

rag = RAGPipeline(project_id="your-project-id")

# Load events
documents = [...]  # From CSV above

rag.chunk_documents(documents, chunk_size=500)
rag.embed_and_store()
```

### 2. Test Queries

```python
queries = [
    "What Python events did WCC host?",
    "Who spoke about cloud architecture?",
    "What events were in September?"
]

for q in queries:
    results = rag.search(q, k=5)
    print(f"\nQuery: {q}")
    for r in results:
        print(f"  - {r['metadata']['title']} ({r['metadata']['date']})")
```

### 3. Build Interface

```python
import streamlit as st
from rag_pipeline import RAGPipeline

st.title("WCC Event Archive")
rag = RAGPipeline(project_id="your-project-id")

question = st.text_input("Search events:")
if question:
    result = rag.query(question)
    st.write(result['answer'])
    
    st.write("**Events:**")
    for source in result['sources']:
        st.write(f"- **{source['title']}** ({source['date']})")
        st.write(f"  Speaker: {source['speaker']}")
        st.write(f"  [{source['url']}]({source['url']})")
```

## Experimentation (1-2 hours)

Test with different chunk sizes and metadata:

```python
# Try with/without speaker metadata
for include_speaker in [True, False]:
    if include_speaker:
        content = f"{row['title']}\nSpeaker: {row['speaker']}\n{row['description']}"
    else:
        content = f"{row['title']}\n{row['description']}"
    
    # Test and compare results
```

## Submission

Create `participants/[your-username]/event-archive/`:

```text
event-archive/
├── rag_pipeline.py
├── data/
│   └── events.csv
├── app.py
├── requirements.txt
└── README.md
```

In README:

- How many events indexed
- Best chunk size and why
- 3 example queries
- Challenges with structured data

## Tips

- Include metadata (date, speaker, topic tags)
- Test date-based queries
- Consider filtering by date range
- Add speaker names to search results

---

**Next:** Try [Blog Search](./wcc-blog-search.md) or [Mentorship KB](./mentorship-kb.md)
