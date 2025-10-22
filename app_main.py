import streamlit as st
from core.ingestion import load_pdfs
from core.vector_store import build_faiss_index, retrieve_context
from core.synthesis import synthesize_across_docs
from ui.layout import set_custom_style, show_header, show_footer
from ui.components import show_upload_instructions, show_document_chart
import hashlib



# ------------------------- PAGE CONFIG -------------------------
st.set_page_config(
    page_title="Retrieval Augmented Generation Synthesizer",
    page_icon="🧩",
    layout="wide",
)

# ------------------------- LOAD STYLE -------------------------
set_custom_style()
show_header()

# ------------------------- FILE UPLOAD -------------------------
def get_file_hash(files):
    """Create a unique hash for uploaded files to detect changes."""
    file_hash = hashlib.md5()
    for f in files:
        file_hash.update(f.read())
        f.seek(0)  # Reset pointer
    return file_hash.hexdigest()

uploaded_files = st.file_uploader("📄 Upload your PDF research papers", type=["pdf"], accept_multiple_files=True)

@st.cache_resource(show_spinner=False)
def process_and_index_pdfs(files):
    """Cache the FAISS index so it doesn't rebuild each time."""
    chunks = load_pdfs(files)
    db, emb_model = build_faiss_index(chunks)
    return chunks, db, emb_model

if uploaded_files:
    file_hash = get_file_hash(uploaded_files)

    if "last_hash" not in st.session_state or st.session_state.last_hash!=file_hash:
        with st.spinner("Processing and indexing documents... ⏳"):
            chunks, db, emb_model = process_and_index_pdfs(uploaded_files)
            st.session_state.last_hash = file_hash
            st.session_state.chunks = chunks
            st.session_state.db = db
            st.session_state.emb_model = emb_model
    else:
        chunks = st.session_state.chunks
        db = st.session_state.db
        emb_model = st.session_state.emb_model

    st.success(f"✅ Indexed **{len(chunks)}** text chunks from **{len(uploaded_files)}** PDF(s).")
    st.markdown("---")

    tab1, tab2 = st.tabs(["💬 Ask a Question", "📊 Document Insights"])

    # ------------------------- TAB 1: Q&A -------------------------
    with tab1:
        st.subheader("🔍 Ask a research question")
        st.caption("Example: *Compare dropout vs. quantization methods in deep learning*")

        query = st.text_input("Enter your question below:", key="user_query")
        if query:
            with st.spinner("Retrieving relevant content..."):
                context = retrieve_context(db, emb_model, query)
            with st.spinner("Generating synthesized insight..."):
                answer = synthesize_across_docs(context, query)

            st.markdown("### 🧩 Synthesized Insight")
            # st.markdown(
            #     f"<div style='background-color:#F5F5FF; padding:15px; border-radius:10px; font-size:16px;'>{answer}</div>",
            #     unsafe_allow_html=True,
            # )/
            # --- Adaptive styling for visibility and error handling ---
            if "Error" in answer or "Exception" in answer:
                bg_color = "#FFEBEE"   # light red
                text_color = "#B00020"  # dark red
            else:
                bg_color = "#F5F5FF"   # light blue-gray
                text_color = "#000000"  # black

            st.markdown(
                f"""
                <div style='
                    background-color:{bg_color};
                    color:{text_color};
                    padding:15px;
                    border-radius:10px;
                    font-size:16px;
                    white-space:pre-wrap;
                '>{answer}</div>
                """,
                unsafe_allow_html=True,
            )
            # st.session_state.user_query = ""

    # ------------------------- TAB 2: DOCUMENT STATS -------------------------
    with tab2:
        st.subheader("📊 Document Contribution to Knowledge Base")
        show_document_chart(chunks)

else:
    show_upload_instructions()

show_footer()
