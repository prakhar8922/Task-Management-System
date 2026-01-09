@echo off
title Test Fixed Monolith
color 0E

echo.
echo ========================================
echo   Testing Fixed Monolith Setup
echo ========================================
echo.

echo [INFO] Cleaning old builds...
cd frontend
if exist "dist" rmdir /s /q dist
if exist "..\backend\static" rmdir /s /q "..\backend\static"

echo [INFO] Building React frontend...
call npm run build
if errorlevel 1 (
    echo [ERROR] Frontend build failed
    pause
    exit /b 1
)

echo [SUCCESS] Frontend built successfully
echo [INFO] Checking build output...
dir dist\

cd ..
echo [INFO] Setting up backend...
cd backend
call ..\venv\Scripts\activate.bat

echo [INFO] Installing backend dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Backend dependencies failed
    pause
    exit /b 1
)

echo [SUCCESS] Backend dependencies installed
echo [INFO] Running migrations...
python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Migration failed
    pause
    exit /b 1
)

echo [SUCCESS] Migrations completed
echo [INFO] Collecting static files...
python manage.py collectstatic --no-input --clear
if errorlevel 1 (
    echo [ERROR] Static file collection failed
    pause
    exit /b 1
)

echo [SUCCESS] Static files collected
echo [INFO] Checking static files...
dir static\

echo.
echo ========================================
echo   Starting Fixed Monolith Server
echo ========================================
echo.
echo Your app will be available at:
echo   http://127.0.0.1:8000/
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver
