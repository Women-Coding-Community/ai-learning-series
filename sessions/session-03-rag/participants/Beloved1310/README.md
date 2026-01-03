# WCC Event Archive Q&A System

## Overview

This project implements a RAG (Retrieval-Augmented Generation) system for searching and querying the Women Coding Community (WCC) event history. Users can ask questions like "What Python events did WCC host?" or "Who spoke about cloud architecture?" and get answers with citations from past events.

## Features

- **Semantic Search**: Find relevant events using natural language queries
- **Q&A System**: Get comprehensive answers with source citations
- **Event Metadata**: Search by topic, speaker, date, or description
- **Streamlit Interface**: User-friendly web interface for exploring events
- **ChromaDB Storage**: Persistent vector database for fast retrieval

## Project Structure

```
event-archive/
├── rag_pipeline.py      # Core RAG pipeline implementation
├── app.py                # Streamlit web interface
├── data/
│   └── events.csv        # Event data (20 events)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
PROJECT_ID=your-gcp-project-id
LOCATION=us-central1
EMBEDDING_MODEL_NAME=text-embedding-004
GENERATION_MODEL_NAME=gemini-2.5-flash-lite
```

### 3. Authenticate with GCP

**⚠️ IMPORTANT: You must set up Application Default Credentials before running the app!**

**Option A: Using gcloud CLI (Recommended - Easiest)**

```bash

# Authenticate
gcloud auth application-default login

# Set your project
gcloud config set project YOUR_PROJECT_ID
```

**Option B: Using Service Account JSON**

1. Create a service account in GCP Console:
   - Go to IAM & Admin → Service Accounts
   - Create a new service account
   - Grant "Vertex AI User" role
   - Create and download JSON key

2. Set environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-key.json"
```

**Troubleshooting:**
- If you see "credentials not found" error, run: `gcloud auth application-default login`
- Make sure Vertex AI API is enabled in your GCP project
- Verify your PROJECT_ID is correct in the .env file

### 4. Run the Application

**Option 1: Streamlit Web Interface (Recommended)**
```bash
streamlit run app.py
```

**Option 2: Command Line**
```bash
python rag_pipeline.py
```

## Data

### Events Indexed

**Total Events:** 20 events  
**Date Range:** January 2023 - October 2024  
**Topics Covered:** Python, Django, Cloud Architecture, AI/ML, Data Science, Web Development, DevOps, and more

### Sample Events

- Python Basics Workshop (Oct 2024)
- Django Web Development (Sep 2024)
- Cloud Architecture Deep Dive (Aug 2024)
- AI and Machine Learning Intro (Jul 2024)
- Python for Data Science (Jun 2024)
- And 15 more events...

## Implementation Details

### Chunking Strategy

**Best Chunk Size:** 500 characters  
**Chunk Overlap:** 50 characters  
**Rationale:** 
- 500 characters provides enough context for meaningful retrieval
- Large enough to capture complete thoughts and event descriptions
- Small enough to maintain specificity for targeted queries
- 50-character overlap ensures context continuity between chunks

### Metadata Handling

Each chunk includes:
- `title`: Event title
- `date`: Event date (YYYY-MM-DD format)
- `speaker`: Speaker name
- `url`: Event URL
- `chunk_id`: Chunk index within event
- `total_chunks`: Total chunks for the event

This metadata enables:
- Filtering by date range
- Speaker-based queries
- Event-specific retrieval
- Source attribution in answers

### Embedding Model

- **Model:** `text-embedding-004`
- **Dimension:** 10 (reduced for efficiency)
- **Provider:** Vertex AI

### Generation Model

- **Model:** `gemini-2.5-flash-lite`
- **Provider:** Vertex AI
- **Use Case:** Answer generation with context from retrieved chunks

## Example Queries

### 1. Topic-Based Queries
```
Query: "What Python events did WCC host?"
Result: Returns all Python-related events with dates and speakers
```

### 2. Speaker-Based Queries
```
Query: "Who spoke about cloud architecture?"
Result: Identifies Rachel Martinez's Cloud Architecture Deep Dive event
```

### 3. Date-Based Queries
```
Query: "What events were in September?"
Result: Returns events from September 2024 (Django Web Development)
```

### 4. Technical Queries
```
Query: "What events covered machine learning?"
Result: Returns AI/ML Intro event and scikit-learn workshop
```

## Problems Faced

### Problem 1: Google Application Default Credentials (ADC) Setup

I encountered significant difficulty setting up Google Application Default Credentials (ADC) to get the authentication token working. When I first ran the application, I kept getting this error:

```
Your default credentials were not found. To set up Application Default Credentials, see https://cloud.google.com/docs/authentication/external/set-up-adc for more information.
```

**My Experience:**
- The demo and documentation were not detailed enough for my specific environment setup
- I had a service account JSON file (`angular-sorter-300803-6352fb3c7987.json`) with a valid project ID, but the application still couldn't find the credentials
- The error messages didn't provide clear, actionable steps for my situation
- I spent considerable time trying different approaches:
  - Setting `GOOGLE_APPLICATION_CREDENTIALS` environment variable
  - Using `gcloud auth application-default login`
  - Placing the JSON file in different locations
  - Checking project ID configuration

**What Would Have Helped:**
- More specific error messages pointing to exact configuration issues
- Step-by-step troubleshooting guide for different authentication scenarios
- Clearer instructions on how to verify credentials are working
- Better integration between service account JSON files and the application

### Problem 2: Billing Credentials Setup

Another challenge I faced was setting up billing credentials for my GCP project. This was a separate but related issue that needed to be resolved before I could use Vertex AI services.

**My Experience:**
- The setup process required navigating multiple GCP console pages
- Understanding the relationship between billing accounts, projects, and service accounts was not immediately clear
- The demo assumed billing was already configured, which wasn't the case for me

**What Would Have Helped:**
- A checklist of prerequisites before starting the project
- Clear explanation of billing requirements and how to set them up
- Visual guide or screenshots for GCP console navigation

## Challenges & Solutions

### Challenge 1: Structured Data Handling
**Problem:** CSV data needed proper formatting for RAG pipeline  
**Solution:** Created `load_events_from_csv()` method that combines title, speaker, and description into searchable content while preserving metadata separately.

### Challenge 2: Optimal Chunk Size
**Problem:** Finding the right balance between context and specificity  
**Solution:** Tested multiple chunk sizes (200, 400, 500, 800). 500 characters provided the best balance:
- Small enough for specific retrieval
- Large enough to maintain context
- Preserves event descriptions as complete units

### Challenge 3: Metadata Preservation
**Problem:** Ensuring date, speaker, and URL information is available in search results  
**Solution:** Stored comprehensive metadata with each chunk and included it in the RAG prompt for better answer generation.

### Challenge 4: Date-Based Filtering
**Problem:** Vector search doesn't naturally support date range queries  
**Solution:** Included dates in chunk content and metadata. The LLM can interpret date information from retrieved chunks to answer date-based questions.

## Testing Results

### Query Performance

| Query Type | Results | Accuracy |
|------------|---------|----------|
| Topic-based | 5/5 | 100% |
| Speaker-based | 4/5 | 80% |
| Date-based | 3/5 | 60% |
| Technical | 5/5 | 100% |

### Chunk Size Comparison

| Chunk Size | Avg Retrieval Quality | Context Preservation |
|------------|----------------------|---------------------|
| 200 chars | High specificity | Low context |
| 400 chars | Good balance | Moderate context |
| **500 chars** | **Best balance** | **Good context** |
| 800 chars | Lower specificity | High context |

## Future Improvements

1. **Date Range Filtering**: Implement pre-filtering by date before vector search
2. **Speaker Filtering**: Add metadata filtering for speaker-specific queries
3. **Event Categories**: Add topic tags for better categorization
4. **Multi-modal Search**: Include event images or slides if available
5. **Analytics**: Track popular queries and events

## Key Learnings

1. **Chunk Size Matters**: Finding the optimal chunk size requires experimentation
2. **Metadata is Critical**: Preserving structured data (dates, speakers) improves answer quality
3. **Prompt Engineering**: Including metadata in the prompt helps the LLM generate better answers
4. **User Experience**: Streamlit provides an excellent interface for RAG systems
5. **Structured Data**: CSV to RAG requires careful content formatting

## Resources Used

- [Session 3 Starter Template](../starter-template/)
- [Session 3 Live Demo](../live-demo/)
- [Event Archive Q&A Guide](../../use-case-guides/event-archive-qa.md)
- Vertex AI Documentation
- ChromaDB Documentation

## Acknowledgments

Thanks to the WCC AI Learning Series team for providing excellent learning materials and the RAG pipeline starter template!

---
