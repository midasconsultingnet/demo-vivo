"""
Script to run the Django application with Gunicorn locally (similar to Render)
"""
import os
import subprocess
import sys
from pathlib import Path

def run_gunicorn_local():
    # Collect static files first
    print("Collecting static files...")
    os.system(f"{sys.executable} manage.py collectstatic --noinput")
    
    # Run gunicorn with local settings
    port = os.environ.get('PORT', '8000')
    print(f"Starting Gunicorn server on port {port}...")
    
    cmd = [
        'gunicorn',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '1',  # Use 1 worker for local development
        '--timeout', '120',
        '--max-requests', '1000',
        '--max-requests-jitter', '100',
        'succes_fuel.wsgi:application'
    ]
    
    # Add environment variable for Django settings
    env = os.environ.copy()
    env['DJANGO_SETTINGS_MODULE'] = 'succes_fuel.settings'
    
    try:
        subprocess.run(cmd, env=env)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        
if __name__ == "__main__":
    run_gunicorn_local()