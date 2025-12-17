@echo off
echo ==========================================
echo   Starting Mushroom Application System
echo ==========================================

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
