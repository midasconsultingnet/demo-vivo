"""
Script to run the Django application with Waitress server (Windows-compatible alternative to Gunicorn)
"""
import os
import subprocess
import sys
from pathlib import Path

def run_waitress_server():
    # Install waitress if not already installed
    print("Installing waitress...")
    os.system(f"{sys.executable} -m pip install waitress")
    
    # Collect static files first
    print("Collecting static files...")
    os.system(f"{sys.executable} manage.py collectstatic --noinput")
    
    # Run waitress server
    port = os.environ.get('PORT', '8000')
    print(f"Starting Waitress server on port {port}...")
    print("Access the application at http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    
    cmd = [
        sys.executable, "-m", "waitress", "--host=0.0.0.0", f"--port={port}",
        "succes_fuel.wsgi:application"
    ]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nShutting down server...")

if __name__ == "__main__":
    run_waitress_server()