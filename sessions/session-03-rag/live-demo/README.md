# Session 3 Live Demo - RAG Pipeline

## Overview

This folder contains the complete live coding demo for **Session 3: Introduction to RAG (Retrieval Augmented Generation)**.

We'll build a complete RAG system that:

1. Chunks WCC blog posts
2. Generates embeddings with Vertex AI
3. Stores in ChromaDB (local vector database)
4. Performs semantic search
5. Connects to Gemini for RAG with citations

---

## Prerequisites

Before running the demo, make sure you have:

1. ✅ Python 3.11+ installed
2. ✅ GCP project with Vertex AI enabled
3. ✅ Service account credentials (or use `gcloud auth`)
4. ✅ All dependencies installed

### Quick Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up GCP authentication
gcloud auth application-default login

# 3. Update PROJECT_ID in rag_demo.py
# Edit line 27: PROJECT_ID = "your-project-id"
```

---

## Files in This Folder

- **`rag_demo.py`** - Main RAG implementation with all 5 steps
- **`streamlit_app.py`** - Interactive web UI for the RAG system
- **`vertex_ai_quick_demo.py`** - Quick demo focusing on Vertex AI integration
- **`requirements.txt`** - Python dependencies
- **`README.md`** - This file

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up GCP Credentials

Option A: Use gcloud CLI (recommended)

```bash
gcloud auth application-default login
```

Option B: Use service account JSON

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

### 3. Update Project ID

Edit `rag_demo.py` line 27:

```python
PROJECT_ID = "your-gcp-project-id"  # TODO: Update this
```

### 4. Run the Demo

**Option A: CLI Demo (recommended for live coding)**

```bash
python rag_demo.py --all          # Run all demos
python rag_demo.py --reset        # Reset and re-setup
python rag_demo.py --search       # Demo semantic search only
python rag_demo.py --rag          # Demo RAG pipeline only
```

**Option B: Interactive Streamlit UI**

```bash
streamlit run streamlit_app.py
```

**Option C: Quick Vertex AI Demo**

```bash
python vertex_ai_quick_demo.py
```

---

## Demo Structure: 45-Minute Hands-On Breakdown

The live demo follows this structure aligned to your presentation:

### ⏱️ Timeline

- **Step 1: Chunking Documents (10 min)** - Break blog posts into manageable pieces
- **Step 2: Generate Embeddings (15 min)** - Convert chunks to vectors with Vertex AI
- **Step 3: Store in ChromaDB (5 min)** - Index embeddings for fast search
- **Step 4: Semantic Search (10 min)** - Find relevant chunks by meaning
- **Step 5: RAG Pipeline (5 min)** - Connect to Gemini for answers with citations

---

## Step 1: Chunking Documents (10 min)

**What you'll learn:**

- Why we need to chunk documents
- Different chunking strategies
- How chunk size affects results

**Key function:**

```python
def chunk_documents(blogs: List[Dict], chunk_size: int = 400, chunk_overlap: int = 50):
    """Break blog posts into 400-token chunks with 50-token overlap"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    # ... returns list of chunks with metadata
```

**Live demo command:**

```bash
python rag_demo.py --reset  # Chunks 5 WCC blog posts into ~50 chunks
```

**What to show:**

- Print first chunk preview
- Show chunk count
- Highlight metadata (title, URL, chunk_id)

---

## Step 2: Generate Embeddings (15 min)

**What you'll learn:**

- What embeddings are (768-dimensional vectors)
- How Vertex AI's text-embedding-004 works
- Batch processing for efficiency

**Key function:**

```python
def generate_embeddings(texts: List[str], batch_size: int = 5):
    """Generate embeddings using Vertex AI text-embedding-004"""
    embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = embedding_model.get_embeddings(batch)
    # ... returns list of 768-dimensional vectors
```

**Live demo command:**

```bash
python rag_demo.py --reset  # Generates embeddings for all chunks
```

**What to show:**

- Progress updates ("Processed 10/50 chunks...")
- Final embedding dimension (768)
- Time taken (~1 second per 10 chunks)

---

## Step 3: Store in ChromaDB (5 min)

**What you'll learn:**

- How vector databases work
- Storing embeddings + text + metadata
- Preparing for similarity search

**Key function:**

```python
def store_in_vectordb(chunks: List[Dict], embeddings: List[List[float]]):
    """Store in ChromaDB with embeddings, text, and metadata"""
    collection.add(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
```

**Live demo output:**

```text
✓ Stored 50 chunks in ChromaDB
  Collection size: 50
```

---

## Step 4: Semantic Search (10 min)

**What you'll learn:**

- How semantic search differs from keyword search
- Embedding similarity (cosine distance)
- Retrieving top-k results

**Key function:**

```python
def semantic_search(query: str, k: int = 5):
    """Search for relevant chunks by semantic similarity"""
    query_embedding = embedding_model.get_embeddings([query])[0].values
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    # ... returns top 5 most similar chunks
```

**Live demo command:**

```bash
python rag_demo.py --search
```

**Test queries to show:**

- "How do I start learning Python?"
- "What events did WCC host about web development?"
- "Tell me about mentorship at WCC"

**What to show:**

- Retrieved chunk titles
- Similarity distances (lower = more similar)
- Text previews

---

## Step 5: RAG Pipeline (5 min)

**What you'll learn:**

- Combining retrieval + generation
- Building prompts with context
- Source attribution

**Key function:**

```python
def rag_query(question: str, k: int = 5):
    """Complete RAG: retrieve context + generate answer with Gemini"""
    relevant_docs = semantic_search(question, k=k)
    context = "\n\n".join([doc['text'] for doc in relevant_docs])
    prompt = f"Answer based on context:\n{context}\n\nQuestion: {question}"
    response = generation_model.generate_content(prompt)
    return {'answer': response.text, 'sources': [doc['metadata'] for doc in relevant_docs]}
```

**Live demo command:**

```bash
python rag_demo.py --rag
```

**Test questions to show:**

- "What Python topics has WCC covered?"
- "How can I transition from backend to AI engineering?"
- "What advice do you have for mentees?"

**What to show:**

- Retrieved chunks used as context
- Gemini's answer with [Source X] citations
- Source links and titles

---

## Sample Data

The demo includes 5 pre-loaded WCC blog posts:

1. **Introduction to Python for Beginners** - Python basics, getting started
2. **Django Web Development Workshop Recap** - Web framework, MVT pattern
3. **Career Transitions: From Backend to AI Engineering** - Career advice, ML skills
4. **Effective Mentorship: Guide for Mentees** - Mentorship tips, best practices
5. **Cloud Architecture Best Practices for Startups** - Cloud platforms, architecture

Each blog post is automatically chunked, embedded, and stored when you run `--reset`.

---

## Running the Demo During Session

### Full Demo (Recommended for live coding)

```bash
python rag_demo.py --all
```

Runs all 5 steps sequentially with output.

### Reset and Re-setup

```bash
python rag_demo.py --reset
```

Clears ChromaDB and re-chunks, embeds, and stores all documents.

### Demo Semantic Search Only

```bash
python rag_demo.py --search
```

Shows search results for 3 test queries.

### Demo RAG Pipeline Only

```bash
python rag_demo.py --rag
```

Shows complete RAG answers for 4 test questions.

### Interactive Streamlit UI

```bash
streamlit run streamlit_app.py
```

Opens a web interface where you can:

- Type custom queries
- Adjust number of results
- See retrieved chunks
- View similarity distances

---

## Troubleshooting

### Error: "PROJECT_ID not set"

**Solution:**
Edit `rag_demo.py` line 27 and set your GCP project ID:

```python
PROJECT_ID = "your-actual-gcp-project-id"
```

### Error: "Authentication failed"

**Solution:**

```bash
gcloud auth application-default login
```

### Error: "ModuleNotFoundError: No module named 'chromadb'"

**Solution:**

```bash
pip install -r requirements.txt
```

### Error: "Collection is empty"

**Solution:**

```bash
python rag_demo.py --reset
```

### Slow embedding generation

**Note:** First run takes ~30-60 seconds to embed 50 chunks. Subsequent queries are instant (cached in ChromaDB).

---

## Customization Ideas

### Add Your Own Blog Posts

Edit `SAMPLE_BLOGS` in `rag_demo.py` to add more WCC content:

```python
SAMPLE_BLOGS = [
    {
        "title": "Your Blog Title",
        "date": "2024-11-19",
        "url": "https://womencodingcommunity.com/blog/your-post",
        "content": "Your blog content here..."
    },
    # ... more blogs
]
```

### Adjust Chunk Size

Experiment with different chunk sizes to see impact:

```python
chunks = chunk_documents(SAMPLE_BLOGS, chunk_size=200)  # Smaller chunks
chunks = chunk_documents(SAMPLE_BLOGS, chunk_size=800)  # Larger chunks
```

### Change Number of Retrieved Results

Modify `k` parameter in search/RAG functions:

```python
results = semantic_search(query, k=3)   # Get top 3
results = semantic_search(query, k=10)  # Get top 10
```

### Use Different LLM Model

Edit line 35 in `rag_demo.py`:

```python
generation_model = GenerativeModel("gemini-1.5-pro")  # More powerful
generation_model = GenerativeModel("gemini-2.0-flash")  # Faster
```

---

## Learning Outcomes

After this demo, you'll understand:

✅ Document chunking strategies and trade-offs  
✅ How embeddings represent semantic meaning  
✅ Vector databases and similarity search  
✅ Complete RAG pipeline architecture  
✅ Source attribution and citations  
✅ Hands-on experience with Vertex AI + ChromaDB + Gemini  

---

## Next Steps: Homework

1. **Collect your own data** (10-20 documents)
   - Scrape WCC blog posts, or
   - Use event descriptions, or
   - Create mentorship FAQs

2. **Build your RAG pipeline** (follow today's code)
   - Chunk documents
   - Generate embeddings
   - Store in ChromaDB
   - Test semantic search

3. **Experiment with parameters**
   - Try chunk_size = 200, 400, 800
   - Compare results
   - Document findings

4. **Implement source attribution**
   - Return blog titles and URLs
   - Show which chunks were retrieved

5. **Submit your work**
   - GitHub repo with code
   - README with results
   - Example queries and answers

---

## Resources

- [Vertex AI Embeddings Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-text-embeddings)
- [ChromaDB Python SDK](https://docs.trychroma.com/)
- [LangChain Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
- [Gemini API Reference](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- [RAG Best Practices](https://cloud.google.com/vertex-ai/docs/generative-ai/rag/overview)

---

## Questions?

Ask in the [WCC Slack](https://womencodingcommunity.slack.com/archives/C09L9C3FJP7) channel!

---

**Let's build amazing RAG systems together! 🚀**
