import os
import streamlit as st
import chromadb
from docx import Document  # python-docx
from langchain_text_splitters import RecursiveCharacterTextSplitter
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if(api_key is None):
    raise ValueError("GEMINI_API_KEY not found in environment variables")
genai.configure(api_key=api_key)

EMBED_MODEL = "text-embedding-004"
LLM_MODEL = "gemini-2.5-flash-lite"

chroma_client = chromadb.PersistentClient(path="handbook_db")
collection = chroma_client.get_or_create_collection("staff_handbook")

def load_handbook_chunks(path: str, chunk_size: int = 600, overlap: int = 100):
    print("Loading handbook...")
    doc = Document(path)
    full_text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", " "]
    )
    return splitter.create_documents([full_text])


def upsert_handbook(docs):
    ids, contents = [], []
    for idx, doc in enumerate(docs):
        ids.append(f"handbook_{idx}")
        contents.append(doc.page_content)

    embeddings = genai.embed_content(model=EMBED_MODEL, content=contents)["embedding"]

    collection.upsert(
        ids=ids,
        documents=contents,
        metadatas=[{"source": "Staff Handbook"}] * len(contents),
        embeddings=embeddings
    )

def retrieve(query: str, k: int = 4):
    query_embedding = genai.embed_content(model=EMBED_MODEL, content=query)["embedding"]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "distances"]
    )
    return results["documents"][0]

SYSTEM_PROMPT = """You are an HR assistant specializing in company policies.
Use only the provided Staff Handbook context. If uncertain, say you don't know.
"""

def generate_answer(question: str, context_chunks: list[str]) -> str:
    context_block = "\n\n".join(context_chunks)

    response = genai.GenerativeModel(LLM_MODEL).generate_content(
        [
            SYSTEM_PROMPT,
            f"Context:\n{context_block}",
            f"Employee question: {question}",
            "Answer using the handbook context. If info is missing, say so."
        ]
    )
    return response.text.strip()    

def main():
    st.set_page_config(page_title="Employee Handbook Assistant", page_icon="📘")
    st.title("📘 Employee Handbook Assistant")
    st.caption("Ask any policy question and I'll cite the Staff Handbook.")

    if "messages" not in st.session_state:
        st.session_state.messages = []
        if collection.count() == 0:
            with st.spinner("Loading handbook..."):
                docs = load_handbook_chunks("Staff_Handbook.docx")
                upsert_handbook(docs)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if question := st.chat_input("What policy would you like to check?"):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Looking up the handbook..."):
                context = retrieve(question)
                answer = generate_answer(question, context)
                st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})    


if __name__ == "__main__":
    main()        