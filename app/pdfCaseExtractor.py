# pdfCaseExtractor.py
# This module loads cleaned Supreme Court cases and matches relevant ones to user queries using similarity.

import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load cleaned Supreme Court case data
def load_supreme_court_cases(path='data/processed/cleaned_cases.json'):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found.")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Find relevant cases based on user query
def search_supreme_court_cases(user_query, top_n=2):
    cases = load_supreme_court_cases()

    # Safely access 'text' and 'title', skip cases with empty text
    texts = []
    titles = []
    for case in cases:
        text = case.get('text', '').strip()
        title = case.get('title', 'Untitled Case')
        if text:
            texts.append(text)
            titles.append(title)

    if not texts:
        return [{"title": "No results found", "summary": "No relevant Supreme Court cases found."}]

    vectorizer = TfidfVectorizer().fit_transform([user_query] + texts)
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()

    results = []
    for idx in similarity.argsort()[::-1][:top_n]:
        results.append({
            "title": titles[idx],
            "summary": texts[idx][:300] + "...",
        })

    return results
