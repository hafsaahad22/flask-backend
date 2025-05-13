# config.py

# This file contains configuration settings for the Flask application.
# It includes paths for the PDFs and other configurations.
import os

class Config:
    # Add paths for your PDFs and output folders
    PDF_FOLDER_PATH = os.path.join(os.getcwd(), 'data/raw/supreme_court_cases')
    OUTPUT_FOLDER_PATH = os.path.join(os.getcwd(), 'data/cleaned/supreme_court_cases_cleaned')


import os

class Config:
    """Basic configuration class for the app."""
    
    # Path to the Constitution PDF
    CONSTITUTION_PDF_PATH = os.path.join(os.path.dirname(__file__), 'data', 'raw', 'constitution', 'constitution.pdf')
    
    # Path to the Supreme Court Cases PDF
    SUPREME_COURT_CASES_PDF_PATH = os.path.join(os.path.dirname(__file__), 'data', 'raw', 'supreme_court_cases', 'supreme_cases.pdf')

    # Example: add API keys, or any other sensitive configurations here
    # Example:
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-default-secret-key'
    
    # For local testing, you can set a debug mode
    DEBUG = True
