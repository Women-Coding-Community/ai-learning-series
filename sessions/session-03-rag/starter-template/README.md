# Starter Template: RAG Pipeline

Build your own RAG system. Start here, then pick a use case from [use-case-guides/](../use-case-guides/).

## Setup (5 min)

```bash
pip install -r requirements.txt
gcloud auth application-default login
```

## Core RAG Pipeline

Use `rag_pipeline.py` as your foundation:

```python
from rag_pipeline import RAGPipeline

# Initialize
rag = RAGPipeline(project_id="your-gcp-project-id")

# 1. Load and chunk documents
documents = [
    {"title": "Doc 1", "content": "..."},
    {"title": "Doc 2", "content": "..."}
]
rag.chunk_documents(documents, chunk_size=400)

# 2. Generate embeddings and store
rag.embed_and_store()

# 3. Search
results = rag.search("Your question here", k=5)

# 4. Get RAG answer
answer = rag.query("Your question here")
print(answer['answer'])
print(answer['sources'])
```

## Customization

### Change Chunk Size

```python
rag.chunk_documents(documents, chunk_size=200)  # Smaller
rag.chunk_documents(documents, chunk_size=800)  # Larger
```

### Adjust Number of Retrieved Results

```python
results = rag.search(query, k=3)   # Top 3
results = rag.search(query, k=10)  # Top 10
```

### Use Different LLM

```python
rag.generation_model = GenerativeModel("gemini-1.5-pro")
```

## Next Steps

1. Choose a use case: [Blog Search](../use-case-guides/wcc-blog-search.md) | [Event Archive](../use-case-guides/event-archive-qa.md) | [Mentorship KB](../use-case-guides/mentorship-kb.md)
2. Collect your data (10-20 documents)
3. Follow the use case guide
4. Experiment with chunk sizes
5. Submit to `participants/[your-username]/`

## Resources

- [Live Demo](../live-demo/README.md) - Full working example
- [Vertex AI Embeddings](https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-text-embeddings)
- [ChromaDB Docs](https://docs.trychroma.com/)

---

Happy coding! 🚀
