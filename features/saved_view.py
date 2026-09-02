import streamlit as st

def render_saved_page():
    """Manages bookmarked and saved answers."""
    st.markdown("## 🔖 Saved Answers & Bookmarks")
    st.caption("Access all saved responses, citations, and legal summaries.")

    if not st.session_state.saved_items:
        st.info("No answers bookmarked yet. Use the 'Save Answer' button in the chat view to bookmark key responses.")
        return

    for idx, item in enumerate(st.session_state.saved_items):
        st.markdown(f"""
            <div class="custom-card">
                <small>Saved on: {item['timestamp']} | Jurisdiction: {item.get('jurisdiction', 'India')}</small>
                <h4>Q: {item['question']}</h4>
                <p>{item['answer']}</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([8, 2])
        with col2:
            if st.button("Remove Bookmark", key=f"del_saved_{idx}"):
                st.session_state.saved_items.pop(idx)
                st.rerun()