import streamlit as st
from rag.retriever import retrieve_relevant_documents
from rag.generator import generate_grounded_response

def render_regulatory_pathways_page(vector_store):
    """Explores the regulatory approval pathway under AYUSH, CDSCO, and FSSAI."""
    st.markdown("## 🏛️ Regulatory Approval Pathways")
    st.caption("Navigate licensing authorities (State Licensing Authority, CDSCO, FSSAI) based on product category.")

    pathway = st.selectbox(
        "Select Regulatory Pathway to Explore:",
        [
            "Classical Ayurvedic Medicine (Rule 158B - Drugs & Cosmetics Rules)",
            "Patent / Proprietary Ayurvedic Medicine",
            "Phytopharmaceutical Drug (CDSCO New Drug Approval)",
            "Ayurveda Aahar (FSSAI Regulations 2022)",
            "Ayurvedic Cosmetic (Form 32)"
        ]
    )

    if st.button("Generate Regulatory Pathway Guide", use_container_width=True):
        with st.spinner("Fetching regulatory pathway details..."):
            query = f"Outline the licensing procedure, clinical data requirements, application forms, and statutory authority for {pathway}."
            chunks, conf = retrieve_relevant_documents(vector_store, query, top_k=4)
            pathway_guide = generate_grounded_response(
                query=query,
                retrieved_chunks=chunks,
                jurisdiction=st.session_state.jurisdiction,
                language=st.session_state.language
            )

        st.markdown(f"### 📑 Guidance: {pathway}")
        st.markdown(pathway_guide)

        if chunks:
            with st.expander("📚 Regulatory References"):
                for c in chunks:
                    st.markdown(f"**{c['source']} — Page {c['page']}**")
                    st.caption(c['text'])