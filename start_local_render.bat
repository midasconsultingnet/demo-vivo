@echo off
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
echo Starting Gunicorn server on port 8000...
echo Access the application at http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

REM Run Gunicorn with the WSGI application
gunicorn succes_fuel.wsgi:application --bind 0.0.0.0:8000 --workers 1 --timeout 120