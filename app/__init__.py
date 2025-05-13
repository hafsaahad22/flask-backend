# __init__.py

# This file initializes the Flask application.
# It does the following:
# 1. Creates a Flask app instance.
# 2. Enables CORS to allow communication between the backend and the Wix frontend.
# 3. Registers routes from routes.py using Flask's Blueprint system to keep the app modular.
# 4. Returns the Flask app instance to be used in the app startup (run.py).

# Import necessary modules for creating the Flask app
from flask import Flask
from flask_cors import CORS  # type: ignore # CORS allows cross-origin requests, essential for Wix frontend

# This function initializes the Flask app and registers routes
def create_app():
    # Create a new Flask app instance
    app = Flask(__name__)

    # Enable CORS for all routes, allowing frontend (Wix) to make requests to this backend
    CORS(app)

    # Import routes from routes.py (the actual route definitions)
    from .routes import main  # Import the Blueprint for handling routes

    # Register the imported routes (Blueprint) to the app
    app.register_blueprint(main)

    # Return the Flask app instance, now set up with routes and CORS
    return app
