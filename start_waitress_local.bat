@echo off
echo Installing waitress...
pip install waitress

echo.
echo Setting up environment for Render-like local run...
echo.

REM Collect static files
python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo Error collecting static files
    pause
    exit /b %errorlevel%
)

echo.
echo Starting Waitress server on port 8000...
echo Access the application at http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

REM Run Waitress server (Windows-compatible alternative to Gunicorn)
python -m waitress --host=0.0.0.0 --port=8000 succes_fuel.wsgi:application