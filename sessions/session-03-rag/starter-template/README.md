# Starter Template: RAG Pipeline

A beginner-friendly RAG implementation to learn the core concepts and build your own system.

## Quick Start (10 min)

### 1. Setup

```bash
pip install -r requirements.txt
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Create `.env` file

```env
PROJECT_ID=your-gcp-project-id
LOCATION=us-central1
GENERATION_MODEL_NAME=gemini-2.5-flash-lite
```

### 3. Run the example

```bash
python rag_pipeline.py
```

## Understanding RAG: The 4 Steps

The `RAGPipeline` class breaks RAG into 4 simple steps:

### Step 1: Chunking
Break large documents into smaller pieces for better retrieval.

```python
rag.chunk_documents(documents, chunk_size=400, chunk_overlap=50)
```

### Step 2: Embedding & Storage
Convert text to vectors and store in a local database.

```python
rag.embed_and_store()
```

### Step 3: Search
Find the most relevant chunks for a query.

```python
results = rag.search("Your question here", k=5)
```

### Step 4: Generation (Full RAG)
Combine retrieved chunks with an LLM to generate answers.

```python
answer = rag.query("Your question here")
print(answer['answer'])
print(answer['sources'])
```

## Complete Example

```python
from rag_pipeline import RAGPipeline
import os

# Initialize
rag = RAGPipeline(project_id=os.getenv("PROJECT_ID"))

# Your documents
documents = [
    {
        "title": "Python Basics",
        "source": "WCC Blog",
        "content": "Python is a versatile programming language..."
    },
    {
        "title": "Web Development",
        "source": "WCC Workshop",
        "content": "Django is a Python web framework..."
    }
]

# Run the pipeline
rag.chunk_documents(documents, chunk_size=200)
rag.embed_and_store()

# Ask questions
result = rag.query("How do I learn Python?")
print(result['answer'])
```

## Customization

### Adjust Chunk Size

```python
# Smaller chunks = more specific retrieval
rag.chunk_documents(documents, chunk_size=200)

# Larger chunks = more context
rag.chunk_documents(documents, chunk_size=800)
```

### Change Number of Retrieved Results

```python
# Get top 3 most relevant chunks
results = rag.search(query, k=3)

# Get top 10
results = rag.search(query, k=10)
```

### Use Different Gemini Model

```python
# Use a more powerful model
result = rag.query("Your question", model="gemini-1.5-pro")
```

## Utilities

```python
# Check status
rag.status()

# Clear everything and start fresh
rag.reset()
```

## Next Steps

1. **Understand the code**: Read through `rag_pipeline.py` - it's heavily commented!
2. **Experiment**: Try different chunk sizes, models, and documents
3. **Build your own**: Use this as a template for your data
4. **Explore use cases**: Check [use-case-guides/](../use-case-guides/) for real-world examples
5. **Compare approaches**: See the [full demo](../live-demo/) for production patterns

## Key Concepts

| Concept | What it does | Why it matters |
|---------|-------------|----------------|
| **Chunking** | Breaks documents into pieces | Smaller pieces = better retrieval |
| **Embedding** | Converts text to vectors | Enables semantic search |
| **Vector DB** | Stores and searches vectors | Fast similarity matching |
| **Retrieval** | Finds relevant chunks | Provides context for LLM |
| **Generation** | LLM creates answer | Combines context with reasoning |

## Troubleshooting

**"No module named 'google'"**
```bash
pip install --upgrade google-generativeai google-genai
```

**"Project not found"**
Make sure `PROJECT_ID` in `.env` matches your GCP project.

**"API not enabled"**
Enable Vertex AI API in your GCP project console.

## Resources

- [Live Demo](../live-demo/README.md) - Full working example with Streamlit
- [Vertex AI Docs](https://cloud.google.com/vertex-ai/docs)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Gemini API](https://ai.google.dev/)

---

**Happy learning! 🚀**

Questions? Check the [live-demo](../live-demo/) for more examples or ask in the WCC Slack!
