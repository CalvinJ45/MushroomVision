@echo off
echo ==========================================
echo   Starting Mushroom Application System
echo ==========================================

echo.
echo 0. Checking & Installing Dependencies...
echo    - Python dependencies...
pip install -r backend\requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo    WARNING: Failed to install Python dependencies. Ensure python is installed.
    pause
)

echo    - Checking Node.js modules...
if not exist "computervision\node_modules" (
    echo    - node_modules not found. Installing...
    cd computervision
    call npm install
    cd ..
) else (
    echo    - node_modules found. Skipping install.
)

echo.
echo 1. Starting Backend Server...
start "Mushroom Backend" cmd /k "cd backend && python app.py"

echo.
echo 2. Starting Frontend Application...
start "Mushroom Frontend" cmd /k "cd computervision && npm run dev"

echo.
echo ==========================================
echo   Both services are starting...
echo   Backend will be at: http://localhost:5000
echo   Frontend will be at: http://localhost:3000
echo ==========================================
