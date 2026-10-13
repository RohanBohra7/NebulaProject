@echo off
echo ========================================================
echo NEBULA: Intelligent Astronomical Data Exploration Platform
echo Starting All Services (Backend and Frontend)...
echo ========================================================
start "NEBULA Backend (FastAPI)" cmd /c "%~dp0start_backend.bat"
timeout /t 3 /nobreak > nul
start "NEBULA Frontend (Vite)" cmd /c "%~dp0start_frontend.bat"
timeout /t 2 /nobreak > nul
start http://localhost:5173
echo.
echo NEBULA services started!
echo Backend Docs: http://localhost:8000/docs
echo Frontend App: http://localhost:5173
echo.
