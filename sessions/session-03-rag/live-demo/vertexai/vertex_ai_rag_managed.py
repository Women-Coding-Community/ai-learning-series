"""
WCC AI Learning Series - Session 3: Vertex AI RAG Engine Demo

This demo shows Google's managed RAG service (Vertex AI RAG Engine).
Compare this to our DIY approach (rag_demo.py) to see the difference!

Vertex AI RAG Engine handles:
- Document ingestion from Cloud Storage
- Automatic chunking
- Embedding generation
- Vector storage and indexing
- Retrieval and generation in one API call

Prerequisites:
1. GCP project with Vertex AI API enabled
2. Cloud Storage bucket with documents
3. Vertex AI RAG API enabled (Preview)
"""

import os
import vertexai
from vertexai.preview import rag
from vertexai.preview.generative_models import GenerativeModel
from google.cloud import storage

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ID = "your-project-id"  # TODO: Update this
LOCATION = "us-central1"
BUCKET_NAME = f"{PROJECT_ID}-rag-demo"  # Will be created if doesn't exist

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# ============================================================================
# STEP 1: PREPARE DOCUMENTS IN CLOUD STORAGE
# ============================================================================

def setup_cloud_storage():
    """
    Create Cloud Storage bucket and upload sample documents
    """
    print("\n" + "="*70)
    print("STEP 1: Setting up Cloud Storage")
    print("="*70)
    
    storage_client = storage.Client(project=PROJECT_ID)
    
    # Create bucket if it doesn't exist
    try:
        bucket = storage_client.get_bucket(BUCKET_NAME)
        print(f"✓ Using existing bucket: {BUCKET_NAME}")
    except:
        bucket = storage_client.create_bucket(BUCKET_NAME, location=LOCATION)
        print(f"✓ Created new bucket: {BUCKET_NAME}")
    
    # Sample documents (same content as our DIY demo)
    sample_docs = {
        "python_intro.txt": """
Title: Introduction to Python for Beginners
Date: 2024-10-15

Python is a versatile, beginner-friendly programming language perfect for web development,
data science, automation, and AI. 

Why Python? Clean syntax, powerful capabilities, used by Google, Netflix, NASA.

Getting Started:
- Install Python 3.9+ from python.org
- Use VS Code or PyCharm
- Your first program: print("Hello, World!")

Basic Concepts:
- Variables: name = "Sarah"
- Data types: strings, integers, floats, booleans
- Functions: defined with 'def'
- Loops: 'for' and 'while'

Next Steps:
- Practice on HackerRank or LeetCode
- Join WCC Python study group (Tuesdays 7pm)
- Check out github.com/wcc/python-beginners
        """,
        
        "django_workshop.txt": """
Title: Django Web Development Workshop Recap
Date: 2024-09-22

WCC hosted an amazing Django workshop with 45 attendees!

What We Covered:
- MVT pattern (Models, Views, Templates)
- User authentication
- Database migrations
- Deployment to Heroku

Project: Built a complete blog application with:
- User registration and login
- Post creation, editing, deletion
- Comment system
- Search functionality
- Responsive design with Bootstrap

Instructor: Sarah Chen
Code: github.com/wcc/django-blog-workshop
Next: Django REST Framework workshop (November 2024)
        """,
        
        "career_transitions.txt": """
Title: Career Transitions: Backend to AI Engineering
Date: 2024-08-10

Many WCC members have transitioned to AI engineering successfully.

Your Existing Skills:
- Backend development
- APIs and data pipelines
- Databases and architecture
- Debugging and problem-solving

What to Learn:
1. Python (if new to it)
2. ML fundamentals (supervised/unsupervised learning)
3. Libraries: scikit-learn, TensorFlow, PyTorch
4. MLOps: deployment, monitoring, versioning
5. LLM APIs (OpenAI, Gemini)

Learning Path:
- Andrew Ng's ML course on Coursera
- fast.ai practical courses
- Build projects combining backend + ML

Real Stories:
Emma: Backend → ML Engineer (built sentiment analysis API)
Priya: Java → AI Engineer (MLOps expertise transferred directly)

WCC hosts monthly AI networking events!
        """,
        
        "mentorship_guide.txt": """
Title: Effective Mentorship: Guide for Mentees
Date: 2024-07-18

WCC's mentorship program has connected hundreds of women in tech.

Preparing for First Session:
- Clarify 2-3 concrete goals
- Research mentor's background on LinkedIn
- Come with specific questions

During Sessions:
- Share progress on action items
- Ask thoughtful questions
- Take notes

Good Questions:
- "What would you do differently starting out today?"
- "How do you approach learning new technologies?"
- "Can you review my resume?"

Between Sessions:
- Act on advice received
- Send monthly updates
- Share wins!

Mistakes to Avoid:
- Being vague about goals
- Not doing homework
- Expecting mentors to solve everything
- Not respecting boundaries

Apply: womencodingcommunity.com/mentorship (quarterly applications)
        """,
        
        "cloud_architecture.txt": """
Title: Cloud Architecture Best Practices for Startups
Date: 2024-06-25

Rachel Martinez from Google Cloud spoke at WCC about startup architecture.

Key Principles:
1. Start simple, scale gradually
2. Use managed services (Cloud SQL, Cloud Run)
3. Infrastructure as Code (Terraform/CloudFormation)
4. Monitoring from day one

Don't over-engineer! Use PaaS until you need more control.

Cost Optimization:
- Auto-scaling with limits
- Set budget alerts
- Right-size instances
- Use spot/preemptible instances
- Implement caching
- Clean up unused resources

Security Fundamentals:
- MFA enabled
- Use IAM roles
- Encrypt data
- Regular security audits
- Least-privilege access

Real Example (WCC member's startup):
- Frontend: React on Netlify
- API: Python/Flask on Cloud Run
- Database: Cloud SQL PostgreSQL
- Storage: Cloud Storage
Cost: $150/month for 10K users, $800/month for 100K users

Next WCC Talk: "Kubernetes for Beginners" (August 2024)
        """
    }
    
    # Upload documents to Cloud Storage
    print("\nUploading documents to Cloud Storage...")
    for filename, content in sample_docs.items():
        blob = bucket.blob(f"blogs/{filename}")
        blob.upload_from_string(content)
        print(f"  ✓ Uploaded: {filename}")
    
    print(f"\n✓ All documents uploaded to gs://{BUCKET_NAME}/blogs/")
    return f"gs://{BUCKET_NAME}/blogs/"

# ============================================================================
# STEP 2: CREATE RAG CORPUS
# ============================================================================

def create_rag_corpus():
    """
    Create a RAG corpus (collection) in Vertex AI
    """
    print("\n" + "="*70)
    print("STEP 2: Creating RAG Corpus")
    print("="*70)
    
    # Create corpus
    corpus = rag.create_corpus(
        display_name="WCC Blogs",
        description="Women Coding Community blog posts for RAG demo"
    )
    
    print(f"✓ Created corpus: {corpus.name}")
    print(f"  Display name: {corpus.display_name}")
    
    return corpus

# ============================================================================
# STEP 3: IMPORT DOCUMENTS
# ============================================================================

def import_documents(corpus, gcs_path):
    """
    Import documents from Cloud Storage into RAG corpus
    This handles chunking, embedding, and indexing automatically!
    """
    print("\n" + "="*70)
    print("STEP 3: Importing Documents")
    print("="*70)
    print("(Vertex AI handles chunking, embedding, and indexing...)")
    
    # Import files from GCS
    response = rag.import_files(
        corpus_name=corpus.name,
        paths=[gcs_path],
        chunk_size=512,  # Similar to our 400 tokens
        chunk_overlap=100
    )
    
    print("✓ Import started (this may take a minute...)")
    print(f"  Source: {gcs_path}")
    print(f"  Chunk size: 512 characters")
    print(f"  Chunk overlap: 100 characters")
    
    # Wait for import to complete
    print("  Waiting for import to complete...", end="", flush=True)
    import time
    time.sleep(30)  # Import usually takes 20-40 seconds
    print(" Done!")
    
    return response

# ============================================================================
# STEP 4: QUERY WITH RAG
# ============================================================================

def query_with_rag(corpus, question, num_chunks=5):
    """
    Query the RAG corpus - retrieval and generation in ONE call!
    """
    print("\n" + "="*70)
    print("RAG QUERY")
    print("="*70)
    print(f"\n❓ Question: {question}")
    print("-" * 70)
    
    # This one call does EVERYTHING:
    # 1. Embeds the question
    # 2. Searches the vector database
    # 3. Retrieves relevant chunks
    # 4. Generates answer with citations
    response = rag.retrieval_query(
        rag_resources=[
            rag.RagResource(
                rag_corpus=corpus.name,
            )
        ],
        text=question,
        similarity_top_k=num_chunks,
    )
    
    print("\n💬 ANSWER:")
    print(response.answer)
    
    if response.contexts:
        print("\n📚 SOURCES:")
        for i, context in enumerate(response.contexts.contexts, 1):
            print(f"\n  Source {i}:")
            print(f"  File: {context.source_uri}")
            print(f"  Distance: {context.distance:.3f}")
            print(f"  Preview: {context.text[:150]}...")
    
    return response

# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

def demo_setup():
    """
    Complete setup: Storage → Corpus → Import
    """
    print("\n🎓 WCC AI Learning Series - Vertex AI RAG Engine Demo")
    print("=" * 70)
    
    # Step 1: Setup Cloud Storage
    gcs_path = setup_cloud_storage()
    
    # Step 2: Create corpus
    corpus = create_rag_corpus()
    
    # Step 3: Import documents
    import_documents(corpus, gcs_path + "*")
    
    print("\n✅ Setup complete! Corpus is ready for queries.")
    print(f"   Corpus name: {corpus.name}")
    
    return corpus

def demo_queries(corpus):
    """
    Run sample queries
    """
    print("\n" + "="*70)
    print("DEMO QUERIES")
    print("="*70)
    
    questions = [
        "What Python workshops has WCC hosted?",
        "How do I transition from backend to AI engineering?",
        "What's your advice for mentees?",
        "Tell me about cloud architecture best practices"
    ]
    
    for question in questions:
        query_with_rag(corpus, question, num_chunks=3)
        print("\n" + "-"*70)
        input("Press Enter for next question...")

def demo_interactive(corpus):
    """
    Interactive Q&A session
    """
    print("\n" + "="*70)
    print("INTERACTIVE MODE")
    print("="*70)
    print("Ask questions about WCC content!")
    print("Type 'quit' to exit\n")
    
    while True:
        question = input("\n❓ Your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\nThanks for trying Vertex AI RAG! 👋")
            break
        
        if not question:
            continue
        
        query_with_rag(corpus, question, num_chunks=3)

def cleanup(corpus_name):
    """
    Delete the corpus (cleanup)
    """
    print("\n" + "="*70)
    print("CLEANUP")
    print("="*70)
    
    try:
        rag.delete_corpus(name=corpus_name)
        print(f"✓ Deleted corpus: {corpus_name}")
    except Exception as e:
        print(f"✗ Error deleting corpus: {e}")
    
    print("\nNote: Cloud Storage bucket and files remain for reuse.")
    print(f"To delete bucket: gsutil -m rm -r gs://{BUCKET_NAME}")

# ============================================================================
# COMPARISON WITH DIY RAG
# ============================================================================

def print_comparison():
    """
    Print comparison between DIY and Vertex AI RAG
    """
    print("\n" + "="*70)
    print("DIY RAG vs VERTEX AI RAG - Comparison")
    print("="*70)
    
    print("""
╔══════════════════════╦════════════════════════╦═══════════════════════╗
║ Feature              ║ DIY (rag_demo.py)      ║ Vertex AI RAG         ║
╠══════════════════════╬════════════════════════╬═══════════════════════╣
║ Setup Time           ║ ~30 min (first time)   ║ ~5 min                ║
║ Code Lines           ║ ~500 lines             ║ ~50 lines             ║
║ Chunking             ║ Manual (LangChain)     ║ Automatic             ║
║ Embeddings           ║ Manual API calls       ║ Automatic             ║
║ Vector DB            ║ ChromaDB (local)       ║ Managed (cloud)       ║
║ Search               ║ Manual implementation  ║ One API call          ║
║ Generation           ║ Separate Gemini call   ║ Integrated            ║
║ Scalability          ║ Limited (local)        ║ Enterprise scale      ║
║ Access Control       ║ DIY                    ║ Built-in IAM          ║
║ Audit Logs           ║ DIY                    ║ Built-in              ║
║ Cost                 ║ Very low (local)       ║ Pay per query         ║
║ Learning Value       ║ ⭐⭐⭐⭐⭐ (see internals)║ ⭐⭐ (black box)       ║
║ Production Ready     ║ ⭐⭐ (needs hardening)  ║ ⭐⭐⭐⭐⭐ (enterprise)   ║
╚══════════════════════╩════════════════════════╩═══════════════════════╝

WHEN TO USE EACH:

DIY RAG (rag_demo.py):
✅ Learning and understanding RAG concepts
✅ Custom chunking logic needed
✅ Small to medium datasets (< 100K documents)
✅ Budget-conscious (free local option)
✅ Prototyping and experimentation

Vertex AI RAG Engine:
✅ Production deployments
✅ Enterprise features needed (IAM, audit, compliance)
✅ Large scale (100K+ documents)
✅ Team doesn't want to manage infrastructure
✅ Need automatic updates and scaling

BOTTOM LINE:
Learn with DIY → Deploy with Vertex AI RAG
(Just like we learned to build the car engine, then use a manufactured one!)
    """)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys
    
    print("\n🎓 WCC AI Learning Series - Vertex AI RAG Engine Demo")
    print("=" * 70)
    print("\nThis demo uses Google's managed RAG service.")
    print("Compare to rag_demo.py to see the differences!\n")
    
    # Print comparison first
    print_comparison()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--setup":
            corpus = demo_setup()
            print(f"\n✅ Setup complete! Save this corpus name for queries:")
            print(f"   {corpus.name}")
            
        elif sys.argv[1] == "--query":
            if len(sys.argv) < 3:
                print("Usage: python vertex_ai_rag_managed.py --query <corpus_name>")
                sys.exit(1)
            
            corpus_name = sys.argv[2]
            # Reconstruct corpus object
            corpus = rag.RagCorpus(name=corpus_name)
            demo_queries(corpus)
            
        elif sys.argv[1] == "--interactive":
            if len(sys.argv) < 3:
                print("Usage: python vertex_ai_rag_managed.py --interactive <corpus_name>")
                sys.exit(1)
            
            corpus_name = sys.argv[2]
            corpus = rag.RagCorpus(name=corpus_name)
            demo_interactive(corpus)
            
        elif sys.argv[1] == "--cleanup":
            if len(sys.argv) < 3:
                print("Usage: python vertex_ai_rag_managed.py --cleanup <corpus_name>")
                sys.exit(1)
            
            cleanup(sys.argv[2])
            
        elif sys.argv[1] == "--all":
            corpus = demo_setup()
            input("\nPress Enter to run demo queries...")
            demo_queries(corpus)
    else:
        print("\nUsage:")
        print("  python vertex_ai_rag_managed.py --setup           # One-time setup")
        print("  python vertex_ai_rag_managed.py --query <corpus>  # Run demo queries")
        print("  python vertex_ai_rag_managed.py --interactive <corpus>  # Interactive Q&A")
        print("  python vertex_ai_rag_managed.py --cleanup <corpus>      # Delete corpus")
        print("  python vertex_ai_rag_managed.py --all             # Setup + queries")
        print("\nExample workflow:")
        print("  1. python vertex_ai_rag_managed.py --setup")
        print("  2. python vertex_ai_rag_managed.py --interactive projects/123/locations/us-central1/ragCorpora/456")

# ============================================================================
# PRESENTER NOTES
# ============================================================================

"""
PRESENTING VERTEX AI RAG (5-10 minutes):

1. SHOW THE COMPARISON TABLE (2 min):
   - "Let me show you what this looks like in production"
   - Walk through the comparison table
   - Emphasize: same concepts, different implementation

2. LIVE DEMO - SETUP (3 min):
   python vertex_ai_rag_managed.py --setup
   - Point out how much is automated
   - "Google is doing all the work we did manually!"
   - Show: upload → corpus created → indexed automatically

3. LIVE DEMO - QUERY (2 min):
   python vertex_ai_rag_managed.py --interactive <corpus-name>
   - Take a question from audience
   - Show how it's ONE API call
   - Point out: still gets citations!

4. WHEN TO USE EACH (2 min):
   - "For learning: DIY (what we built)"
   - "For production: Vertex AI RAG Engine"
   - "You now understand BOTH approaches!"

KEY MESSAGES:
✅ Concepts are identical (you already learned them!)
✅ Vertex AI just packages it all up
✅ DIY gives you control and understanding
✅ Managed service gives you scale and features
✅ You learned to build the engine - now you can also buy one!

TIMING:
- Include this ONLY if ahead of schedule
- Perfect for "advanced" students who ask "what about production?"
- Can be skipped if running behind

BACKUP PLAN:
- If API fails, just show the comparison table
- Walk through the code differences
- Point to documentation
"""
