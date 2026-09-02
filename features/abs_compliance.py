import streamlit as st
from rag.retriever import retrieve_relevant_documents
from rag.generator import generate_grounded_response

def render_abs_compliance_page(vector_store):
    """Access and Benefit Sharing (ABS) & National Biodiversity Authority (NBA) checker."""
    st.markdown("## 🌱 Access & Benefit Sharing (ABS) Compliance")
    st.caption("Guidance under the Biological Diversity Act, 2002 and National Biodiversity Authority (NBA) regulations.")

    with st.form("abs_form"):
        applicant_type = st.radio("Applicant Entity Type:", ["Indian Citizen / Entity without foreign participation", "Foreign Entity / NRI / Indian company with foreign shareholding (Section 3(2))"])
        activity = st.multiselect("Intended Commercial/Research Activity:", ["Commercial Utilization", "Bio-survey and Bio-utilization", "Applying for Patent inside/outside India (Section 6)", "Transfer of Research Results (Section 4)"])
        source_origin = st.radio("Sourcing of Biological Resource:", ["Directly from local growers / cultivators / BMCs", "Purchased from local market as normal trade commodity", "Cultivated on private land"])

        run_abs = st.form_submit_button("Check ABS Requirements", use_container_width=True)

    if run_abs:
        with st.spinner("Evaluating compliance steps under Biological Diversity Act..."):
            query = f"Determine ABS requirements under Biological Diversity Act 2002 for {applicant_type} engaging in {', '.join(activity)} sourced via {source_origin}. State required Forms (Form I, Form II, Form III), SBB approvals, and benefit sharing obligations."
            chunks, conf = retrieve_relevant_documents(vector_store, query, top_k=4)
            abs_guidance = generate_grounded_response(
                query=query,
                retrieved_chunks=chunks,
                jurisdiction=st.session_state.jurisdiction,
                language=st.session_state.language
            )

        st.markdown("### 📌 ABS Compliance Checklist & Authority Routing")
        st.markdown(abs_guidance)

        if chunks:
            with st.expander("📚 Biodiversity Act Citations"):
                for c in chunks:
                    st.markdown(f"**{c['source']} (Page {c['page']})**")
                    st.caption(c['text'])