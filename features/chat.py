import streamlit as st
import datetime
from rag.retriever import retrieve_relevant_documents
from rag.generator import generate_grounded_response

def render_chat_page(vector_store):
    st.markdown("## Namaste! I'm IP-SAKTI Sahayak")
    st.caption("Your multilingual, source-cited AI assistant for Intellectual Property & Regulatory Guidance in Ayurveda.")

    # Emojis removed for a clean, Enterprise look
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Classify Product", use_container_width=True):
            st.session_state.active_page = "Classify Formulation"
            st.rerun()
    with col2:
        if st.button("IPR Guidance", use_container_width=True):
            st.session_state.active_page = "IPR Guidance"
            st.rerun()
    with col3:
        if st.button("ABS Compliance", use_container_width=True):
            st.session_state.active_page = "ABS Compliance"
            st.rerun()
    with col4:
        if st.button("Prior Art Search", use_container_width=True):
            st.session_state.active_page = "TKDL / Prior Art Search"
            st.rerun()

    st.markdown(
        '<div class="disclaimer-badge" style="border-left: 3px solid #4ADE80; padding-left: 10px; color: #D1D5DB; font-size: 0.85rem; margin-top: 15px;"><b>Legal Notice:</b> IP-SAKTI Sahayak provides informational guidance grounded in indexed statutes. It does not constitute formal legal counsel.</div>',
        unsafe_allow_html=True
    )

    # --- NEW FEATURE: HUMAN ESCALATION PATH (Sidebar) ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("##### 👩‍⚖️ Expert Support")
    if st.sidebar.button("📞 Escalate to Human IP Expert", use_container_width=True):
        st.sidebar.success("Escalation Triggered! Connecting to AIIA IP Facilitation Desk... (Simulated)")
        st.sidebar.caption("Session transcript securely forwarded. An expert will assist you shortly.")
    # ----------------------------------------------------

    # FILLING THE DEAD SPACE: Show suggestions only if chat is empty
    if not st.session_state.current_chat:
        st.write("")
        st.write("")
        st.markdown("##### 💡 Suggested Queries to try:")
        st.caption("• What is the rule regarding the aggregation or duplication of known properties of traditionally known components?")
        st.caption("• What are the provisions regarding the constitution of the Ayurvedic, Siddha and Unani Drugs Technical Advisory Board?")
        st.caption("• What is the procedure for seeking prior approval of the National Biodiversity Authority for biological resources?")

    # Render Current Conversation
    for idx, item in enumerate(st.session_state.current_chat):
        with st.chat_message("user", avatar="🧑‍💻"):
            # BACK TO NATIVE STREAMLIT UI
            st.write(item["question"])
            
        with st.chat_message("assistant", avatar="🌿"):
            st.markdown(item["answer"])
            
            conf = item.get("confidence", "None")
            conf_color = {"High": "🟢", "Medium": "🟡", "Low": "🔴", "None": "⚪"}.get(conf, "⚪")
            st.caption(f"Evidence Grounding: {conf_color} **{conf}** | Jurisdiction Context: **{item.get('jurisdiction', 'India')}**")
            
            if item.get("sources"):
                with st.expander("View Cited Sources & Page Excerpts"):
                    for s_idx, src in enumerate(item["sources"], 1):
                        st.markdown(f"**[{s_idx}] {src['source']} — Page {src['page']}**")
                        st.markdown(f"> *\"{src['text']}\"*")
                        st.divider()

            if st.button(f"Save Answer #{idx+1}", key=f"save_btn_{idx}"):
                st.session_state.saved_items.append({
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "question": item["question"],
                    "answer": item["answer"],
                    "sources": item.get("sources", []),
                    "jurisdiction": item.get("jurisdiction", "India")
                })
                st.toast("Answer saved to Bookmarks!", icon="✅")

    # Chat Input Box
    user_query = st.chat_input("Try: 'What is the rule regarding the aggregation of traditionally known components?'")
    if user_query:
        with st.chat_message("user", avatar="🧑‍💻"):
            # BACK TO NATIVE STREAMLIT UI
            st.write(user_query)

        with st.chat_message("assistant", avatar="🌿"):
            with st.spinner("Retrieving verified legal passages and analyzing context..."):
                retrieved_chunks, confidence = retrieve_relevant_documents(vector_store, user_query, top_k=4)
                answer = generate_grounded_response(
                    query=user_query,
                    retrieved_chunks=retrieved_chunks,
                    jurisdiction=st.session_state.jurisdiction,
                    language=st.session_state.language
                )
                st.markdown(answer)

            chat_record = {
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "question": user_query,
                "answer": answer,
                "sources": retrieved_chunks,
                "confidence": confidence,
                "jurisdiction": st.session_state.jurisdiction
            }
            st.session_state.current_chat.append(chat_record)
            st.session_state.all_history.append(chat_record)
            st.rerun()