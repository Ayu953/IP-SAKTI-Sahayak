from typing import List, Dict
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODELS

def get_active_gemini_model():
    """Configures and initializes a supported Gemini generative model instance."""
    if not GEMINI_API_KEY:
        return None
    genai.configure(api_key=GEMINI_API_KEY)
    
    for model_name in GEMINI_MODELS:
        try:
            return genai.GenerativeModel(model_name)
        except Exception:
            continue
    return genai.GenerativeModel("gemini-1.5-flash")

def generate_grounded_response(
    query: str, 
    retrieved_chunks: List[Dict], 
    jurisdiction: str, 
    language: str
) -> str:
    """Generates a strictly source-grounded answer using Google Gemini."""
    model = get_active_gemini_model()
    if model is None:
        return "⚠️ Gemini API Key not configured. Please set GEMINI_API_KEY in your `.env` file."

    if not retrieved_chunks:
        return (
            "I could not find relevant legal or regulatory information in the available knowledge base "
            "to answer this question accurately."
        )

    # Format retrieved evidence into structured numbered blocks
    context_blocks = []
    for idx, chunk in enumerate(retrieved_chunks, 1):
        block = f"[SOURCE {idx}]\nDocument: {chunk['source']}\nPage: {chunk['page']}\nPassage:\n{chunk['text']}"
        context_blocks.append(block)

    formatted_context = "\n\n━━━━━━━━━━━━━━━━━━━━\n\n".join(context_blocks)

    system_prompt = f"""
You are IP-SAKTI Sahayak, an AI legal and regulatory assistant for Ayurveda.

OPERATIONAL CONSTRAINTS:
1. Ground your answer EXCLUSIVELY in the provided context passages. Do not invent provisions, rules, or sections.
2. If the context does not contain sufficient evidence to answer the query, clearly state:
   "I cannot verify this information from the available knowledge base."
3. Distinguish between explicit statutory evidence and logical inference.
4. Active Jurisdiction Context: {jurisdiction}. If Jurisdiction is 'India', prioritize Indian acts (Patents Act 1970, Biological Diversity Act 2002, Drugs & Cosmetics Act 1940). If 'International', evaluate treaties (CBD, Nagoya Protocol, WIPO/TRIPS).
5. Target Output Language: {language}. If Language is Hindi, answer fluently in Hindi while keeping official legal statutes/acts in their standard official form.
6. MANDATORY: Explicitly cite sources at the bottom or in-text referring to the provided Document names and Page numbers.
7. NEVER give definitive legal clearances. Use phrases such as "Based on the retrieved sources...", "The available documents suggest...".

CONTEXT PASSAGES:
{formatted_context}

USER QUESTION:
{query}
"""

    try:
        response = model.generate_content(system_prompt)
        return response.text
    except Exception as e:
        return f"⚠️ An error occurred while generating the response: {str(e)}"