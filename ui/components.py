import streamlit as st
import plotly.express as px
import pandas as pd

def show_upload_instructions():
    st.info("📂 Upload one or more research PDFs to get started.")
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3588/3588658.png", width=120)
    st.markdown(
        "<p style='text-align:center; color:#777;'>Your uploaded PDFs will be processed locally to build a knowledge base for research synthesis.</p>",
        unsafe_allow_html=True,
    )

def show_document_chart(chunks):
    """Plot document contribution histogram."""
    data = {"source": [c["source"] for c in chunks]}
    fig = px.histogram(
        pd.DataFrame(data),
        x="source",
        title="Document Contribution Overview",
        color="source",
    )
    fig.update_layout(
        xaxis_title="PDF Source",
        yaxis_title="Number of Chunks",
        template="plotly_white",
        showlegend=False,
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)
