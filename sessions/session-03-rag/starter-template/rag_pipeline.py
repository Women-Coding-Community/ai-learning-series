"""
WCC AI Learning Series - Session 3: Simple RAG Pipeline Starter
A beginner-friendly RAG implementation to learn the core concepts.

This is a simplified version of the full demo. Perfect for:
- Understanding RAG step-by-step
- Building your own RAG system
- Experimenting with different data
"""

import os
from typing import List, Dict
from dotenv import load_dotenv

# Import required libraries
import vertexai
from google import genai
from google.genai import types
import chromadb
from langchain_text_splitters.character import RecursiveCharacterTextSplitter


load_dotenv()

# Set your GCP project ID
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION", "us-central1")

class RAGPipeline:
    """
    Simple RAG Pipeline - Learn the 4 core steps:
    1. Chunk: Break documents into smaller pieces
    2. Embed: Convert text to vectors
    3. Store: Save vectors in a database
    4. Query: Retrieve relevant chunks and generate answers
    """
    
    def __init__(self, project_id: str, location: str = "us-central1"):
        """
        Initialize the RAG pipeline
        
        Args:
            project_id: Your GCP project ID
            location: GCP region (default: us-central1)
        """
        self.project_id = project_id
        self.location = location
        
        # Initialize Vertex AI and Generative AI client
        vertexai.init(project=project_id, location=location)
        
        # Initialize clients
        self.client = genai.Client(
            vertexai=True, project=project_id, location=location)
        
        # Model names from environment or defaults
        self.embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-004")
        self.generation_model_name = os.getenv("GENERATION_MODEL_NAME", "gemini-2.5-flash-lite")
        
        # Initialize ChromaDB (local, persistent storage)
        self.chroma_client = chromadb.PersistentClient(path="./chroma_data")
        
        # Create or get collection
        self.collection_name = "my_documents"
        try:
            self.collection = self.chroma_client.get_collection(self.collection_name)
            print(f"✓ Using existing collection: {self.collection_name}")
        except:
            self.collection = self.chroma_client.create_collection(self.collection_name)
            print(f"✓ Created new collection: {self.collection_name}")
        
        # Store documents for reference
        self.documents = []
    
    # ========================================================================
    # STEP 1: CHUNKING
    # ========================================================================
    
    def chunk_documents(self, documents: List[Dict], chunk_size: int = 400, 
                       chunk_overlap: int = 50) -> List[Dict]:
        """
        STEP 1: Break documents into smaller chunks
        
        Why? Large documents don't fit well in embeddings.
        Smaller chunks = better retrieval.
        
        Args:
            documents: List of dicts with 'title' and 'content'
            chunk_size: Size of each chunk (in characters)
            chunk_overlap: Overlap between chunks (for context)
        
        Returns:
            List of chunks with metadata
        """
        print("\n" + "="*70)
        print("STEP 1: CHUNKING DOCUMENTS")
        print("="*70)
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len,
        )
        
        all_chunks = []
        
        for doc in documents:
            # Combine title and content
            full_text = f"Title: {doc['title']}\n\n{doc['content']}"
            
            # Split into chunks
            chunks = text_splitter.split_text(full_text)
            
            # Add metadata to each chunk
            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    "text": chunk,
                    "metadata": {
                        "title": doc.get("title", "Unknown"),
                        "source": doc.get("source", "Unknown"),
                        "chunk_id": i,
                        "total_chunks": len(chunks)
                    }
                })
        
        self.chunks = all_chunks
        print(f"✓ Created {len(all_chunks)} chunks from {len(documents)} documents")
        print(f"  Chunk size: {chunk_size} characters")
        print(f"  Chunk overlap: {chunk_overlap} characters")
        
        return all_chunks
    
    # ========================================================================
    # STEP 2: EMBEDDING & STORAGE
    # ========================================================================
    
    def embed_and_store(self, batch_size: int = 5) -> None:
        """
        STEP 2: Generate embeddings and store in vector database
        
        Why? Embeddings convert text to numbers that capture meaning.
        Vector DB lets us find similar chunks quickly.
        
        Args:
            batch_size: Process this many chunks at once
        """
        print("\n" + "="*70)
        print("STEP 2: EMBEDDING & STORAGE")
        print("="*70)
        
        if not hasattr(self, 'chunks'):
            print("❌ No chunks found. Run chunk_documents() first!")
            return
        
        # Extract texts
        texts = [chunk["text"] for chunk in self.chunks]
        
        print(f"Generating embeddings for {len(texts)} chunks...")
        
        all_embeddings = []
        
        # Process in batches
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            
            # Get embeddings from Vertex AI
            response = self.client.models.embed_content(
                model=self.embedding_model_name,
                contents=batch,
                config=types.EmbedContentConfig(output_dimensionality=10),
            )
            
            batch_embeddings = [emb.values for emb in response.embeddings]
            all_embeddings.extend(batch_embeddings)
            
            if (i + batch_size) % 10 == 0:
                print(f"  Processed {min(i+batch_size, len(texts))}/{len(texts)} chunks")
        
        # Store in ChromaDB
        ids = [f"chunk_{i}" for i in range(len(self.chunks))]
        documents = [chunk["text"] for chunk in self.chunks]
        metadatas = [chunk["metadata"] for chunk in self.chunks]
        
        self.collection.add(
            embeddings=all_embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✓ Stored {len(self.chunks)} chunks in vector database")
        print(f"  Embedding dimension: {len(all_embeddings[0])}")
        print(f"  Collection size: {self.collection.count()}")
    
    # ========================================================================
    # STEP 3: SEMANTIC SEARCH
    # ========================================================================
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """
        STEP 3: Search for relevant chunks
        
        Why? Find the most similar chunks to the user's question.
        This is "retrieval" - the R in RAG.
        
        Args:
            query: User's question or search term
            k: Number of results to return
        
        Returns:
            List of relevant chunks with similarity scores
        """
        print(f"\n🔍 Searching for: {query}")
        
        # Embed the query
        response = self.client.models.embed_content(
            model=self.embedding_model_name,
            contents=[query],
            config=types.EmbedContentConfig(output_dimensionality=10),
        )
        query_embedding = response.embeddings[0].values
        
        # Search the vector database
        results = self.collection.query(
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
        
        print(f"✓ Found {len(relevant_docs)} relevant chunks")
        
        return relevant_docs
    
    # ========================================================================
    # STEP 4: GENERATION (RAG)
    # ========================================================================
    
    def query(self, question: str, k: int = 5, model: str = "gemini-2.5-flash-lite") -> Dict:
        """
        STEP 4: Complete RAG - Retrieve context and generate answer
        
        Why? Combine retrieved chunks with an LLM to generate answers.
        This is the full RAG pipeline!
        
        Args:
            question: User's question
            k: Number of context chunks to retrieve
            model: Which Gemini model to use
        
        Returns:
            Dict with 'answer' and 'sources'
        """
        print("\n" + "="*70)
        print("STEP 4: GENERATING ANSWER (RAG)")
        print("="*70)
        
        # 1. Search for relevant chunks
        relevant_docs = self.search(question, k=k)
        
        if not relevant_docs:
            return {
                'answer': "I couldn't find any relevant information.",
                'sources': []
            }
        
        # 2. Build context from retrieved chunks
        context_parts = []
        for i, doc in enumerate(relevant_docs):
            context_parts.append(f"""[Source {i+1}: {doc['metadata']['title']}]
{doc['text']}
""")
        
        context = "\n\n".join(context_parts)
        
        # 3. Build prompt
        prompt = f"""Answer the question based ONLY on the provided context.
If the context doesn't contain enough information, say so.
Always cite your sources using [Source X] format.

Context:
{context}

Question: {question}

Answer:"""
        
        # 4. Generate answer with Gemini
        print("🤖 Generating answer with Gemini...")
        
        response = self.client.models.generate_content(
            model=model,
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
            'chunks': relevant_docs
        }
    
    # ========================================================================
    # UTILITIES
    # ========================================================================
    
    def reset(self) -> None:
        """Clear all stored documents and start fresh"""
        self.chroma_client.delete_collection(self.collection_name)
        self.collection = self.chroma_client.create_collection(self.collection_name)
        self.chunks = []
        print("✓ Collection reset")
    
    def status(self) -> None:
        """Show current status"""
        print("\n" + "="*70)
        print("PIPELINE STATUS")
        print("="*70)
        print(f"Project ID: {self.project_id}")
        print(f"Location: {self.location}")
        print(f"Collection: {self.collection_name}")
        print(f"Stored chunks: {self.collection.count()}")
        if hasattr(self, 'chunks'):
            print(f"Loaded chunks: {len(self.chunks)}")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # 1. Initialize
    rag = RAGPipeline(project_id=os.getenv("GCP_PROJECT_ID"), location=os.getenv("GCP_LOCATION"))
    
    # 2. Sample documents
    sample_docs = [
        {
            "title": "Python Basics",
            "source": "WCC Blog",
            "content": """
Python is a versatile programming language. It's great for beginners because:
- Clean, readable syntax
- Powerful libraries
- Used by tech giants like Google and Netflix

Getting started:
1. Install Python 3.9+
2. Use VS Code or PyCharm
3. Write your first program: print("Hello, World!")
            """
        },
        {
            "title": "Web Development with Django",
            "source": "WCC Workshop",
            "content": """
Django is a Python web framework. It provides:
- Models for database management
- Views for business logic
- Templates for HTML rendering

Key concepts:
- MVT pattern (Models, Views, Templates)
- ORM for database queries
- Built-in admin interface
            """
        }
    ]
    
    # 3. Run the pipeline
    print("\n🚀 Starting RAG Pipeline Demo\n")
    
    # Step 1: Chunk
    rag.chunk_documents(sample_docs, chunk_size=200)
    
    # Step 2: Embed & Store
    rag.embed_and_store()
    
    # Step 3: Search
    rag.search("How do I learn Python?", k=2)
    
    # Step 4: Full RAG
    result = rag.query("What are the benefits of using Django?")
    print("\n💬 Answer:")
    print(result['answer'])
    print("\n📚 Sources:")
    for source in result['sources']:
        print(f"  - {source['title']}")
    
    # Show status
    rag.status()
