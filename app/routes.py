# app/routes.py

from flask import Blueprint, request, jsonify
from app.queryHandler import process_query  # use the right file name

main = Blueprint("main", __name__)

@main.route("/query", methods=["POST"])
def handle_query():
    try:
        data = request.get_json()
        query = data.get("query", "").strip()

        if not query:
            return jsonify({"error": "Query cannot be empty."}), 400

        result = process_query(query)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
