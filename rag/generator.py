from typing import List, Dict
import os
from google import genai
from config import GEMINI_API_KEY

def get_genai_client():
    """Initializes the new official google.genai client."""
    if not GEMINI_API_KEY:
        return None
    return genai.Client(api_key=GEMINI_API_KEY)

def get_dynamic_model_name(client) -> str:
    """Automatically finds the best available active model dynamically from Google's servers."""
    try:
        # Naye SDK me models ko list karne ka tareeka
        for m in client.models.list():
            if 'generateContent' in getattr(m, 'supported_generation_methods', []) and 'flash' in m.name:
                return m.name
        for m in client.models.list():
            if 'generateContent' in getattr(m, 'supported_generation_methods', []) and 'pro' in m.name:
                return m.name
    except Exception:
        pass
    
    # Safe fallback
    return "gemini-3.6-flash"

def generate_grounded_response(
    query: str, 
    retrieved_chunks: List[Dict], 
    jurisdiction: str, 
    language: str
) -> str:
    """Generates a strictly source-grounded answer using the new Google GenAI SDK."""
    client = get_genai_client()
    if client is None:
        return "⚠️ Gemini API Key not configured. Please check your settings."

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
        model_name = get_dynamic_model_name(client)
        # Naye SDK ka official generate call
        response = client.models.generate_content(
            model=model_name,
            contents=system_prompt,
        )
        return response.text
    except Exception as e:
        return f"⚠️ An error occurred while generating the response: {str(e)}"