import re
import json
from app.citationRetrieval import search_constitution_articles
from app.pdfCaseExtractor import search_supreme_court_cases

# Load lawyer data
def load_lawyer_data(path='data/lawyers/lawyers.json'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

# Recommend lawyers based on query keywords
def recommend_lawyers(query, max_results=3):
    lawyers = load_lawyer_data()
    query_lower = query.lower()
    
    # Filter lawyers by specialization matching query
    filtered = [
        lawyer for lawyer in lawyers
        if lawyer.get("specialization") and lawyer["specialization"].lower() in query_lower
    ]
    
    # Fallback: return top experienced lawyers if no specialization match
    if not filtered:
        filtered = sorted(lawyers, key=lambda l: l.get("experience", 0), reverse=True)

    return filtered[:max_results]

def process_query(query):
    """
    Processes the legal query to extract matching constitutional articles,
    supreme court cases, and recommend relevant lawyers.
    """
    matched_articles = search_constitution_articles(query)
    matched_cases = search_supreme_court_cases(query)
    recommended_lawyers = recommend_lawyers(query)

    response = {
        "query": query,
        "matched_articles": matched_articles,
        "matched_cases": matched_cases,
        "recommended_lawyers": recommended_lawyers
    }

    return response
