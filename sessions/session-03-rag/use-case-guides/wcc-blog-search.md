# Use Case: WCC Blog Search & Q&A

**Difficulty:** Hard | **Time:** 5-6 hours | **Data:** Web scraping

Build a RAG system over WCC blog posts with semantic search.

## Problem

Members can't easily find relevant blog posts or extract information from them.

## Solution

RAG system with semantic search over blog content + Q&A with citations.

## Data Collection (2-3 hours)

### Option A: Web Scraping

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_wcc_blogs():
    """Scrape blog posts from WCC website"""
    documents = []
    
    # Replace with actual WCC blog URL
    base_url = "https://womencodingcommunity.com/blog"
    
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    for article in soup.find_all('article'):
        title = article.find('h2').text
        url = article.find('a')['href']
        date = article.find('time')['datetime']
        
        # Get full article content
        article_response = requests.get(url)
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        content = article_soup.find('main').text
        
        documents.append({
            "title": title,
            "date": date,
            "url": url,
            "content": content
        })
    
    return documents
```

### Option B: Manual Collection

Save blog posts as markdown files in `data/blogs/`:

```text
data/blogs/
├── python-intro.md
├── django-workshop.md
├── career-transition.md
└── mentorship-guide.md
```

Then load:

```python
import os
from pathlib import Path

documents = []
for file in Path("data/blogs").glob("*.md"):
    with open(file) as f:
        documents.append({
            "title": file.stem.replace("-", " ").title(),
            "url": f"https://wcc.example.com/blog/{file.stem}",
            "content": f.read()
        })
```

## Implementation (2-3 hours)

### 1. Load and Chunk

```python
from rag_pipeline import RAGPipeline

rag = RAGPipeline(project_id="your-project-id")

# Load blogs
documents = scrape_wcc_blogs()  # or load from files

# Chunk with overlap for better context
rag.chunk_documents(documents, chunk_size=500, chunk_overlap=100)
rag.embed_and_store()

print(f"Indexed {len(documents)} blog posts")
```

### 2. Test Search Quality

```python
test_queries = [
    "How do I start learning Python?",
    "What's the best way to transition to AI?",
    "How can I get mentorship?",
    "What web frameworks does WCC cover?"
]

for query in test_queries:
    results = rag.search(query, k=3)
    print(f"\nQuery: {query}")
    for r in results:
        print(f"  - {r['metadata']['title']} (distance: {r['distance']:.3f})")
```

### 3. Build Search Interface

```python
import streamlit as st
from rag_pipeline import RAGPipeline

st.set_page_config(page_title="WCC Blog Search", layout="wide")
st.title("🔍 WCC Blog Search")

rag = RAGPipeline(project_id="your-project-id")

# Search box
query = st.text_input("Search WCC blogs:")

if query:
    # Show semantic search results
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Semantic Search")
        results = rag.search(query, k=5)
        for i, r in enumerate(results, 1):
            st.write(f"**{i}. {r['metadata']['title']}**")
            st.write(f"Distance: {r['distance']:.3f}")
            st.write(f"[Read more]({r['metadata']['url']})")
            st.divider()
    
    with col2:
        st.subheader("AI Answer")
        result = rag.query(query)
        st.write(result['answer'])
        st.write("**Sources:**")
        for source in result['sources']:
            st.write(f"- [{source['title']}]({source['url']})")
```

## Experimentation (1-2 hours)

Compare different strategies:

```python
# Test 1: Chunk size impact
for chunk_size in [300, 500, 800]:
    rag.chunk_documents(documents, chunk_size=chunk_size)
    rag.embed_and_store()
    
    # Measure search quality
    results = rag.search("Python tutorial", k=3)
    print(f"Chunk size {chunk_size}: avg distance {sum(r['distance'] for r in results)/3:.3f}")

# Test 2: Semantic vs keyword search
query = "How do I start coding?"
semantic_results = rag.search(query, k=3)
# Compare with simple keyword search on titles
```

## Submission

Create `participants/[your-username]/blog-search/`:

```text
blog-search/
├── rag_pipeline.py
├── scraper.py              # If using web scraping
├── data/
│   └── blogs/              # Blog posts
├── app.py                  # Streamlit app
├── requirements.txt
└── README.md
```

In README:

- How many blog posts indexed
- Scraping approach (manual vs automated)
- Best chunk size and reasoning
- 5 example queries with results
- Challenges with real-world data
- Ideas for improvement

## Tips

- Start with 5-10 blog posts
- Use overlap to preserve context at chunk boundaries
- Test with real user questions
- Consider adding blog category/topic as metadata
- Handle HTML/markdown formatting carefully
- Cache embeddings to avoid re-embedding

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Slow scraping | Cache results, use async requests |
| Duplicate content | Deduplicate before chunking |
| Poor search results | Adjust chunk size, add metadata |
| Hallucination in answers | Strict prompt instructions for citations |

---

**Next:** Compare with [Event Archive](./event-archive-qa.md) or [Mentorship KB](./mentorship-kb.md)
