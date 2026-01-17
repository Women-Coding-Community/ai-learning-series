"""
WCC AI Learning Series - Session 3: Event Archive Q&A
Streamlit Web Interface for searching WCC event history

Run with: streamlit run app.py
"""

import streamlit as st
import os
from typing import Dict, List
from dotenv import load_dotenv

# Import our RAG pipeline
from rag_pipeline import EventArchiveRAG

load_dotenv()

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="WCC Event Archive",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #6B46C1;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #718096;
        text-align: center;
        margin-bottom: 2rem;
    }
    .source-card {
        background-color: #F7FAFC;
        border-left: 4px solid #6B46C1;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
    }
    .event-card {
        background-color: #EDF2F7;
        padding: 1rem;
        border-radius: 0.5rem;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    .distance-badge {
        background-color: #48BB78;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        font-size: 0.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE RAG PIPELINE
# ============================================================================

@st.cache_resource
def initialize_rag():
    """Initialize the RAG pipeline (cached to avoid re-initialization)"""
    project_id = os.getenv("PROJECT_ID") or os.getenv("GCP_PROJECT_ID")
    location = os.getenv("LOCATION", "us-central1")
    
    if not project_id:
        st.error("⚠️ PROJECT_ID not found in environment variables. Please set it in your .env file.")
        return None
    
    try:
        rag = EventArchiveRAG(project_id=project_id, location=location)
        return rag
    except Exception as e:
        error_msg = str(e)
        
        # Check for authentication errors
        if "credentials" in error_msg.lower() or "authentication" in error_msg.lower():
            st.error("❌ **Authentication Error: Default credentials not found**")
            st.markdown("""
            ### 🔐 How to Fix:
            
            **Option 1: Use gcloud CLI (Recommended)**
            ```bash
            gcloud auth application-default login
            ```
            
            **Option 2: Use Service Account JSON**
            1. Download your service account JSON key from GCP Console
            2. Set environment variable:
            ```bash
            export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-key.json"
            ```
            
            **For more help, see:** [GCP Setup Guide](../../../getting-started/gcp-setup.md)
            """)
        else:
            st.error(f"❌ Error initializing RAG pipeline: {e}")
        
        return None

# Initialize RAG
rag = initialize_rag()

# ============================================================================
# SIDEBAR - CONFIGURATION
# ============================================================================

with st.sidebar:
    st.markdown("### 📅 WCC Event Archive")
    st.markdown("Search past events and get answers about WCC history")
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Search Settings")
    
    num_results = st.slider(
        "Number of results",
        min_value=1,
        max_value=10,
        value=5,
        help="How many relevant event chunks to retrieve"
    )
    
    show_chunks = st.checkbox(
        "Show retrieved chunks",
        value=False,
        help="Display the actual text chunks used for context"
    )
    
    show_distances = st.checkbox(
        "Show similarity scores",
        value=False,
        help="Display distance scores (lower = more similar)"
    )
    
    st.markdown("---")
    
    st.markdown("### 📊 System Status")
    
    if rag:
        # Check collection status
        doc_count = rag.collection.count()
        
        if doc_count > 0:
            st.success(f"✓ {doc_count} chunks indexed")
            st.info(f"📅 {len(rag.documents)} events loaded")
        else:
            st.warning("⚠️ No events indexed")
            st.info("Click 'Initialize System' below to load events")
        
        st.markdown(f"""
        **Embedding model:** text-embedding-004  
        **LLM:** gemini-2.5-flash-lite
        """)
        
        # Initialize button
        if doc_count == 0:
            if st.button("🚀 Initialize System", type="primary"):
                with st.spinner("Loading events and setting up RAG system..."):
                    try:
                        csv_path = "data/events.csv"
                        rag.load_events_from_csv(csv_path)
                        rag.chunk_documents(chunk_size=500)
                        rag.embed_and_store()
                        st.success("✓ System initialized successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error initializing: {e}")
    else:
        st.error("RAG pipeline not initialized")
    
    st.markdown("---")
    
    st.markdown("""
    ### 💡 Tips
    - Ask about specific topics: "Python", "cloud", "web development"
    - Search by speaker: "Who spoke about..."
    - Date-based queries: "What events were in September?"
    - Try: "What Python events did WCC host?"
    """)

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Header
st.markdown('<p class="main-header">📅 WCC Event Archive</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Search and ask questions about past WCC events</p>', 
            unsafe_allow_html=True)

# Check if system is initialized
if not rag:
    st.error("⚠️ RAG pipeline not initialized. Please check your .env file and PROJECT_ID.")
    st.stop()

if rag.collection.count() == 0:
    st.warning("⚠️ System not initialized. Please click 'Initialize System' in the sidebar.")
    st.stop()

# Create tabs
tab1, tab2, tab3 = st.tabs(["🤖 Q&A", "🔍 Search", "📚 All Events"])

# ============================================================================
# TAB 1: RAG Q&A
# ============================================================================

with tab1:
    st.markdown("### Ask a Question")
    st.markdown("Get answers with citations from WCC event history")
    
    # Query input
    question = st.text_input(
        "Your question:",
        placeholder="What Python events did WCC host?",
        key="rag_query"
    )
    
    # Example questions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🐍 Python events?"):
            question = "What Python events did WCC host?"
    with col2:
        if st.button("☁️ Cloud topics?"):
            question = "Who spoke about cloud architecture?"
    with col3:
        if st.button("📅 September events?"):
            question = "What events were in September?"
    
    if question:
        with st.spinner("🔍 Searching events and generating answer..."):
            try:
                result = rag.query(question, k=num_results)
            except Exception as e:
                st.error(f"❌ Error querying: {e}")
                result = None
        
        if result:
            # Display answer
            st.markdown("### 💬 Answer")
            st.markdown(result['answer'])
            
            # Display sources
            if result['sources']:
                st.markdown("### 📚 Events")
                for i, source in enumerate(result['sources'], 1):
                    st.markdown(f"""
                    <div class="source-card">
                        <strong>{i}. {source['title']}</strong><br>
                        📅 {source['date']} | 👤 {source['speaker']}<br>
                        🔗 <a href="{source['url']}" target="_blank">Event link</a>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Display chunks if requested
            if show_chunks and result.get('chunks'):
                st.markdown("### 📄 Retrieved Chunks")
                st.markdown("*These are the actual text chunks used as context for the answer*")
                
                for i, chunk in enumerate(result['chunks'], 1):
                    with st.expander(f"Chunk {i}: {chunk['metadata']['title']}"):
                        if show_distances:
                            st.markdown(f"**Similarity score:** {chunk['distance']:.4f}")
                        st.markdown(f"**Event:** {chunk['metadata']['title']}")
                        st.markdown(f"**Date:** {chunk['metadata']['date']}")
                        st.markdown(f"**Speaker:** {chunk['metadata']['speaker']}")
                        st.markdown(f"**Chunk ID:** {chunk['metadata']['chunk_id']} of {chunk['metadata']['total_chunks']}")
                        st.markdown("---")
                        st.markdown(chunk['text'])

# ============================================================================
# TAB 2: SEMANTIC SEARCH
# ============================================================================

with tab2:
    st.markdown("### Semantic Search")
    st.markdown("Find relevant events without RAG - just pure search")
    
    # Search input
    search_query = st.text_input(
        "Search query:",
        placeholder="Python workshops",
        key="search_query"
    )
    
    # Example searches
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🌐 Web development"):
            search_query = "web development frameworks"
    with col2:
        if st.button("☁️ Cloud computing"):
            search_query = "cloud architecture"
    with col3:
        if st.button("🤖 Machine learning"):
            search_query = "machine learning AI"
    
    if search_query:
        with st.spinner("🔍 Searching..."):
            try:
                results = rag.search(search_query, k=num_results)
            except Exception as e:
                st.error(f"❌ Error searching: {e}")
                results = []
        
        if results:
            st.markdown(f"### Found {len(results)} relevant events")
            
            for i, result in enumerate(results, 1):
                with st.expander(f"Result {i}: {result['metadata']['title']}"):
                    # Metadata
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**Title:** {result['metadata']['title']}")
                        st.markdown(f"**Date:** {result['metadata']['date']}")
                        st.markdown(f"**Speaker:** {result['metadata']['speaker']}")
                        st.markdown(f"**URL:** [{result['metadata']['url']}]({result['metadata']['url']})")
                    with col2:
                        if show_distances:
                            st.markdown(f"**Score:** {result['distance']:.4f}")
                    
                    # Content
                    st.markdown("---")
                    st.markdown("**Content Preview:**")
                    st.markdown(f'<div class="event-card">{result["text"]}</div>', 
                              unsafe_allow_html=True)
        else:
            st.warning("No results found. Try a different query.")

# ============================================================================
# TAB 3: ALL EVENTS
# ============================================================================

with tab3:
    st.markdown("### 📚 All Indexed Events")
    
    if rag.documents:
        st.markdown(f"Currently indexing **{len(rag.documents)}** events")
        
        # Sort by date (newest first)
        sorted_events = sorted(rag.documents, key=lambda x: x['date'], reverse=True)
        
        for i, event in enumerate(sorted_events, 1):
            with st.expander(f"{i}. {event['title']}"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**Date:** {event['date']}")
                    st.markdown(f"**Speaker:** {event['speaker']}")
                    st.markdown(f"**URL:** [{event['url']}]({event['url']})")
                with col2:
                    # Count chunks for this event
                    chunks_in_event = sum(1 for chunk in rag.chunks 
                                         if chunk['metadata']['title'] == event['title'])
                    st.metric("Chunks", chunks_in_event)
                
                st.markdown("**Description:**")
                st.markdown(f'<div class="event-card">{event["content"][:500]}...</div>', 
                          unsafe_allow_html=True)
    else:
        st.info("No events loaded. Initialize the system first.")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #718096; font-size: 0.9rem;">
    <p>WCC AI Learning Series - Session 3: Event Archive Q&A</p>
    <p>Built with Vertex AI, ChromaDB, and Gemini</p>
</div>
""", unsafe_allow_html=True)

