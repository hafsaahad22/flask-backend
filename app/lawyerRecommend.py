import json
import os
import re

LAWYER_DB_PATH = 'data/lawyers/lawyers.json'  # Ensure this file exists

def extract_specialization_and_location(query):
    """
    Extracts specialization and location from the user's query.
    
    Args:
    - query (str): The user query text.
    
    Returns:
    - tuple: (specialization, location) extracted from the query.
    """
    # A simple set of keywords for specialization and location (can be extended)
    specialization_keywords = ['criminal', 'civil', 'corporate', 'family', 'tax', 'property']
    location_keywords = ['karachi', 'lahore', 'islamabad', 'peshawar', 'multan', 'quetta']
    
    specialization = None
    location = None
    
    # Convert the query to lowercase for easier matching
    query_lower = query.lower()

    # Extract specialization from the query
    for keyword in specialization_keywords:
        if keyword in query_lower:
            specialization = keyword
            break  # We take the first match, can be adjusted as per need

    # Extract location from the query
    for location_name in location_keywords:
        if location_name in query_lower:
            location = location_name
            break  # We take the first match, can be adjusted as per need

    return specialization, location


def recommend_lawyers_based_on_query(query):
    """
    Recommend lawyers based on the user's query.
    
    Args:
    - query (str): The user's query text.
    
    Returns:
    - list: List of matching lawyer profiles.
    """
    if not os.path.exists(LAWYER_DB_PATH):
        return {"error": "Lawyer database not found."}

    with open(LAWYER_DB_PATH, 'r', encoding='utf-8') as f:
        lawyers = json.load(f)

    # Extract specialization and location from the user's query
    specialization, location = extract_specialization_and_location(query)

    filtered = []

    # Iterate through the lawyer profiles and filter based on the extracted specialization and location
    for lawyer in lawyers:
        match = True
        if specialization and specialization.lower() not in lawyer.get("specialization", "").lower():
            match = False
        if location and location.lower() not in lawyer.get("location", "").lower():
            match = False
        if match:
            filtered.append(lawyer)

    return filtered if filtered else [{"message": "No matching lawyers found."}]

# Example query
query = "I need a criminal lawyer in Lahore"
recommended_lawyers = recommend_lawyers_based_on_query(query)

# Output result (can be integrated into your app's response handling)
print(json.dumps(recommended_lawyers, ensure_ascii=False, indent=2))
