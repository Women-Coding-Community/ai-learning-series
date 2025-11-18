"""
WCC AI Learning Series - Session 3: Quick Vertex AI RAG Demo

This is a simplified demo using Vertex AI's managed RAG capabilities.
Use this if you're short on time and want to demo the Vertex AI RAG feature directly.

For production use cases, Vertex AI provides a managed RAG service that handles:
- Automatic document ingestion
- Embedding generation
- Vector storage
- Retrieval and generation

This demo shows the concept using Gemini with manually retrieved context.
"""

import vertexai
from vertexai.generative_models import GenerativeModel, Part
from vertexai.language_models import TextEmbeddingModel

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ID = "your-project-id"  # TODO: Update this
LOCATION = "us-central1"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Initialize models
embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
generation_model = GenerativeModel("gemini-1.5-flash")

# ============================================================================
# SAMPLE KNOWLEDGE BASE (Simplified)
# ============================================================================

KNOWLEDGE_BASE = {
    "Python Basics": """
    WCC regularly hosts Python workshops. Our Introduction to Python workshop covers:
    - Variables and data types
    - Functions and loops
    - File handling and error management
    - Building simple projects
    
    The workshop is beginner-friendly and includes hands-on coding exercises.
    Next session: November 2024. Sign up at womencodingcommunity.com
    """,
    
    "Django Workshop": """
    Our Django workshop taught participants to build web applications. 
    Sarah Chen led the session with 45 attendees. Topics covered:
    - MVT pattern (Models, Views, Templates)
    - User authentication
    - Database migrations
    - Deployment to Heroku
    
    Participants built a complete blog application with comments and search.
    All code is available at github.com/wcc/django-blog-workshop
    """,
    
    "Career Transitions": """
    WCC community members have successfully transitioned to AI engineering.
    Key advice:
    - Leverage your existing backend skills
    - Start with practical ML projects
    - Take online courses (Andrew Ng, fast.ai)
    - Build a portfolio of AI projects
    - Get cloud certifications (GCP ML Engineer, AWS ML Specialty)
    
    The transition typically takes 6-12 months of focused learning.
    """,
    
    "Mentorship Program": """
    WCC's mentorship program matches women in tech for 6-month mentorships.
    For mentees:
    - Set clear goals before starting
    - Come prepared to each session
    - Act on advice received
    - Stay in touch after the formal program
    
    Applications open quarterly at womencodingcommunity.com/mentorship
    Join #mentorship on Slack for questions.
    """,
    
    "Cloud Architecture": """
    Rachel Martinez from Google Cloud spoke at WCC about startup architecture.
    Key points:
    - Start simple, scale gradually
    - Use managed services (Cloud SQL, Cloud Run)
    - Implement Infrastructure as Code from day one
    - Set up monitoring and logging early
    - Optimize costs with auto-scaling and right-sizing
    
    Best for startups: stick with one cloud provider initially.
    """
}

# ============================================================================
# SIMPLE RAG FUNCTIONS
# ============================================================================

def simple_semantic_search(query: str, knowledge_base: dict, top_k: int = 3):
    """
    Simple semantic search using embeddings
    
    Args:
        query: User's search query
        knowledge_base: Dictionary of topic -> content
        top_k: Number of results to return
    
    Returns:
        List of (topic, content, similarity_score) tuples
    """
    # Get query embedding
    query_embedding = embedding_model.get_embeddings([query])[0].values
    
    # Calculate similarity for each document
    results = []
    for topic, content in knowledge_base.items():
        # Get document embedding
        doc_embedding = embedding_model.get_embeddings([content])[0].values
        
        # Calculate cosine similarity
        dot_product = sum(q * d for q, d in zip(query_embedding, doc_embedding))
        query_norm = sum(q * q for q in query_embedding) ** 0.5
        doc_norm = sum(d * d for d in doc_embedding) ** 0.5
        similarity = dot_product / (query_norm * doc_norm)
        
        results.append((topic, content, similarity))
    
    # Sort by similarity (highest first) and return top k
    results.sort(key=lambda x: x[2], reverse=True)
    return results[:top_k]

def vertex_ai_rag(question: str, top_k: int = 3):
    """
    Simple RAG pipeline using Vertex AI
    
    Args:
        question: User's question
        top_k: Number of context documents to retrieve
    
    Returns:
        Dictionary with answer and sources
    """
    print(f"\n🔍 Question: {question}")
    print("-" * 70)
    
    # 1. Retrieve relevant documents
    print("Retrieving relevant documents...")
    relevant_docs = simple_semantic_search(question, KNOWLEDGE_BASE, top_k=top_k)
    
    # 2. Build context
    context_parts = []
    sources = []
    
    for i, (topic, content, score) in enumerate(relevant_docs, 1):
        print(f"  ✓ Found: {topic} (similarity: {score:.3f})")
        context_parts.append(f"[Source {i}: {topic}]\n{content}\n")
        sources.append({"topic": topic, "score": score})
    
    context = "\n".join(context_parts)
    
    # 3. Build prompt
    prompt = f"""You are a helpful assistant for the Women Coding Community (WCC).

Answer the question based ONLY on the context provided below.
If the context doesn't contain enough information, say so honestly.
Always cite your sources using [Source X] format.

Context:
{context}

Question: {question}

Answer with citations:"""
    
    # 4. Generate answer
    print("\nGenerating answer with Gemini...")
    response = generation_model.generate_content(prompt)
    
    return {
        "answer": response.text,
        "sources": sources,
        "context": context
    }

# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

def demo_basic_search():
    """Demo basic semantic search without generation"""
    print("\n" + "="*70)
    print("DEMO 1: SEMANTIC SEARCH")
    print("="*70)
    
    queries = [
        "How do I learn Python?",
        "Tell me about web development",
        "Career advice for AI transition"
    ]
    
    for query in queries:
        print(f"\n🔍 Query: {query}")
        results = simple_semantic_search(query, KNOWLEDGE_BASE, top_k=2)
        
        for i, (topic, content, score) in enumerate(results, 1):
            print(f"\n  Result {i}: {topic}")
            print(f"  Similarity: {score:.3f}")
            print(f"  Preview: {content[:150]}...")

def demo_rag():
    """Demo complete RAG pipeline"""
    print("\n" + "="*70)
    print("DEMO 2: RAG PIPELINE")
    print("="*70)
    
    questions = [
        "What Python workshops has WCC hosted?",
        "How do I transition from backend to AI engineering?",
        "What's your advice for mentees?",
    ]
    
    for question in questions:
        result = vertex_ai_rag(question, top_k=2)
        
        print("\n💬 ANSWER:")
        print(result["answer"])
        
        print("\n📚 SOURCES:")
        for source in result["sources"]:
            print(f"  • {source['topic']} (relevance: {source['score']:.3f})")
        
        print("\n" + "-"*70)

def interactive_demo():
    """Interactive Q&A session"""
    print("\n" + "="*70)
    print("INTERACTIVE RAG DEMO")
    print("="*70)
    print("\nAvailable topics:")
    for topic in KNOWLEDGE_BASE.keys():
        print(f"  • {topic}")
    
    print("\nType 'quit' to exit")
    
    while True:
        print("\n" + "-"*70)
        question = input("\n❓ Your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\nThanks for trying the demo! 👋")
            break
        
        if not question:
            continue
        
        result = vertex_ai_rag(question, top_k=2)
        
        print("\n💬 ANSWER:")
        print(result["answer"])
        
        print("\n📚 SOURCES:")
        for source in result["sources"]:
            print(f"  • {source['topic']}")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys
    
    print("\n🎓 WCC AI Learning Series - Session 3: Quick RAG Demo")
    print("=" * 70)
    print("\nThis demo uses a simplified knowledge base for fast demonstration.")
    print("For production, use the full rag_demo.py with ChromaDB.\n")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--search":
            demo_basic_search()
        elif sys.argv[1] == "--rag":
            demo_rag()
        elif sys.argv[1] == "--interactive":
            interactive_demo()
        elif sys.argv[1] == "--all":
            demo_basic_search()
            demo_rag()
    else:
        print("Usage:")
        print("  python vertex_ai_quick_demo.py --search       # Demo semantic search")
        print("  python vertex_ai_quick_demo.py --rag          # Demo RAG pipeline")
        print("  python vertex_ai_quick_demo.py --interactive  # Interactive Q&A")
        print("  python vertex_ai_quick_demo.py --all          # Run all demos")
        print("\nTry: python vertex_ai_quick_demo.py --interactive")

# ============================================================================
# PRESENTER NOTES
# ============================================================================

"""
PRESENTING THIS DEMO:

1. START WITH SEARCH (5 minutes):
   python vertex_ai_quick_demo.py --search
   - Show how semantic search finds relevant docs
   - Explain similarity scores
   - Compare to keyword search

2. SHOW RAG PIPELINE (10 minutes):
   python vertex_ai_quick_demo.py --rag
   - Walk through the questions
   - Highlight how context is retrieved
   - Show citations in answers
   - Explain why it doesn't hallucinate

3. INTERACTIVE SESSION (5 minutes):
   python vertex_ai_quick_demo.py --interactive
   - Take questions from audience
   - Show real-time retrieval and generation
   - Demonstrate edge cases (out-of-scope questions)

KEY POINTS TO EMPHASIZE:
- Embeddings capture semantic meaning
- Vector similarity finds relevant content
- Context + Question → Accurate answer
- Always cite sources for accountability
- System only answers from knowledge base (no hallucination)

COMMON QUESTIONS:
Q: How many documents can this handle?
A: This demo has 5 docs. Production systems handle millions with vector databases.

Q: What if my question isn't in the knowledge base?
A: The system will say it doesn't have that information (demo this!)

Q: How much does this cost?
A: Very cheap - embeddings are $0.00002 per 1K characters, Gemini is $0.0001 per query.

Q: Can I use my company's documents?
A: Yes! Just replace KNOWLEDGE_BASE with your data. For larger datasets, use ChromaDB.
"""
