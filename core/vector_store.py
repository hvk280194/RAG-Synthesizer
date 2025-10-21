# from langchain_community.vectorstores import FAISS
# from sentence_transformers import SentenceTransformer
# import numpy as np
# from typing import List, Dict

# def build_faiss_index(chunks: List[Dict]):
#     model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
#     texts = [c["content"] for c in chunks]
#     embeddings = model.encode(texts)
#     db = FAISS.from_embeddings(embeddings, texts, metadatas=[{"source": c["source"]} for c in chunks])
#     return db, model
# def retrieve_context(db, model, query: str, k: int = 4):
#     query_emb = model.encode([query])
#     docs = db.similarity_search_by_vector(query_emb[0], k=k)
#     context = "\n\n".join([f"[{d.metadata['source']}] {d.page_content}" for d in docs])
    # return context

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List, Dict

def build_faiss_index(chunks: List[Dict]):
    """Create FAISS vector store from text chunks using sentence-transformers."""
    # Use HuggingFaceEmbeddings wrapper (LangChain version)
    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    texts = [c["content"] for c in chunks]
    metadatas = [{"source": c["source"]} for c in chunks]

    # This automatically handles embedding generation
    db = FAISS.from_texts(texts, embedding=emb, metadatas=metadatas)
    return db, emb

def retrieve_context(db, emb_model, query: str, k: int = 10):
    """Retrieve top-k similar chunks."""
    docs = db.similarity_search(query, k=k)
    context = "\n\n".join([f"[{d.metadata['source']}] {d.page_content}" for d in docs])
    return context
