import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Streamlit Cloud (secrets) ya Local (.env / environment) dono se safely key uthayega
try:
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

KNOWLEDGE_BASE_DIR = "knowledge_base"
FAISS_INDEX_DIR = "faiss_index"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Priority fallback list - Tested & Verified for Sep 2026
GEMINI_MODELS = [
    "gemini-3.8-flash",       # Sabse latest (No traffic issues)
    "gemini-3.7-flash",       # Highly stable backup
    "gemini-3.6-flash",       # Backup 2
    "gemini-3.5-flash-lite"   # Low-latency subagent (Final fallback)
]