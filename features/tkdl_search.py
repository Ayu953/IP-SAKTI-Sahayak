import streamlit as st
from rag.retriever import retrieve_relevant_documents

def render_tkdl_search_page(vector_store):
    """Local Knowledge Base Prior-Art Explorer."""
    st.markdown("## 📚 Prior-Art & Knowledge Base Search")
    st.caption("Search local indexed documents for traditional formulations, prior claims, and statutory definitions.")

    search_query = st.text_input("Enter Formulation Name, Herb (Sanskrit/Botanical), or Therapeutic Keyword:", "Curcuma longa wound healing")

    if st.button("Search Knowledge Base", use_container_width=True):
        if not search_query.strip():
            st.warning("Please enter a valid search term.")
            return

        with st.spinner("Searching indexed vector database..."):
            chunks, conf = retrieve_relevant_documents(vector_store, search_query, top_k=6)

        if not chunks:
            st.info("No matching records found in the local knowledge base.")
            return

        st.markdown(f"### 🔎 Found {len(chunks)} Relevant Prior-Art Passages")
        for idx, chunk in enumerate(chunks, 1):
            st.markdown(f"""
                <div class="source-box">
                    <b>[{idx}] {chunk['source']}</b> &nbsp;|&nbsp; <b>Page {chunk['page']}</b> &nbsp;|&nbsp; Relevance Score: <code>{chunk['score']:.4f}</code>
                    <p style="margin-top: 8px; font-style: italic;">"{chunk['text']}"</p>
                </div>
            """, unsafe_allow_html=True)