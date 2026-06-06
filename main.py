import sys
import os
import importlib.util

# Automatically add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), "nyayadiary-backend")
sys.path.append(backend_path)

# Load the backend main.py module under a unique namespace to prevent circular import name collision
spec = importlib.util.spec_from_file_location("backend_main", os.path.join(backend_path, "main.py"))
backend_main = importlib.util.module_from_spec(spec)
sys.modules["backend_main"] = backend_main
spec.loader.exec_module(backend_main)

# Expose the app object for uvicorn
app = backend_main.app
