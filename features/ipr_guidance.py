import streamlit as st
from rag.retriever import retrieve_relevant_documents
from rag.generator import generate_grounded_response

def render_ipr_guidance_page(vector_store):
    """Interactive IPR Pathway Evaluator addressing Section 3(p), novelty, and GI/TM options."""
    st.markdown("## 📜 Intellectual Property Rights (IPR) Guidance")
    st.caption("Evaluate patentability barriers (Section 3(p)), Traditional Knowledge restrictions, and alternative IP mechanisms.")

    ip_type = st.selectbox(
        "Select Target IP Protection Route:",
        ["Patent", "Geographical Indication (GI)", "Trademark", "Trade Secret", "Plant Variety Protection"]
    )

    with st.form("ipr_eval_form"):
        novelty_claim = st.text_area("Describe the novelty or technical improvement over known traditional knowledge:", placeholder="E.g., Novel synergistic composition of Ashwagandha and Piperine showing enhanced bioavailability for neuroprotection.")
        traditional_use = st.radio("Is this therapeutic use documented in public domain literature/Ayurvedic texts?", ["Yes, well documented", "No, previously unknown property", "Partially documented"])
        bio_source = st.checkbox("Uses biological material accessed from India", value=True)

        evaluate = st.form_submit_button("Evaluate IPR Feasibility", use_container_width=True)

    if evaluate:
        with st.spinner("Cross-referencing Patents Act Section 3(p) and TKDL prior art guidelines..."):
            query = f"Evaluate {ip_type} feasibility for an Ayurvedic formulation claiming: '{novelty_claim}'. Traditional knowledge status: {traditional_use}. Biological material from India: {bio_source}. Detail Section 3(p) implications, inventive step hurdles, and NBA requirements."
            chunks, conf = retrieve_relevant_documents(vector_store, query, top_k=4)
            ipr_analysis = generate_grounded_response(
                query=query,
                retrieved_chunks=chunks,
                jurisdiction=st.session_state.jurisdiction,
                language=st.session_state.language
            )

        st.markdown("### ⚖️ IPR Evaluation & Strategy")
        st.markdown(ipr_analysis)

        if chunks:
            with st.expander("📚 Statutory Sources"):
                for c in chunks:
                    st.markdown(f"**{c['source']} — Page {c['page']}**")
                    st.caption(c['text'])