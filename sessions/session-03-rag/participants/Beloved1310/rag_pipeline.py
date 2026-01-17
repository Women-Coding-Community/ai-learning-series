"""
WCC AI Learning Series - Session 3: Event Archive RAG Pipeline
A RAG system for searching and querying WCC event history.

This implementation follows the starter template structure and adapts it
for event data with proper metadata handling (date, speaker, URL).
"""

import os
import csv
from typing import List, Dict
from dotenv import load_dotenv

# Import required libraries
import vertexai
from google import genai
from google.genai import types
import chromadb
from langchain_text_splitters.character import RecursiveCharacterTextSplitter


load_dotenv()


class EventArchiveRAG:
    """
    RAG Pipeline for WCC Event Archive
    
    This class implements a complete RAG system for searching past events:
    1. Load events from CSV
    2. Chunk: Break event descriptions into smaller pieces
    3. Embed: Convert text to vectors
    4. Store: Save vectors in a database
    5. Query: Retrieve relevant events and generate answers
    """
    
    def __init__(self, project_id: str, location: str = "us-central1"):
        """
        Initialize the Event Archive RAG pipeline
        
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
        self.collection_name = "wcc_events"
        try:
            self.collection = self.chroma_client.get_collection(self.collection_name)
            print(f"✓ Using existing collection: {self.collection_name}")
        except:
            self.collection = self.chroma_client.create_collection(self.collection_name)
            print(f"✓ Created new collection: {self.collection_name}")
        
        # Store documents for reference
        self.documents = []
        self.chunks = []
    
    # ========================================================================
    # DATA LOADING
    # ========================================================================
    
    def load_events_from_csv(self, csv_path: str) -> List[Dict]:
        """
        Load events from CSV file and convert to document format
        
        Args:
            csv_path: Path to the events CSV file
            
        Returns:
            List of event documents with metadata
        """
        print("\n" + "="*70)
        print("LOADING EVENTS FROM CSV")
        print("="*70)
        
        documents = []
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Create content with title, speaker, and description
                    content = f"{row['title']}\nSpeaker: {row['speaker']}\n{row['description']}"
                    
                    documents.append({
                        "title": row['title'],
                        "date": row['date'],
                        "speaker": row['speaker'],
                        "url": row['url'],
                        "content": content
                    })
            
            self.documents = documents
            print(f"✓ Loaded {len(documents)} events from {csv_path}")
            
            return documents
            
        except FileNotFoundError:
            print(f"❌ Error: CSV file not found at {csv_path}")
            return []
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            return []
    
    # ========================================================================
    # STEP 1: CHUNKING
    # ========================================================================
    
    def chunk_documents(self, documents: List[Dict] = None, chunk_size: int = 500, 
                       chunk_overlap: int = 50) -> List[Dict]:
        """
        STEP 1: Break event documents into smaller chunks
        
        Why? Large event descriptions don't fit well in embeddings.
        Smaller chunks = better retrieval for specific questions.
        
        Args:
            documents: List of event dicts (uses self.documents if None)
            chunk_size: Size of each chunk (in characters)
            chunk_overlap: Overlap between chunks (for context)
        
        Returns:
            List of chunks with metadata
        """
        print("\n" + "="*70)
        print("STEP 1: CHUNKING DOCUMENTS")
        print("="*70)
        
        if documents is None:
            documents = self.documents
        
        if not documents:
            print("❌ No documents to chunk. Load events first!")
            return []
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len,
        )
        
        all_chunks = []
        
        for doc in documents:
            # Use the content (title + speaker + description)
            full_text = doc['content']
            
            # Split into chunks
            chunks = text_splitter.split_text(full_text)
            
            # Add metadata to each chunk
            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    "text": chunk,
                    "metadata": {
                        "title": doc.get("title", "Unknown"),
                        "date": doc.get("date", "Unknown"),
                        "speaker": doc.get("speaker", "Unknown"),
                        "url": doc.get("url", ""),
                        "chunk_id": i,
                        "total_chunks": len(chunks)
                    }
                })
        
        self.chunks = all_chunks
        print(f"✓ Created {len(all_chunks)} chunks from {len(documents)} events")
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
        Vector DB lets us find similar event chunks quickly.
        
        Args:
            batch_size: Process this many chunks at once
        """
        print("\n" + "="*70)
        print("STEP 2: EMBEDDING & STORAGE")
        print("="*70)
        
        if not hasattr(self, 'chunks') or not self.chunks:
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
        STEP 3: Search for relevant event chunks
        
        Why? Find the most similar event chunks to the user's question.
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
    
    def query(self, question: str, k: int = 5, model: str = None) -> Dict:
        """
        STEP 4: Complete RAG - Retrieve context and generate answer
        
        Why? Combine retrieved event chunks with an LLM to generate answers.
        This is the full RAG pipeline!
        
        Args:
            question: User's question
            k: Number of context chunks to retrieve
            model: Which Gemini model to use (defaults to self.generation_model_name)
        
        Returns:
            Dict with 'answer' and 'sources'
        """
        print("\n" + "="*70)
        print("STEP 4: GENERATING ANSWER (RAG)")
        print("="*70)
        
        if model is None:
            model = self.generation_model_name
        
        # 1. Search for relevant chunks
        relevant_docs = self.search(question, k=k)
        
        if not relevant_docs:
            return {
                'answer': "I couldn't find any relevant events to answer that question.",
                'sources': []
            }
        
        # 2. Build context from retrieved chunks
        context_parts = []
        for i, doc in enumerate(relevant_docs):
            context_parts.append(f"""[Source {i+1}: {doc['metadata']['title']}]
Date: {doc['metadata']['date']}
Speaker: {doc['metadata']['speaker']}
{doc['text']}
""")
        
        context = "\n\n".join(context_parts)
        
        # 3. Build prompt
        prompt = f"""You are a helpful assistant for the Women Coding Community (WCC) Event Archive.
Answer the question based ONLY on the provided context about past WCC events.
If the context doesn't contain enough information, say so.
Always cite your sources using [Source X] format and include event dates and speakers when relevant.

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
                unique_sources.append({
                    'title': doc['metadata']['title'],
                    'date': doc['metadata']['date'],
                    'speaker': doc['metadata']['speaker'],
                    'url': doc['metadata']['url']
                })
        
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
        self.documents = []
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
        print(f"Loaded events: {len(self.documents)}")
        if hasattr(self, 'chunks'):
            print(f"Loaded chunks: {len(self.chunks)}")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # 1. Initialize
    project_id = os.getenv("PROJECT_ID") or os.getenv("GCP_PROJECT_ID")
    location = os.getenv("LOCATION", "us-central1")
    
    if not project_id:
        print("❌ Error: PROJECT_ID or GCP_PROJECT_ID not found in environment variables")
        exit(1)
    
    rag = EventArchiveRAG(project_id=project_id, location=location)
    
    # 2. Load events from CSV
    csv_path = "data/events.csv"
    rag.load_events_from_csv(csv_path)
    
    # 3. Run the pipeline
    print("\n🚀 Starting Event Archive RAG Pipeline\n")
    
    # Step 1: Chunk
    rag.chunk_documents(chunk_size=500)
    
    # Step 2: Embed & Store
    rag.embed_and_store()
    
    # Step 3: Test Search
    print("\n" + "="*70)
    print("TESTING SEARCH")
    print("="*70)
    results = rag.search("What Python events did WCC host?", k=5)
    for r in results:
        print(f"  - {r['metadata']['title']} ({r['metadata']['date']})")
    
    # Step 4: Full RAG
    print("\n" + "="*70)
    print("TESTING FULL RAG")
    print("="*70)
    result = rag.query("What Python events did WCC host?")
    print("\n💬 Answer:")
    print(result['answer'])
    print("\n📚 Sources:")
    for source in result['sources']:
        print(f"  - {source['title']} ({source['date']})")
        print(f"    Speaker: {source['speaker']}")
    
    # Show status
    rag.status()

