# WCC AI Learning Series - Session 3: RAG Demo

## 🎯 What This Demo Does

This repository includes **TWO approaches** to building RAG systems:

### Approach 1: DIY RAG (rag_demo.py) - For Learning
Build RAG from scratch to understand every component:
1. **Document Chunking** - Breaking blog posts into manageable pieces
2. **Embedding Generation** - Converting text to vectors with Vertex AI
3. **Vector Storage** - Storing embeddings in ChromaDB
4. **Semantic Search** - Finding relevant content by meaning, not keywords
5. **RAG Pipeline** - Generating answers with citations using Gemini

**Best for:** Learning, understanding concepts, custom implementations

### Approach 2: Vertex AI RAG Engine (vertex_ai_rag_managed.py) - For Production
Use Google's managed RAG service where one API call handles everything:
- Automatic document ingestion from Cloud Storage
- Built-in chunking, embedding, and indexing
- Managed vector database
- Retrieval and generation in a single call
- Enterprise features (IAM, audit logs, scaling)

**Best for:** Production deployments, enterprise scale, managed infrastructure

## 🤔 Which Should I Use?

| Your Goal | Use This | Why |
|-----------|----------|-----|
| Learn RAG concepts | DIY RAG | See every step, full control |
| Build homework project | DIY RAG | Practice implementation |
| Prototype quickly | DIY RAG | Local, no infrastructure needed |
| Deploy to production | Vertex AI RAG | Managed, scales automatically |
| Enterprise requirements | Vertex AI RAG | Built-in security, compliance |
| Cost-conscious learning | DIY RAG | Free local option |

**Recommendation:** Start with DIY RAG to learn, then explore Vertex AI RAG for production use cases.

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or later
- Google Cloud Platform account with billing enabled
- GCP project with Vertex AI API enabled

### 1. Set Up GCP

```bash
# Install gcloud CLI (if not already installed)
# Visit: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud auth application-default login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Configure Project

Edit `rag_demo.py` and update:

```python
PROJECT_ID = "your-project-id"  # Your GCP project ID
LOCATION = "us-central1"         # Or your preferred region
```

### 4. Run the Demo

**Option A: DIY RAG (Recommended for learning)**

```bash
# Setup and index documents
python rag_demo.py --reset

# Test semantic search
python rag_demo.py --search

# Test RAG pipeline
python rag_demo.py --rag

# Run all demos
python rag_demo.py --all
```

**Option B: Vertex AI RAG Engine (Production approach)**

```bash
# One-time setup (creates corpus, uploads docs)
python vertex_ai_rag_managed.py --setup
# Save the corpus name from output!

# Run queries with the corpus
python vertex_ai_rag_managed.py --interactive <corpus-name>

# Example:
# python vertex_ai_rag_managed.py --interactive projects/my-project/locations/us-central1/ragCorpora/123

# Cleanup when done
python vertex_ai_rag_managed.py --cleanup <corpus-name>
```

**Option C: Quick Demo (No GCP setup needed)**

```bash
# Simplified demo with mock data
python vertex_ai_quick_demo.py --interactive
```

### 5. Launch Web UI

```bash
streamlit run streamlit_app.py
```

Then open http://localhost:8501 in your browser.

## 📁 Project Structure

```
session-3-rag/
├── rag_demo.py                    # DIY RAG implementation (main demo)
├── vertex_ai_rag_managed.py       # Vertex AI RAG Engine (production)
├── vertex_ai_quick_demo.py        # Quick demo without infrastructure
├── streamlit_app.py               # Web interface
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── PRESENTERS_GUIDE.md           # Delivery guide for instructors
├── QUICK_REFERENCE.md            # Quick reference card
└── .env.example                  # Environment variables template
```

## 🔄 DIY RAG vs Vertex AI RAG - Detailed Comparison

### Code Comparison

**DIY RAG (rag_demo.py):**
```python
# Manual control over every step
chunks = chunk_documents(blogs, chunk_size=400)
embeddings = generate_embeddings([c["text"] for c in chunks])
store_in_vectordb(chunks, embeddings)
results = semantic_search(query, k=5)
answer = rag_query(question)
```

**Vertex AI RAG (vertex_ai_rag_managed.py):**
```python
# One-time setup
corpus = rag.create_corpus(display_name="WCC Blogs")
rag.import_files(corpus=corpus, paths=["gs://bucket/blogs/"])

# Query (single call does everything!)
answer = rag.retrieval_query(corpus=corpus, query=question)
```

### Feature Comparison

| Feature | DIY RAG | Vertex AI RAG |
|---------|---------|---------------|
| **Setup Time** | ~30 minutes | ~5 minutes |
| **Lines of Code** | ~500 | ~50 |
| **Chunking Control** | Full control (custom strategies) | Automatic (configurable) |
| **Embedding Control** | Choose any model | Uses Vertex AI models |
| **Vector Database** | ChromaDB (local) | Managed (cloud) |
| **Scalability** | Limited to local resources | Enterprise scale |
| **Cost (learning)** | Free (local) | Pay per query (~$0.001) |
| **Access Control** | DIY implementation | Built-in IAM |
| **Audit Logs** | DIY implementation | Automatic |
| **Monitoring** | DIY implementation | Cloud Monitoring |
| **Learning Value** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Production Ready** | ⭐⭐ (needs hardening) | ⭐⭐⭐⭐⭐ |

### When to Use Each

**Use DIY RAG if you:**
- ✅ Want to learn how RAG works internally
- ✅ Need custom chunking logic
- ✅ Have small-medium datasets (< 100K documents)
- ✅ Want free local development
- ✅ Need complete control over the pipeline
- ✅ Are building a homework project
- ✅ Want to experiment and iterate quickly

**Use Vertex AI RAG if you:**
- ✅ Are deploying to production
- ✅ Need enterprise features (compliance, audit, IAM)
- ✅ Have large datasets (100K+ documents)
- ✅ Want managed infrastructure
- ✅ Don't want to maintain the pipeline
- ✅ Need automatic scaling
- ✅ Require 99.9% uptime SLA

### Typical Workflow

1. **Learn** with DIY RAG (rag_demo.py)
   - Understand each component
   - Experiment with different settings
   - Build intuition

2. **Prototype** with DIY RAG
   - Validate your use case
   - Test with real data
   - Measure performance

3. **Deploy** with Vertex AI RAG
   - Migrate to managed service
   - Add enterprise features
   - Scale to production

Think of it like learning to build a car engine (DIY) before buying a manufactured one (Vertex AI) - both have value!

## 🎓 Demo Walkthrough

### Option 1: Command Line Demo

The `rag_demo.py` script provides a complete walkthrough:

```bash
# 1. Reset and setup (processes all sample blogs)
python rag_demo.py --reset

# Output:
# ========================================
# WCC RAG SYSTEM SETUP
# ========================================
# 
# 📄 STEP 1: Chunking Documents
# ✓ Created 47 chunks from 5 blog posts
# 
# 🧮 STEP 2: Generating Embeddings
# ✓ Generated 47 embeddings
#   Embedding dimension: 768
# 
# 💾 STEP 3: Storing in ChromaDB
# ✓ Stored 47 chunks in ChromaDB
#   Collection size: 47

# 2. Test semantic search
python rag_demo.py --search

# 3. Test RAG pipeline
python rag_demo.py --rag
```

### Option 2: Interactive Web UI

Launch Streamlit for a user-friendly interface:

```bash
streamlit run streamlit_app.py
```

Features:
- **RAG Q&A Tab**: Ask questions, get answers with citations
- **Semantic Search Tab**: Pure search without LLM generation
- **Indexed Blogs Tab**: Browse all indexed content
- **Settings Sidebar**: Adjust number of results, toggle debug info

## 🔧 Code Explanation

### Document Chunking

```python
def chunk_documents(blogs, chunk_size=400, chunk_overlap=50):
    """
    Breaks documents into chunks using LangChain's RecursiveCharacterTextSplitter
    - Respects sentence boundaries
    - Maintains context with overlap
    - Preserves metadata (title, URL, date)
    """
```

**Why these settings?**
- `chunk_size=400`: Sweet spot for semantic coherence (~400 tokens)
- `chunk_overlap=50`: Prevents context loss at boundaries
- `separators=["\n\n", "\n", ". ", " "]`: Splits intelligently (paragraphs → sentences → words)

### Embedding Generation

```python
def generate_embeddings(texts, batch_size=5):
    """
    Converts text to 768-dimensional vectors using Vertex AI
    - Batch processing for efficiency
    - Uses text-embedding-004 model
    """
```

**Key points:**
- Each chunk becomes a 768-number vector
- Similar meanings = similar vectors
- Enables semantic search (not just keyword matching)

### Semantic Search

```python
def semantic_search(query, k=5):
    """
    Finds most similar chunks using cosine similarity
    - Embeds the query
    - Searches vector database
    - Returns top k matches with distance scores
    """
```

**Distance scores:**
- Lower = more similar
- Typical good match: < 0.5
- Marginal match: 0.5 - 0.8
- Poor match: > 0.8

### RAG Pipeline

```python
def rag_query(question, k=5):
    """
    Complete RAG flow:
    1. Search for relevant chunks
    2. Build context from top k results
    3. Create prompt with context + question
    4. Generate answer with Gemini
    5. Return answer with source attribution
    """
```

## 🧪 Testing the System

### Test Queries

Try these questions to test different aspects:

**Factual Questions:**
- "What Python events has WCC hosted?"
- "When was the Django workshop?"

**Conceptual Questions:**
- "How do I start learning Python?"
- "What are cloud architecture best practices?"

**Comparison Questions:**
- "What's the difference between semantic and keyword search?"

**Out-of-Scope Questions:**
- "What's the weather today?" (Should say not in context)

### Evaluating Results

Good RAG responses should:
- ✅ Answer only from provided context
- ✅ Include citations [Source 1], [Source 2]
- ✅ Say "I don't know" if context insufficient
- ✅ Not hallucinate information

## 🐛 Troubleshooting

### Authentication Errors

```
Error: Could not automatically determine credentials
```

**Solution:**
```bash
gcloud auth application-default login
```

### API Not Enabled

```
Error: API aiplatform.googleapis.com has not been used
```

**Solution:**
```bash
gcloud services enable aiplatform.googleapis.com
```

### ChromaDB Permission Error

```
Error: Permission denied: Cannot write to directory
```

**Solution:**
```bash
# Make sure you have write permissions
chmod -R 755 .
```

### Rate Limit Errors

```
Error: Rate limit exceeded
```

**Solution:**
- Reduce `batch_size` in `generate_embeddings()`
- Add delays between API calls
- Check GCP quotas

### Import Errors

```
ModuleNotFoundError: No module named 'chromadb'
```

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 💡 Customization Guide

### Add Your Own Documents

Replace the `SAMPLE_BLOGS` in `rag_demo.py`:

```python
SAMPLE_BLOGS = [
    {
        "title": "Your Blog Title",
        "date": "2024-11-19",
        "url": "https://your-blog-url.com",
        "content": """Your blog content here..."""
    },
    # Add more blogs...
]
```

### Adjust Chunk Size

Experiment with different sizes:

```python
# In rag_demo.py, modify chunk_documents call:
chunks = chunk_documents(SAMPLE_BLOGS, chunk_size=300, chunk_overlap=30)  # Smaller chunks
chunks = chunk_documents(SAMPLE_BLOGS, chunk_size=600, chunk_overlap=100) # Larger chunks
```

**Guidelines:**
- Smaller chunks (200-300): Better for precise, specific queries
- Larger chunks (500-700): Better for context-heavy queries
- Test with your use case!

### Change Number of Retrieved Chunks

```python
# Retrieve more context
result = rag_query(question, k=10)  # Instead of default k=5
```

**Trade-offs:**
- More chunks = more context, but slower and more expensive
- Fewer chunks = faster, but might miss relevant info

### Switch Vector Database

To use Vertex AI Vector Search instead of ChromaDB:

```python
# See: https://cloud.google.com/vertex-ai/docs/vector-search/quickstart

from google.cloud import aiplatform

# Create index
index = aiplatform.MatchingEngineIndex.create_tree_ah_index(...)

# Deploy index
endpoint = aiplatform.MatchingEngineIndexEndpoint.create(...)
endpoint.deploy_index(index=index, ...)

# Query
results = endpoint.match(
    deployed_index_id=deployed_index_id,
    queries=[query_embedding],
    num_neighbors=5
)
```

## 📊 Cost Estimation

### Vertex AI Pricing (as of Nov 2024)

**Embeddings (text-embedding-004):**
- $0.00002 per 1,000 characters
- Example: 50,000 characters = $0.001

**Gemini 1.5 Flash:**
- Input: $0.00001875 per 1,000 characters
- Output: $0.000075 per 1,000 characters

**Typical Session 3 Demo Costs:**
- Initial indexing (5 blogs, ~25,000 chars): $0.0005
- Per query (with 5 chunks context): $0.0001 - $0.0005
- **Total for demo: < $0.01**

### ChromaDB
- Free for local use
- Memory-only, no cloud costs

## 🎯 Homework Guide

### Phase 1: Data Collection (Day 1-2)

**Option A: Web Scraping**
```python
import requests
from bs4 import BeautifulSoup

def scrape_wcc_blog(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract title, date, content
    # Return structured data
```

**Option B: Manual Collection**
- Copy 10-20 blog posts manually
- Save as JSON or text files
- Include metadata (title, date, URL)

### Phase 2: Build Pipeline (Day 3-4)

1. Modify `rag_demo.py` with your data
2. Run chunking and embedding generation
3. Test semantic search thoroughly
4. Debug any issues

### Phase 3: Add RAG (Day 5-6)

1. Implement RAG query function
2. Test with various questions
3. Build Streamlit UI
4. Add error handling

### Phase 4: Experiment (Day 7)

Test variations:
- Chunk size: 200 vs 400 vs 600 tokens
- Number of chunks: k=3 vs k=5 vs k=10
- Different prompts
- Edge cases and out-of-scope questions

Document your findings!

## 📝 Submission Checklist

- [ ] Working code on GitHub
- [ ] README with:
  - [ ] What you built
  - [ ] How many documents indexed
  - [ ] Example queries and results
  - [ ] Challenges faced
  - [ ] Optimal chunk size for your use case
- [ ] At least 3 test queries with outputs
- [ ] Screenshots of your UI
- [ ] (Optional) Demo video

## 🔗 Resources

### Official Documentation
- [Vertex AI Embeddings](https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-text-embeddings)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [LangChain Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)

### Tutorials
- [Google Cloud RAG Tutorial](https://cloud.google.com/vertex-ai/docs/generative-ai/rag-overview)
- [ChromaDB Quickstart](https://docs.trychroma.com/getting-started)

### Community
- WCC Slack: #ai-learning-series
- Office Hours: Thursday 6pm GMT
- GitHub Discussions: [Link to repo]

## 🎓 What You've Learned

By completing this demo, you now understand:

✅ **Embeddings**: How text becomes mathematical vectors  
✅ **Vector Databases**: Storing and searching embeddings efficiently  
✅ **Semantic Search**: Finding meaning, not just keywords  
✅ **RAG Architecture**: Retrieval → Augmentation → Generation  
✅ **Production Patterns**: Chunking strategies, error handling, source attribution

## 🚀 Next Steps

- **Session 4**: Build AI Agents that use RAG as a tool
- **Session 7**: Advanced RAG (hybrid search, re-ranking, query transformation)
- **Session 8**: GraphRAG - Combining knowledge graphs with RAG

Keep building! 🎉
