"""
WCC AI Learning Series - Session 3: RAG Demo
Complete RAG Pipeline Implementation

This demo shows:
1. Document chunking
2. Embedding generation with Vertex AI
3. Storage in ChromaDB
4. Semantic search
5. RAG with Gemini
"""

import os
import chromadb
import vertexai
from typing import List, Dict
from google import genai
from google.genai import types
from chromadb.config import Settings
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from sample_data import SAMPLE_BLOGS

# ============================================================================
# CONFIGURATION
# ============================================================================

load_dotenv()

# Set your GCP project ID
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")

# Initialize Vertex AI and Generative AI client
vertexai.init(project=PROJECT_ID, location=LOCATION)
client = genai.Client(
    vertexai=True, project=PROJECT_ID, location=LOCATION)

# Initialize models
GENERATION_MODEL_NAME = os.getenv("GENERATION_MODEL_NAME", "gemini-2.5-flash-lite")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-004")

# Initialize ChromaDB (local, persistent storage)
chroma_client = chromadb.Client(Settings(
    anonymized_telemetry=False,
    allow_reset=True
))

# Create or get collection
collection_name = "wcc_blogs"
try:
    collection = chroma_client.get_collection(collection_name)
    print(f"✓ Using existing collection: {collection_name}")
except:
    collection = chroma_client.create_collection(collection_name)
    print(f"✓ Created new collection: {collection_name}")


# ============================================================================
# STEP 1: CHUNKING DOCUMENTS
# ============================================================================

def chunk_documents(blogs: List[Dict], chunk_size: int = 400, chunk_overlap: int = 50) -> List[Dict]:
    """
    Chunk blog posts into smaller pieces with metadata
    
    Args:
        blogs: List of blog post dictionaries
        chunk_size: Target size for each chunk in tokens (~chars)
        chunk_overlap: Number of characters to overlap between chunks
    
    Returns:
        List of document chunks with metadata
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )
    
    all_chunks = []
    
    for blog in blogs:
        # Create a combined text with title and content
        full_text = f"Title: {blog['title']}\n\n{blog['content']}"
        
        # Split into chunks
        chunks = text_splitter.split_text(full_text)
        
        # Add metadata to each chunk
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "metadata": {
                    "title": blog["title"],
                    "date": blog["date"],
                    "url": blog["url"],
                    "chunk_id": i,
                    "total_chunks": len(chunks)
                }
            })
    
    return all_chunks

# ============================================================================
# STEP 2: GENERATE EMBEDDINGS
# ============================================================================

def generate_embeddings(texts: List[str], batch_size: int = 5) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using Vertex AI
    
    Args:
        texts: List of text strings to embed
        batch_size: Number of texts to process at once
    
    Returns:
        List of embeddings (each embedding is a list of floats)
    """
    all_embeddings = []
    
    print(f"Generating embeddings for {len(texts)} chunks...")
    
    # Process in batches to avoid rate limits
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        
        # Get embeddings for this batch
        response = client.models.embed_content(
            model=EMBEDDING_MODEL_NAME,
            contents=batch,
            config=types.EmbedContentConfig(output_dimensionality=10),
        )
        
        # Extract the values (list of floats) from each embedding
        batch_embeddings = [emb.values for emb in response.embeddings]
        all_embeddings.extend(batch_embeddings)
        
        # Progress update
        if (i + batch_size) % 10 == 0:
            print(f"  Processed {min(i+batch_size, len(texts))}/{len(texts)} chunks")
    
    print(f"✓ Generated {len(all_embeddings)} embeddings")
    print(f"  Embedding dimension: {len(all_embeddings[0])}")
    
    return all_embeddings

# ============================================================================
# STEP 3: STORE IN CHROMADB
# ============================================================================

def store_in_vectordb(chunks: List[Dict], embeddings: List[List[float]]) -> None:
    """
    Store chunks, embeddings, and metadata in ChromaDB
    
    Args:
        chunks: List of document chunks with metadata
        embeddings: List of embeddings corresponding to chunks
    """
    # Prepare data for ChromaDB
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    
    # Add to collection
    collection.add(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"✓ Stored {len(chunks)} chunks in ChromaDB")
    print(f"  Collection size: {collection.count()}")

# ============================================================================
# STEP 4: SEMANTIC SEARCH
# ============================================================================

def semantic_search(query: str, k: int = 5) -> List[Dict]:
    """
    Search for relevant chunks given a query
    
    Args:
        query: User's search query
        k: Number of results to return
    
    Returns:
        List of relevant documents with metadata and scores
    """
    # Embed the query
    response = client.models.embed_content(
            model=EMBEDDING_MODEL_NAME,
            contents=[query],
            config=types.EmbedContentConfig(output_dimensionality=10),
        )
    query_embedding = response.embeddings[0].values
    
    # Search the vector database
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    
    # Format results
    relevant_docs = []
    if results['documents'] and len(results['documents'][0]) > 0:
        for i in range(len(results['documents'][0])):
            relevant_docs.append({
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]  # Lower = more similar
            })
    
    return relevant_docs

# ============================================================================
# STEP 5: RAG PIPELINE
# ============================================================================

def rag_query(question: str, k: int = 5, verbose: bool = False) -> Dict:
    """
    Complete RAG pipeline: retrieve relevant context and generate answer
    
    Args:
        question: User's question
        k: Number of context chunks to retrieve
        verbose: Whether to print detailed information
    
    Returns:
        Dictionary with answer, sources, and retrieved chunks
    """
    # 1. Search for relevant chunks
    if verbose:
        print(f"\n🔍 Searching for: {question}")
    
    relevant_docs = semantic_search(question, k=k)
    
    if not relevant_docs:
        return {
            'answer': "I couldn't find any relevant information to answer that question.",
            'sources': [],
            'chunks': []
        }
    
    if verbose:
        print(f"✓ Found {len(relevant_docs)} relevant chunks")
        for i, doc in enumerate(relevant_docs):
            print(f"  [{i+1}] {doc['metadata']['title']} (distance: {doc['distance']:.3f})")
    
    # 2. Build context from retrieved chunks
    context_parts = []
    for i, doc in enumerate(relevant_docs):
        context_parts.append(f"""[Source {i+1}: {doc['metadata']['title']}]
{doc['text']}
""")
    
    context = "\n\n".join(context_parts)
    
    # 3. Build prompt for LLM
    prompt = f"""You are a helpful assistant for the Women Coding Community (WCC).
Answer the question based ONLY on the provided context below.
If the context doesn't contain enough information to answer the question, say so.
Always cite your sources using the format [Source X] where X is the source number.

Context:
{context}

Question: {question}

Answer (with citations):"""
    
    # 4. Generate answer with Gemini
    if verbose:
        print("🤖 Generating answer with Gemini...")
    
    response = client.models.generate_content(
        model=GENERATION_MODEL_NAME,
        contents=[prompt],
        config=types.GenerateContentConfig()
    )
    
    # 5. Extract unique sources
    unique_sources = []
    seen_titles = set()
    for doc in relevant_docs:
        title = doc['metadata']['title']
        if title not in seen_titles:
            seen_titles.add(title)
            unique_sources.append(doc['metadata'])
    
    return {
        'answer': response.text,
        'sources': unique_sources,
        'chunks': relevant_docs  # Include for debugging
    }

# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

def demo_setup():
    """Run the complete RAG setup process"""
    print("\n" + "="*70)
    print("WCC RAG SYSTEM SETUP")
    print("="*70)
    
    # Step 1: Chunk documents
    print("\n📄 STEP 1: Chunking Documents")
    print("-" * 70)
    chunks = chunk_documents(SAMPLE_BLOGS)
    print(f"✓ Created {len(chunks)} chunks from {len(SAMPLE_BLOGS)} blog posts")
    print(f"  First chunk preview: {chunks[0]['text'][:100]}...")
    
    # Step 2: Generate embeddings
    print("\n🧮 STEP 2: Generating Embeddings")
    print("-" * 70)
    texts = [chunk["text"] for chunk in chunks]
    embeddings = generate_embeddings(texts)
    
    # Step 3: Store in vector database
    print("\n💾 STEP 3: Storing in ChromaDB")
    print("-" * 70)
    store_in_vectordb(chunks, embeddings)
    
    print("\n✅ Setup complete! Ready for queries.")
    print("="*70)

def demo_search():
    """Demo semantic search functionality"""
    print("\n" + "="*70)
    print("SEMANTIC SEARCH DEMO")
    print("="*70)
    
    # Test queries
    test_queries = [
        "How do I start learning Python?",
        "What events did WCC host about web development?",
        "Tell me about mentorship at WCC"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        print("-" * 70)
        
        results = semantic_search(query, k=3)
        
        for i, result in enumerate(results):
            print(f"\n  Result {i+1}:")
            print(f"  Title: {result['metadata']['title']}")
            print(f"  Distance: {result['distance']:.3f} (lower = more similar)")
            print(f"  Preview: {result['text'][:150]}...")

def demo_rag():
    """Demo complete RAG pipeline"""
    print("\n" + "="*70)
    print("RAG PIPELINE DEMO")
    print("="*70)
    
    # Test questions
    test_questions = [
        "What Python topics has WCC covered?",
        "How can I transition from backend to AI engineering?",
        "What advice do you have for mentees?",
        "What cloud platforms were discussed?"
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        print("-" * 70)
        
        result = rag_query(question, k=3, verbose=True)
        
        print(f"\n💬 Answer:")
        print(result['answer'])
        
        print(f"\n📚 Sources:")
        for source in result['sources']:
            print(f"  • {source['title']}")
            print(f"    {source['url']}")
        
        print("\n" + "-" * 70)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import sys
    
    print("\n🎓 WCC AI Learning Series - Session 3: RAG Demo")
    print("=" * 70)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--reset":
            print("\n🔄 Resetting collection...")
            chroma_client.delete_collection(collection_name)
            collection = chroma_client.create_collection(collection_name)
            demo_setup()
        elif sys.argv[1] == "--search":
            demo_search()
        elif sys.argv[1] == "--rag":
            demo_rag()
        elif sys.argv[1] == "--all":
            demo_setup()
            input("\n⏩ Press Enter to run the semantic search demo...")
            demo_search()
            input("\n⏩ Press Enter to run the full RAG pipeline demo...")
            demo_rag()
    else:
        # Default behavior: check status and auto-setup if needed
        if collection.count() == 0:
            print("\n⚠️  Collection is empty. Running setup...")
            demo_setup()
        else:
            print(f"\n✓ Collection already contains {collection.count()} documents")
            print("  (Use '--reset' to clear and re-setup)")
        
        print("\n💡 Usage:")
        print("  python rag_demo.py           # Check status")
        print("  python rag_demo.py --reset   # Reset and re-setup")
        print("  python rag_demo.py --search  # Demo search")
        print("  python rag_demo.py --rag     # Demo RAG pipeline")
        print("  python rag_demo.py --all     # Run all demos")
        print("\nFor interactive use, see: streamlit_app.py")
