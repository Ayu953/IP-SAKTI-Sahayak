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

# Agar ek nahi chala toh dusra chalega.
GEMINI_MODELS = ["gemini-3.6-flash", "gemini-1.5-flash", "gemini-pro"]