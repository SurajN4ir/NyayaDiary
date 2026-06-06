import sys
import os

# Automatically add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), "nyayadiary-backend")
sys.path.append(backend_path)

# Import the FastAPI app from the backend folder
from main import app
