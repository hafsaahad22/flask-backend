# citationRetrieval.py
# This module loads the cleaned Constitution text and matches articles to user queries using similarity.

import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load pre-cleaned Constitution articles
def load_constitution_articles(path='data/processed/cleaned_constitution.json'):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found.")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Find matching articles based on user query
def search_constitution_articles(user_query, top_n=2):
    articles = load_constitution_articles()

    # Safely access 'text' and 'title', skip articles missing both
    texts = []
    titles = []
    for article in articles:
        text = article.get('text', '').strip()
        title = article.get('title', 'No Title')
        if text:  # only include articles with non-empty text
            texts.append(text)
            titles.append(title)

    if not texts:
        return [{"title": "No results found", "excerpt": "No matching constitutional articles found."}]

    vectorizer = TfidfVectorizer().fit_transform([user_query] + texts)
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()

    results = []
    for idx in similarity.argsort()[::-1][:top_n]:
        results.append({
            "title": titles[idx],
            "excerpt": texts[idx][:300] + "...",
        })

    return results
