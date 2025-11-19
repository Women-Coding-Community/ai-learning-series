# Use Case: Mentorship Knowledge Base Q&A

**Difficulty:** Easy | **Time:** 3-4 hours | **Data:** Manual FAQ

Build a RAG system that answers mentorship questions with citations.

## Problem

Members ask common mentorship questions repeatedly. Answers are scattered across Slack, docs, and past sessions.

## Solution

RAG system over mentorship FAQs and guidance documents.

## Data Collection (30 min)

Create `data/mentorship-faq.md`:

```markdown
# Mentorship FAQ

## Preparing for Your First Session

Before your first meeting, clarify your goals. Are you looking for career guidance? 
Technical skills? Interview preparation? Be specific.

Research your mentor's background on LinkedIn. Understand their experience so you 
can ask relevant questions.

## During Sessions

Respect your mentor's time. Arrive prepared with:
- Progress updates on previous action items
- Specific questions or challenges you're facing
- Notes to capture advice and resources

## Between Sessions

Act on the advice you receive. Mentors appreciate mentees who implement suggestions.

Keep communication professional but warm. A brief monthly update email shows you 
value the relationship.

## Common Mistakes to Avoid

- Being vague about what you want to achieve
- Not doing your homework between sessions
- Expecting mentors to solve all problems for you
- Ghosting after getting what you need
```

## Implementation (2-3 hours)

### 1. Load Data

```python
from rag_pipeline import RAGPipeline

rag = RAGPipeline(project_id="your-project-id")

# Load FAQ
with open("data/mentorship-faq.md") as f:
    content = f.read()

documents = [
    {
        "title": "Mentorship FAQ",
        "url": "https://wcc.example.com/mentorship",
        "content": content
    }
]

rag.chunk_documents(documents, chunk_size=400)
rag.embed_and_store()
```

### 2. Test Search

```python
queries = [
    "How do I prepare for my first mentorship session?",
    "What should I do between sessions?",
    "What mistakes should I avoid?"
]

for q in queries:
    results = rag.search(q, k=3)
    print(f"\nQuery: {q}")
    for r in results:
        print(f"  - {r['metadata']['title']}")
```

### 3. Build RAG Interface

```python
# CLI
while True:
    question = input("\nYour question: ")
    result = rag.query(question)
    print(f"\nAnswer: {result['answer']}")
    print(f"Sources: {[s['title'] for s in result['sources']]}")
```

Or Streamlit:

```python
import streamlit as st
from rag_pipeline import RAGPipeline

st.title("WCC Mentorship Q&A")
rag = RAGPipeline(project_id="your-project-id")

question = st.text_input("Ask a mentorship question:")
if question:
    result = rag.query(question)
    st.write(result['answer'])
    st.write("**Sources:**")
    for source in result['sources']:
        st.write(f"- {source['title']}")
```

## Experimentation (1 hour)

Try different chunk sizes and document your findings:

```python
for chunk_size in [200, 400, 800]:
    rag.chunk_documents(documents, chunk_size=chunk_size)
    rag.embed_and_store()
    
    # Test queries
    results = rag.search("How do I prepare for my first session?", k=3)
    print(f"Chunk size {chunk_size}: {len(results)} results")
```

## Submission

Create `participants/[your-username]/mentorship-kb/`:

```text
mentorship-kb/
├── rag_pipeline.py          # Your implementation
├── data/
│   └── mentorship-faq.md    # Your FAQ
├── main.py                  # CLI or Streamlit app
├── requirements.txt
└── README.md
```

In README, include:

- What chunk size worked best
- 3 example queries and answers
- Challenges you faced

## Tips

- Start with 1-2 FAQ documents
- Test with real mentorship questions
- Experiment with chunk overlap (50-100 tokens)
- Consider adding metadata (date, author)

---

**Next:** Try [Event Archive](./event-archive-qa.md) or [Blog Search](./wcc-blog-search.md)
