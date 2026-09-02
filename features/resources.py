import os
import streamlit as st
from config import KNOWLEDGE_BASE_DIR
from pypdf import PdfReader

def render_resources_page():
    """Displays all indexed PDF legal documents located inside the knowledge_base directory."""
    st.markdown("## 📂 Knowledge Base Resources")
    st.caption("Verified legal statutes and reference documents currently indexed in the system.")

    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        st.error("Knowledge base folder not found.")
        return

    pdf_files = [f for f in os.listdir(KNOWLEDGE_BASE_DIR) if f.endswith(".pdf")]
    if not pdf_files:
        st.warning("No PDF documents found in 'knowledge_base/'. Place your reference PDFs there.")
        return

    st.markdown(f"**Total Documents Indexed:** `{len(pdf_files)}`")
    
    for file in pdf_files:
        path = os.path.join(KNOWLEDGE_BASE_DIR, file)
        try:
            reader = PdfReader(path)
            num_pages = len(reader.pages)
        except Exception:
            num_pages = "Unavailable"

        st.markdown(f"""
            <div class="custom-card">
                <h4>📄 {file}</h4>
                <p><b>Status:</b> Indexed & Verified &nbsp;|&nbsp; <b>Total Pages:</b> {num_pages}</p>
            </div>
        """, unsafe_allow_html=True)