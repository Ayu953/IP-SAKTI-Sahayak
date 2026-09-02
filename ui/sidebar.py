import streamlit as st

def render_sidebar():
    """Renders the functional left sidebar and returns selected settings and active route."""
    with st.sidebar:
        st.markdown("### 🌿 IP-SAKTI Sahayak")
        st.caption("AI Assistant for Intellectual Property & Regulatory Guidance in Ayurveda")
        st.divider()

        # Primary Navigation
        pages = [
            "Home / Chat",
            "Classify Formulation",
            "IPR Guidance",
            "ABS Compliance",
            "TKDL / Prior Art Search",
            "Regulatory Pathways",
            "Resources",
            "Session History",
            "Saved Answers"
        ]
        
        default_index = 0
        if "active_page" in st.session_state and st.session_state.active_page in pages:
            default_index = pages.index(st.session_state.active_page)

        selected_page = st.radio("Navigation", pages, index=default_index, label_visibility="collapsed")
        st.session_state.active_page = selected_page

        st.divider()
        st.subheader("⚙️ System Controls")

        # Functional Jurisdiction Toggle
        jurisdiction = st.radio(
            "Jurisdiction Regime:",
            ["🇮🇳 India (National)", "🌐 International"],
            index=0 if st.session_state.get("jurisdiction", "India") == "India" else 1
        )
        st.session_state.jurisdiction = "India" if "India" in jurisdiction else "International"

        # Functional Language Selector
        language = st.selectbox(
            "Response Language:",
            ["English", "Hindi (हिंदी)"],
            index=0 if st.session_state.get("language", "English") == "English" else 1
        )
        st.session_state.language = language

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("ℹ️ About", use_container_width=True):
                st.session_state.show_about_dialog = True
        with col2:
            if st.button("❓ Help", use_container_width=True):
                st.session_state.show_help_dialog = True

        st.caption("SIH 2026 | Team TechTonic")

    return selected_page