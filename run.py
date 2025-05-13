# run.py

# This file runs the Flask app by calling the create_app function defined in the app/init.py.
# It is the entry point to start the backend server.

from app import create_app

# Create the Flask app using the factory method defined in app/init.py
app = create_app()

# Run the app
if __name__ == "__main__":
     app.run(host='0.0.0.0', port=5000)

