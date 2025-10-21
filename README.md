# 🧠 InsightBridge: AI Research Synthesizer (Free Hugging Face Edition)

A cost-free Retrieval-Augmented Generation (RAG) application that lets you upload multiple technical PDFs and 
generate cross-document insights using open-source models.

## ✨ Features
- Multi-PDF ingestion & semantic chunking  
- FAISS-based vector search  
- Sentence-Transformer embeddings  
- Hugging Face-hosted LLMs (Mistral, Llama, etc.)  
- Streamlit UI + Plotly visualization  

## 🚀 Run locally
```bash
pip install -r requirements.txt
export HF_TOKEN="hf_..."   # optional but recommended
streamlit run app.py
