from typing import List, Dict, Tuple

def retrieve_relevant_documents(vector_store, query: str, top_k: int = 4) -> Tuple[List[Dict], str]:
    """
    Performs similarity search with distance scores and computes evidence confidence.
    Distance metric: L2 Euclidean distance (lower is closer).
    """
    if vector_store is None:
        return [], "None"

    results_with_score = vector_store.similarity_search_with_score(query, k=top_k)
    if not results_with_score:
        return [], "None"

    retrieved_chunks = []
    distances = []

    for doc, distance in results_with_score:
        distances.append(distance)
        page_num = doc.metadata.get("page", 0) + 1  # 1-based index
        source_name = doc.metadata.get("source", "Unknown Document")
        source_clean = source_name.replace("knowledge_base/", "").replace("knowledge_base\\", "")
        
        retrieved_chunks.append({
            "source": source_clean,
            "page": page_num,
            "text": doc.page_content.strip(),
            "score": float(distance)
        })

    # Confidence calculation based on best matching chunk distance
    best_dist = distances[0]
    if best_dist < 0.85:
        confidence = "High"
    elif best_dist < 1.30:
        confidence = "Medium"
    else:
        confidence = "Low"

    return retrieved_chunks, confidence