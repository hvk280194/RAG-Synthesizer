import streamlit as st
import plotly.express as px
import pandas as pd
from core.ingestion import load_pdfs
from core.vector_store import build_faiss_index, retrieve_context
from core.synthesis import synthesize_across_docs

st.set_page_config(page_title="InsightBridge: AI Research Synthesizer", page_icon="🧠", layout="wide")

st.title("🧠 InsightBridge: AI Research Synthesizer (Free Hugging Face Edition)")
st.markdown("Upload multiple research papers and explore synthesized insights using open-source models.")

uploaded_files = st.file_uploader("📄 Upload PDFs", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    with st.spinner("Processing documents..."):
        chunks = load_pdfs(uploaded_files)
        db, emb_model = build_faiss_index(chunks)
    st.success(f"Indexed {len(chunks)} text chunks from {len(uploaded_files)} PDFs.")

    query = st.text_input("🔍 Ask a research question (e.g., 'Compare dropout vs. quantization methods'):")
    if query:
        with st.spinner("Retrieving relevant content..."):
            context = retrieve_context(db, emb_model, query)
        with st.spinner("Generating synthesized insight..."):
            answer = synthesize_across_docs(context, query)
        st.markdown("### 🧩 Synthesized Insight")
        st.write(answer)

        data = {"source": [c["source"] for c in chunks]}
        fig = px.histogram(pd.DataFrame(data), x="source", title="📊 Document Contribution to Knowledge Base")
        st.plotly_chart(fig, use_container_width=True)
