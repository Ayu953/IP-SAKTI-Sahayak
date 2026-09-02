import os
import hashlib
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import KNOWLEDGE_BASE_DIR, FAISS_INDEX_DIR, EMBEDDING_MODEL_NAME

def get_knowledge_base_hash() -> str:
    """Computes an MD5 hash of all filenames and modification times in knowledge_base."""
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)
        return ""
    
    files = sorted(os.listdir(KNOWLEDGE_BASE_DIR))
    hash_str = ""
    for file in files:
        if file.endswith(".pdf"):
            path = os.path.join(KNOWLEDGE_BASE_DIR, file)
            hash_str += f"{file}_{os.path.getmtime(path)}_"
    return hashlib.md5(hash_str.encode()).hexdigest()

def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

def build_or_load_vector_store():
    """Loads existing FAISS vector store or rebuilds it if PDFs have changed."""
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)

    pdf_files = [f for f in os.listdir(KNOWLEDGE_BASE_DIR) if f.endswith(".pdf")]
    if not pdf_files:
        return None, "No PDF documents found in 'knowledge_base/' directory."

    embeddings = get_embedding_model()
    current_hash = get_knowledge_base_hash()
    hash_file_path = os.path.join(FAISS_INDEX_DIR, "kb_hash.txt")

    # Check if a cached FAISS index exists with a matching hash
    if os.path.exists(FAISS_INDEX_DIR) and os.path.exists(hash_file_path):
        with open(hash_file_path, "r") as f:
            cached_hash = f.read().strip()
        if cached_hash == current_hash:
            try:
                vector_store = FAISS.load_local(
                    FAISS_INDEX_DIR, 
                    embeddings, 
                    allow_dangerous_deserialization=True
                )
                return vector_store, "Loaded cached index."
            except Exception:
                pass  # Rebuild if corrupted

    # Ingest PDFs and preserve exact page numbers and filenames
    loader = PyPDFDirectoryLoader(KNOWLEDGE_BASE_DIR)
    documents = loader.load()

    if not documents:
        return None, "Unable to extract text from the PDF documents in 'knowledge_base/'."

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)

    vector_store = FAISS.from_documents(chunks, embeddings)
    
    # Cache vector store to disk
    os.makedirs(FAISS_INDEX_DIR, exist_ok=True)
    vector_store.save_local(FAISS_INDEX_DIR)
    with open(hash_file_path, "w") as f:
        f.write(current_hash)

    return vector_store, f"Successfully indexed {len(chunks)} chunks from {len(pdf_files)} document(s)."