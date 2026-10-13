# NEBULA Setup & Deployment Guide

This guide describes how to install, configure, verify, and run the complete NEBULA platform locally.

---

## 1. System Requirements

- **Operating System**: Windows 10/11, macOS (12+), or Linux (Ubuntu 20.04+)
- **Python**: Version 3.10 or newer (tested on Python 3.14)
- **Node.js**: Version 18 or newer (tested on Node v24)
- **RAM**: 4 GB minimum (8 GB recommended)
- **GPU**: Any standard integrated or discrete GPU supporting WebGL 2.0

---

## 2. One-Click Launch (Windows)

The simplest way to start the entire system is using the provided batch launcher:
```powershell
.\start_all.bat
```
This launches:
1. The FastAPI scientific backend on `http://localhost:8000`
2. The Vite React client on `http://localhost:5173`
3. Opens the platform directly in your web browser.

---

## 3. Manual Step-by-Step Installation

### 3.1 Backend Installation

1. Navigate to the `backend` directory:
   ```powershell
   cd d:\CODING\Projects\backend
   ```
2. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Verify backend functionality with the test suite:
   ```powershell
   python test_backend.py
   ```
   *Expected output: `>>> ALL NEBULA BACKEND SUBSYSTEM TESTS PASSED WITH 100% SUCCESS!`*

5. Run the backend server:
   ```powershell
   python run.py
   ```
   *Runs on `http://127.0.0.1:8000`. Swagger API docs available at `http://127.0.0.1:8000/docs`.*

---

### 3.2 Frontend Installation

1. Open a new terminal in the `frontend` directory:
   ```powershell
   cd d:\CODING\Projects\frontend
   ```
2. Install npm dependencies:
   ```powershell
   npm install
   ```
3. Run the development server:
   ```powershell
   npm run dev
   ```
4. Access the web interface at `http://localhost:5173`.

---

## 4. Optional Environment Variables (`.env`)

To enable external cloud LLMs (Gemini or OpenAI), create a `.env` file in `backend/.env`:

```env
# Optional External AI Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Database (defaults to local SQLite)
DATABASE_URL=sqlite:///./nebula.db

# Simulation default integrator (ias15, whfast, leapfrog)
DEFAULT_INTEGRATOR=ias15
```

> **Note**: If no API keys are provided, NEBULA automatically runs its high-precision deterministic knowledge synthesis engine offline with zero configuration required!

---

## 5. Troubleshooting & Verification

- **Port 8000 already in use**:
  Ensure no other instance of FastAPI or uvicorn is running, or edit `backend/run.py` to change the port number.
- **WebGL Hardware Acceleration**:
  Ensure WebGL is enabled in your browser settings (`chrome://gpu` or `edge://gpu`).
- **Data Cache Reset**:
  If you ever need to reset the local database, delete `backend/nebula.db`. The application will automatically recreate and re-seed the full catalog on next launch.
