import time
import json
import os
import streamlit as st
from streamlit_lottie import st_lottie

# --- STREAMLIT SECRETS CONFIGURATION FOR CLOUD ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
except Exception:
    # Local development fallback agar .env use kar rahe ho
    pass

from rag.ingestion import build_or_load_vector_store
from ui.theme import apply_custom_theme
from ui.sidebar import render_sidebar

# Import Feature Views
from features.chat import render_chat_page
from features.classification import render_classification_page
from features.ipr_guidance import render_ipr_guidance_page
from features.abs_compliance import render_abs_compliance_page
from features.tkdl_search import render_tkdl_search_page
from features.regulatory_pathways import render_regulatory_pathways_page
from features.resources import render_resources_page
from features.history_view import render_history_page
from features.saved_view import render_saved_page

# --- STREAMLIT CONFIGURATION ---
st.set_page_config(
    page_title="IP-SAKTI Sahayak",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- APPLY THEME ---
apply_custom_theme()

# --- SESSION STATE INITIALIZATION ---
if "splash_shown" not in st.session_state:
    st.session_state.splash_shown = False
if "current_chat" not in st.session_state:
    st.session_state.current_chat = []
if "all_history" not in st.session_state:
    st.session_state.all_history = []
if "saved_items" not in st.session_state:
    st.session_state.saved_items = []
if "jurisdiction" not in st.session_state:
    st.session_state.jurisdiction = "India"
if "language" not in st.session_state:
    st.session_state.language = "English"
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home / Chat"
if "show_about_dialog" not in st.session_state:
    st.session_state.show_about_dialog = False
if "show_help_dialog" not in st.session_state:
    st.session_state.show_help_dialog = False

# ==========================================
# 🎬 THE SPLASH SCREEN LOGIC (Netflix Style)
# ==========================================
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Error: Could not find '{filepath}'. Make sure it's in the same folder as app.py")
        return None

if not st.session_state.splash_shown:
    # Ek empty container banayenge jisko baad me destroy kar sakein
    splash_placeholder = st.empty()
    
    with splash_placeholder.container():
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 4, 3])
        with col2:
            # Yahan direct local file call kar li hai
            lottie_anim = load_lottiefile("animation.json")
            if lottie_anim:
                st_lottie(lottie_anim, height=300, key="splash_logo")
            
            st.markdown("<h2 style='text-align: center; color: #00E5FF; text-shadow: 0 0 10px #00E5FF;'>IP-SAKTI Sahayak</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #D1D5DB;'>Initializing Knowledge Engine...</p>", unsafe_allow_html=True)
    
    # 2.5 Second ka pause taaki animation smoothly dikhe aur backend load ho jaye
    time.sleep(2.8)
    
    # Container ko destroy karke app ko aage badhne do
    splash_placeholder.empty()
    st.session_state.splash_shown = True

# ==========================================
# 🚀 MAIN APP EXECUTION (Runs after Splash)
# ==========================================

# --- LOAD RAG VECTOR STORE (CACHED) ---
@st.cache_resource(show_spinner=False)
def initialize_knowledge_engine():
    return build_or_load_vector_store()

vector_store, status_msg = initialize_knowledge_engine()

# --- RENDER SIDEBAR NAVIGATION ---
active_page = render_sidebar()

# --- MODAL DIALOGS ---
if st.session_state.show_about_dialog:
    st.markdown("""
        <div class="custom-card">
            <h3>🌿 About IP-SAKTI Sahayak</h3>
            <p><b>Project Title:</b> A multilingual, RAG-based AI assistant for Intellectual Property & Regulatory Guidance in Ayurveda across national and international regimes.</p>
            <p><b>Developed For:</b> Smart India Hackathon (SIH) 2026</p>
            <p><b>Team:</b> Team TechTonic</p>
            <p><b>Developer:</b> Ayush Kawalkar (ID: 0832CS241047)</p>
            <p><b>Architecture:</b> Hybrid RAG (HuggingFace Embeddings + FAISS Local Cache + Gemini Generative AI).</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Close About Dialog"):
        st.session_state.show_about_dialog = False
        st.rerun()

if st.session_state.show_help_dialog:
    st.markdown("""
        <div class="custom-card">
            <h3>❓ System Usage Guide</h3>
            <ul>
                <li><b>Home / Chat:</b> Ask natural legal questions and receive answers with cited sources and page numbers.</li>
                <li><b>Jurisdiction Switch:</b> Toggle between India and International regimes to tailor citations.</li>
                <li><b>Language Selector:</b> Switch output language between English and Hindi without distorting official statute names.</li>
                <li><b>Workflows:</b> Use dedicated tabs for Product Classification, Patentability evaluation, and ABS compliance.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Close Help Dialog"):
        st.session_state.show_help_dialog = False
        st.rerun()

# --- MAIN ROUTING ENGINE ---
if active_page == "Home / Chat":
    render_chat_page(vector_store)
elif active_page == "Classify Formulation":
    render_classification_page(vector_store)
elif active_page == "IPR Guidance":
    render_ipr_guidance_page(vector_store)
elif active_page == "ABS Compliance":
    render_abs_compliance_page(vector_store)
elif active_page == "TKDL / Prior Art Search":
    render_tkdl_search_page(vector_store)
elif active_page == "Regulatory Pathways":
    render_regulatory_pathways_page(vector_store)
elif active_page == "Resources":
    render_resources_page()
elif active_page == "Session History":
    render_history_page()
elif active_page == "Saved Answers":
    render_saved_page()