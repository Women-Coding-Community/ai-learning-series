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
from typing import List, Dict
import vertexai
from vertexai.language_models import TextEmbeddingModel
from vertexai.generative_models import GenerativeModel
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ============================================================================
# CONFIGURATION
# ============================================================================

# Set your GCP project ID
PROJECT_ID = "your-project-id"  # TODO: Update this
LOCATION = "us-central1"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Initialize models
embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
generation_model = GenerativeModel("gemini-1.5-flash")

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
# SAMPLE DATA - WCC Blog Posts
# ============================================================================

SAMPLE_BLOGS = [
    {
        "title": "Introduction to Python for Beginners",
        "date": "2024-10-15",
        "url": "https://womencodingcommunity.com/blog/python-intro",
        "content": """
Python is a versatile, beginner-friendly programming language that has become one of the most popular 
languages in the world. Whether you're interested in web development, data science, automation, or 
artificial intelligence, Python is an excellent starting point.

Why Python for Beginners?

Python's syntax is clean and readable, making it easier to learn compared to many other programming 
languages. You can write functional code with fewer lines than languages like Java or C++. This 
simplicity doesn't mean Python lacks power – it's used by tech giants like Google, Netflix, and NASA.

Getting Started with Python

First, install Python from python.org. We recommend Python 3.9 or later. After installation, you can 
verify by opening a terminal and typing 'python --version'. You'll also want to install an IDE like 
VS Code or PyCharm to make coding easier.

Your First Python Program

Let's start with the classic "Hello, World!" program:

print("Hello, World!")

That's it! This simple line prints text to the screen. Try modifying it to print your name.

Basic Python Concepts

Variables store data: name = "Sarah"
Data types include strings, integers, floats, and booleans
Functions are reusable blocks of code defined with 'def'
Loops help you repeat actions with 'for' and 'while'

Next Steps

Practice is key. Try coding challenges on platforms like HackerRank or LeetCode. Join our WCC 
Python study group that meets every Tuesday at 7pm. Check out our GitHub repository with beginner 
exercises: github.com/wcc/python-beginners.

Remember, every expert was once a beginner. Don't be discouraged by errors – they're part of learning!
        """
    },
    {
        "title": "Django Web Development Workshop Recap",
        "date": "2024-09-22",
        "url": "https://womencodingcommunity.com/blog/django-workshop-recap",
        "content": """
Last week, WCC hosted an amazing Django workshop with over 45 attendees! This comprehensive session 
covered building web applications with Python's most popular framework.

What We Covered

Our workshop instructor, Sarah Chen, guided participants through creating a complete blog application. 
The session started with Django fundamentals: models, views, and templates (the MVT pattern). We then 
built user authentication, database migrations, and deployed to Heroku.

Key Takeaways

Django handles a lot of the heavy lifting for you. Its ORM (Object-Relational Mapping) lets you work 
with databases using Python instead of SQL. The built-in admin interface is a game-changer for content 
management. And the Django community is incredibly supportive with extensive documentation.

Project Highlights

Participants built a fully functional blog with:
- User registration and login
- Post creation, editing, and deletion
- Comment system
- Search functionality
- Responsive design with Bootstrap

Attendee Feedback

"This was my first time working with a web framework, and Sarah's teaching style made it so accessible!" 
- Maria K.

"I've been wanting to learn Django for months. This workshop gave me the confidence to start my own 
project." - Priya S.

What's Next?

We're planning a follow-up workshop on Django REST Framework for building APIs. Expected date: November 
2024. Stay tuned to our Slack channel for updates!

Want to continue learning? Join our Django study group that meets bi-weekly. Check out the complete 
workshop code on our GitHub: github.com/wcc/django-blog-workshop.
        """
    },
    {
        "title": "Career Transitions: From Backend to AI Engineering",
        "date": "2024-08-10",
        "url": "https://womencodingcommunity.com/blog/backend-to-ai-transition",
        "content": """
Many developers are curious about transitioning into AI and machine learning. This article shares 
practical advice from WCC members who've successfully made this transition.

Why the Transition Makes Sense

If you're already a backend engineer, you have strong programming fundamentals. You understand APIs, 
databases, and software architecture. These skills transfer beautifully to AI engineering, where you'll 
build systems that incorporate machine learning models.

Skills You Already Have

Backend developers excel at:
- Writing clean, production-quality code
- Working with APIs and data pipelines
- Database design and optimization
- System architecture and scalability
- Debugging and problem-solving

These are exactly the skills needed in AI engineering! You're not starting from scratch.

What You Need to Learn

Focus on these areas:
1. Python (if you don't know it already)
2. Machine learning fundamentals (supervised, unsupervised learning)
3. Popular ML libraries: scikit-learn, TensorFlow, PyTorch
4. MLOps: model deployment, monitoring, versioning
5. Working with LLMs and APIs (OpenAI, Google's Gemini, etc.)

Learning Path Recommendations

Start with Andrew Ng's Machine Learning course on Coursera. Follow up with fast.ai's practical courses. 
Build projects that combine your backend skills with ML – for example, create an API that serves ML 
predictions, or build a recommendation system.

Real Transition Stories

Emma, Backend → ML Engineer at TechCorp:
"I started with weekend projects. Built a sentiment analysis API using my existing Flask knowledge plus 
scikit-learn. That project landed me interviews."

Priya, Java Developer → AI Engineer at FinTech:
"The MLOps part was easiest because it's basically DevOps for ML. My Kubernetes and Docker experience 
translated directly."

Getting Started Today

1. Build a simple ML project this weekend
2. Join AI-focused communities (like our WCC AI study group!)
3. Contribute to open-source ML projects
4. Get GCP or AWS AI certifications
5. Network with AI engineers

Remember: You don't need a PhD. You need curiosity, projects, and persistence. The industry needs 
practical engineers who can build production AI systems, not just researchers.

WCC hosts monthly AI networking events. Join us to connect with others on the same journey!
        """
    },
    {
        "title": "Effective Mentorship: Guide for Mentees",
        "date": "2024-07-18",
        "url": "https://womencodingcommunity.com/blog/mentorship-guide-mentees",
        "content": """
WCC's mentorship program has connected hundreds of women in tech. This guide helps mentees get the 
most from their mentorship experience.

Preparing for Your First Session

Before your first meeting, clarify your goals. Are you looking for career guidance? Technical skills? 
Interview preparation? Be specific. Write down 2-3 concrete goals you'd like to achieve through 
mentorship.

Research your mentor's background on LinkedIn. Understand their experience so you can ask relevant 
questions. Come prepared with specific questions rather than "tell me everything about your career."

During Sessions

Respect your mentor's time. Arrive prepared with:
- Progress updates on previous action items
- Specific questions or challenges you're facing
- Notes to capture advice and resources

Ask thoughtful questions:
- "What would you do differently if you were starting out today?"
- "How do you approach learning new technologies?"
- "Can you review my resume and suggest improvements?"

Avoid overly broad questions like "How do I become a senior engineer?" Instead: "What specific skills 
do I need to develop to move from mid-level to senior?"

Between Sessions

Act on the advice you receive. Mentors appreciate mentees who implement suggestions. If your mentor 
recommends a book or course, engage with it and report back.

Keep communication professional but warm. A brief monthly update email shows you value the relationship. 
Share wins: "I got the job! Your interview prep advice was invaluable."

When to Seek Additional Support

Mentors aren't therapists or career counselors. For deep personal issues, consider professional support. 
For technical questions that need immediate answers, use community forums or Stack Overflow first.

Building Long-term Relationships

The best mentorships extend beyond formal programs. Stay in touch even after the official period ends. 
Share interesting articles, congratulate them on achievements, and offer help when you can.

Remember, mentorship is a two-way street. As you grow, you can mentor others. Many WCC members are both 
mentees and mentors!

Common Mistakes to Avoid

- Being vague about what you want to achieve
- Not doing your homework between sessions
- Expecting mentors to solve all problems for you
- Ghosting after getting what you need
- Not respecting boundaries and time

WCC Mentorship Program

Our program matches women in tech based on skills, goals, and availability. Mentorship pairs meet 
monthly for 6 months. Apply at womencodingcommunity.com/mentorship. Applications open quarterly.

Questions about mentorship? Join our #mentorship Slack channel!
        """
    },
    {
        "title": "Cloud Architecture Best Practices for Startups",
        "date": "2024-06-25",
        "url": "https://womencodingcommunity.com/blog/cloud-architecture-startups",
        "content": """
Last month's WCC tech talk featured Rachel Martinez, Solutions Architect at Google Cloud, who shared 
practical advice for startups building on cloud platforms.

Start Simple, Scale Gradually

Rachel emphasized: "Don't over-engineer from day one. Use managed services until you absolutely need 
more control." For most startups, Platform-as-a-Service (PaaS) options like Google App Engine, AWS 
Elastic Beanstalk, or Azure App Service are perfect.

Avoid premature optimization. You don't need Kubernetes on day one unless you're handling massive scale. 
Start with simpler deployment options and graduate to containers when complexity justifies it.

Core Architecture Principles

1. Stateless Applications: Design apps that don't store session state locally. Use managed databases 
   or caching services like Redis for state management.

2. Managed Services: Leverage cloud provider services instead of self-hosting. Use Cloud SQL instead 
   of managing your own PostgreSQL server.

3. Infrastructure as Code: Use Terraform or CloudFormation from the start. This makes environments 
   reproducible and prevents configuration drift.

4. Monitoring and Logging: Implement from day one. Use Cloud Logging, CloudWatch, or Application 
   Insights. You can't fix what you can't see.

Cost Optimization Tips

Cloud costs can spiral quickly. Rachel shared these strategies:
- Use auto-scaling with appropriate limits
- Set up budget alerts
- Right-size instances (don't use xlarge when medium suffices)
- Use spot/preemptible instances for non-critical workloads
- Implement caching aggressively
- Clean up unused resources regularly

Security Fundamentals

Never skip security basics:
- Enable multi-factor authentication
- Use IAM roles, not root credentials
- Encrypt data at rest and in transit
- Regular security audits with Cloud Security Scanner
- Implement least-privilege access
- Keep dependencies updated

Multi-Cloud vs. Single Cloud

Rachel advised: "For startups, stick with one cloud provider. Multi-cloud adds complexity that most 
startups don't need. Focus on building your product, not managing cloud abstractions."

Database Decisions

Choose based on your needs:
- Relational (SQL): Cloud SQL, RDS – use for structured data, ACID requirements
- NoSQL: Firestore, DynamoDB – use for flexible schemas, high scale
- Caching: Redis, Memcached – essential for performance
- Data Warehouse: BigQuery, Redshift – for analytics

Real-World Example

A WCC member shared her startup's architecture:
- Frontend: React on Netlify (simple, fast)
- API: Python/Flask on Google Cloud Run (serverless, scales to zero)
- Database: Cloud SQL PostgreSQL (managed, automatic backups)
- Storage: Cloud Storage (for user uploads)
- Monitoring: Cloud Logging + Sentry

Total monthly cost for 10,000 users: $150. By year two with 100,000 users: $800. The managed services 
scaled seamlessly without architectural changes.

Common Startup Mistakes

- Over-architecting too early
- Ignoring monitoring until problems arise
- Not implementing CI/CD from the start
- Skipping infrastructure as code
- Choosing databases based on hype, not requirements

Getting Started

Rachel recommended:
1. Take free cloud certifications (AWS Cloud Practitioner, GCP Associate Cloud Engineer)
2. Build a personal project on the cloud
3. Use cloud provider free tiers generously
4. Join cloud architecture communities

Next WCC Tech Talk: "Kubernetes for Beginners" scheduled for August 2024. RSVP on our Meetup page!
        """
    }
]

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
        embeddings = embedding_model.get_embeddings(batch)
        
        # Extract the values (list of floats) from each embedding
        batch_embeddings = [emb.values for emb in embeddings]
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
    query_embedding = embedding_model.get_embeddings([query])[0].values
    
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
    
    response = generation_model.generate_content(prompt)
    
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
    
    # Check if collection has data
    if collection.count() == 0:
        print("\n⚠️  Collection is empty. Running setup...")
        demo_setup()
    else:
        print(f"\n✓ Collection already contains {collection.count()} documents")
        print("  (Use '--reset' to clear and re-setup)")
    
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
            demo_search()
            demo_rag()
    else:
        print("\n💡 Usage:")
        print("  python rag_demo.py           # Check status")
        print("  python rag_demo.py --reset   # Reset and re-setup")
        print("  python rag_demo.py --search  # Demo search")
        print("  python rag_demo.py --rag     # Demo RAG pipeline")
        print("  python rag_demo.py --all     # Run all demos")
        print("\nFor interactive use, see: streamlit_app.py")
