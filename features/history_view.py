import streamlit as st

def render_history_page():
    """Renders active session chat history with restore options."""
    st.markdown("## 🕒 Session Chat History")
    st.caption("Review previous queries and answers from the current application session.")

    if not st.session_state.all_history:
        st.info("No queries recorded in this session yet.")
        return

    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.all_history = []
            st.session_state.current_chat = []
            st.rerun()

    for idx, item in enumerate(reversed(st.session_state.all_history), 1):
        st.markdown(f"""
            <div class="custom-card">
                <small>Timestamp: {item.get('timestamp', 'N/A')} | Regime: {item.get('jurisdiction', 'India')}</small>
                <h4>Q: {item['question']}</h4>
                <p>{item['answer']}</p>
            </div>
        """, unsafe_allow_html=True)