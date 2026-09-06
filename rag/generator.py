from typing import List, Dict
import os
from google import genai
# YAHAN DHYAN DE: Humne config se GEMINI_MODELS list import kar li hai
from config import GEMINI_API_KEY, GEMINI_MODELS 

def get_genai_client():
    """Initializes the new official google.genai client."""
    if not GEMINI_API_KEY:
        return None
    return genai.Client(api_key=GEMINI_API_KEY)

def generate_grounded_response(
    query: str, 
    retrieved_chunks: List[Dict], 
    jurisdiction: str, 
    language: str
): 
    # (Note: Maine -> str hata diya hai kyunki ab yeh stream/generator return karega)
    """Generates a strictly source-grounded answer using the Fallback Loop and Streaming."""
    client = get_genai_client()
    if client is None:
        yield "⚠️ Gemini API Key not configured. Please check your settings."
        return

    if not retrieved_chunks:
        yield (
            "I could not find relevant legal or regulatory information in the available knowledge base "
            "to answer this question accurately."
        )
        return

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

    # ====================================================
    # 🚀 THE FIX: SMART FALLBACK LOOP + STREAMING
    # ====================================================
    last_error_message = ""
    
    # Ek-ek karke config.py wale models ko try karega
    for model_name in GEMINI_MODELS:
        try:
            # 1. generate_content_stream use kiya (Streaming On)
            response_stream = client.models.generate_content_stream(
                model=model_name,
                contents=system_prompt,
            )
            
            # 2. Streamlit ko string format me data chahiye hota hai, 
            # isliye hum explicitly chunk.text yield kar rahe hain
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
            
            # Agar bina error ke stream complete ho gayi, toh loop yahi khatam kardo
            return 
            
        except Exception as e:
            # Agar 503/429 error aaya ya connection latka, toh turant fail hokar next par jayega
            last_error_message = str(e)
            print(f"Model {model_name} failed. Switching to next... Error: {last_error_message}")
            continue 

    # Agar list ke saare models fail ho jayein
    yield f"⚠️ All Google servers are currently busy. Last error: {last_error_message}"