import streamlit as st
from pathlib import Path

def set_custom_style():
    """Inject custom CSS styling into Streamlit."""
    css_path = Path(__file__).parent / "theme.css"
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def show_header():
    """Display app header."""
    st.markdown('<h1 class="main-title">🧠 InsightBridge: AI Research Synthesizer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Upload multiple research papers and explore synthesized insights using open-source models.</p>', unsafe_allow_html=True)
    st.markdown("---")

def show_footer():
    """Display footer."""
    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:#888;'>Built with ❤️ using LangChain, Hugging Face, and Streamlit.</p>",
        unsafe_allow_html=True,
    )
