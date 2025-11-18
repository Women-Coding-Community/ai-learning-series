"""
WCC AI Learning Series - Session 3: RAG Demo
Streamlit Web Interface

Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import sys
from typing import Dict, List

# Import our RAG functions
from rag_demo import (
    semantic_search,
    rag_query,
    collection,
    SAMPLE_BLOGS,
    demo_setup
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="WCC Blog Search",
    page_icon="🔍",
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
    .chunk-preview {
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
# SIDEBAR - CONFIGURATION
# ============================================================================

with st.sidebar:
    st.image("https://via.placeholder.com/300x100/6B46C1/FFFFFF?text=WCC+AI+Series", 
             use_column_width=True)
    
    st.markdown("### ⚙️ Search Settings")
    
    num_results = st.slider(
        "Number of results",
        min_value=1,
        max_value=10,
        value=5,
        help="How many relevant chunks to retrieve"
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
    
    # Check collection status
    doc_count = collection.count()
    
    if doc_count > 0:
        st.success(f"✓ {doc_count} chunks indexed")
    else:
        st.warning("⚠️ No documents indexed")
        if st.button("Initialize System"):
            with st.spinner("Setting up RAG system..."):
                demo_setup()
            st.rerun()
    
    st.markdown(f"""
    **Indexed blogs:** {len(SAMPLE_BLOGS)}  
    **Total chunks:** {doc_count}  
    **Embedding model:** text-embedding-004  
    **LLM:** gemini-1.5-flash
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 💡 Tips
    - Ask specific questions
    - Questions about Python, Django, mentorship, or cloud work best
    - Try: "What events covered web development?"
    """)

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Header
st.markdown('<p class="main-header">🔍 WCC Blog Search</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ask questions about Women Coding Community content</p>', 
            unsafe_allow_html=True)

# Check if system is initialized
if collection.count() == 0:
    st.error("⚠️ System not initialized. Please click 'Initialize System' in the sidebar.")
    st.stop()

# Create tabs
tab1, tab2, tab3 = st.tabs(["🤖 RAG Q&A", "🔍 Semantic Search", "📚 Indexed Blogs"])

# ============================================================================
# TAB 1: RAG Q&A
# ============================================================================

with tab1:
    st.markdown("### Ask a Question")
    st.markdown("Get answers with citations from WCC blog posts")
    
    # Query input
    question = st.text_input(
        "Your question:",
        placeholder="What Python workshops has WCC hosted?",
        key="rag_query"
    )
    
    # Example questions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🐍 Python topics?"):
            question = "What Python topics has WCC covered?"
    with col2:
        if st.button("💼 Career advice?"):
            question = "How can I transition from backend to AI?"
    with col3:
        if st.button("👥 Mentorship tips?"):
            question = "What advice do you have for mentees?"
    
    if question:
        with st.spinner("🔍 Searching and generating answer..."):
            result = rag_query(question, k=num_results)
        
        # Display answer
        st.markdown("### 💬 Answer")
        st.markdown(result['answer'])
        
        # Display sources
        if result['sources']:
            st.markdown("### 📚 Sources")
            for i, source in enumerate(result['sources'], 1):
                st.markdown(f"""
                <div class="source-card">
                    <strong>{i}. {source['title']}</strong><br>
                    📅 {source['date']} | 🔗 <a href="{source['url']}" target="_blank">Read full article</a>
                </div>
                """, unsafe_allow_html=True)
        
        # Display chunks if requested
        if show_chunks and result['chunks']:
            st.markdown("### 📄 Retrieved Chunks")
            st.markdown("*These are the actual text chunks used as context for the answer*")
            
            for i, chunk in enumerate(result['chunks'], 1):
                with st.expander(f"Chunk {i}: {chunk['metadata']['title']}"):
                    if show_distances:
                        st.markdown(f"**Similarity score:** {chunk['distance']:.4f}")
                    st.markdown(f"**Source:** {chunk['metadata']['title']}")
                    st.markdown(f"**Chunk ID:** {chunk['metadata']['chunk_id']} of {chunk['metadata']['total_chunks']}")
                    st.markdown("---")
                    st.markdown(chunk['text'])

# ============================================================================
# TAB 2: SEMANTIC SEARCH
# ============================================================================

with tab2:
    st.markdown("### Semantic Search")
    st.markdown("Find relevant content without RAG - just pure search")
    
    # Search input
    search_query = st.text_input(
        "Search query:",
        placeholder="learning Python programming",
        key="search_query"
    )
    
    # Example searches
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🌐 Web frameworks"):
            search_query = "web development frameworks"
    with col2:
        if st.button("☁️ Cloud architecture"):
            search_query = "cloud computing best practices"
    with col3:
        if st.button("🎓 Learning resources"):
            search_query = "how to learn programming"
    
    if search_query:
        with st.spinner("🔍 Searching..."):
            results = semantic_search(search_query, k=num_results)
        
        if results:
            st.markdown(f"### Found {len(results)} relevant chunks")
            
            for i, result in enumerate(results, 1):
                with st.expander(f"Result {i}: {result['metadata']['title']}"):
                    # Metadata
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**Title:** {result['metadata']['title']}")
                        st.markdown(f"**Date:** {result['metadata']['date']}")
                        st.markdown(f"**URL:** [{result['metadata']['url']}]({result['metadata']['url']})")
                    with col2:
                        if show_distances:
                            st.markdown(f"**Score:** {result['distance']:.4f}")
                    
                    # Content
                    st.markdown("---")
                    st.markdown("**Content Preview:**")
                    st.markdown(f'<div class="chunk-preview">{result["text"]}</div>', 
                              unsafe_allow_html=True)
        else:
            st.warning("No results found. Try a different query.")

# ============================================================================
# TAB 3: INDEXED BLOGS
# ============================================================================

with tab3:
    st.markdown("### 📚 Indexed Blog Posts")
    st.markdown(f"Currently indexing **{len(SAMPLE_BLOGS)}** blog posts")
    
    for i, blog in enumerate(SAMPLE_BLOGS, 1):
        with st.expander(f"{i}. {blog['title']}"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**Date:** {blog['date']}")
                st.markdown(f"**URL:** [{blog['url']}]({blog['url']})")
            with col2:
                # Count chunks for this blog
                chunks_in_blog = sum(1 for j in range(collection.count()) 
                                   if collection.get(ids=[f"chunk_{j}"])['metadatas'][0]['title'] == blog['title'])
                st.metric("Chunks", chunks_in_blog)
            
            st.markdown("**Content Preview:**")
            st.markdown(f'<div class="chunk-preview">{blog["content"][:500]}...</div>', 
                      unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #718096; font-size: 0.9rem;">
    <p>WCC AI Learning Series - Session 3: Introduction to RAG</p>
    <p>Built with Vertex AI, ChromaDB, and Gemini</p>
</div>
""", unsafe_allow_html=True)
