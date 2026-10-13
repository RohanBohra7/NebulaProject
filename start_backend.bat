@echo off
echo ========================================================
echo NEBULA: Intelligent Astronomical Exploration Platform
echo Starting Python Scientific Backend (FastAPI + REBOUND)
echo ========================================================
cd /d "%~dp0backend"
call venv\Scripts\activate.bat
python run.py
pause
