# NEBULA: Environment Setup & Execution Guide

This document provides the exact, verified instructions to configure, run, test, and build the **NEBULA: Intelligent Astronomical Data Visualization & Exploration Platform** across Windows, macOS, and Linux.

---

## 1. Prerequisites

Before starting, ensure the following runtimes are installed on your workstation:

| Prerequisite | Minimum Version | Recommended / Tested | Verification Command |
| :--- | :--- | :--- | :--- |
| **Python** | `3.10+` | `3.14.0` (with pre-built wheels) | `python --version` |
| **Node.js** | `18.0+` | `22.x` or `24.x` | `node --version` |
| **npm** | `9.0+` | `10.x+` | `npm --version` |
| **Git** | `2.30+` | `2.40+` | `git --version` |

---

## 2. One-Click Demonstration Launch (Windows)

For rapid local evaluation, batch scripts are provided in the repository root:

- **Launch Everything**: Double-click `start_all.bat` or run:
  ```powershell
  .\start_all.bat
  ```
  *(Launches FastAPI on port 8000, Vite React on port 5173, and opens your default browser).*

- **Backend Only**: Double-click `start_backend.bat` or run:
  ```powershell
  .\start_backend.bat
  ```

- **Frontend Only**: Double-click `start_frontend.bat` or run:
  ```powershell
  .\start_frontend.bat
  ```

---

## 3. Manual Step-by-Step Installation

### Step 3.1: Backend Setup

1. **Navigate to the backend directory**:
   ```powershell
   cd d:\CODING\Projects\backend
   ```
   *(On Linux/macOS: `cd backend`)*

2. **Create the Python virtual environment**:
   ```powershell
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\activate
     ```
   - **Windows (Command Prompt)**:
     ```cmd
     .\venv\Scripts\activate.bat
     ```
   - **Linux / macOS (Bash / Zsh)**:
     ```bash
     source venv/bin/activate
     ```

4. **Install backend dependencies**:
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   *Note: Packages installed include `fastapi`, `uvicorn`, `pydantic`, `pydantic-settings`, `sqlalchemy`, `numpy`, `scipy`, `pandas`, `astropy`, `rebound`, `httpx`, and `python-multipart`.*

5. **Start the backend development server**:
   ```powershell
   python run.py
   ```
   *Or directly using Uvicorn:*
   ```powershell
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   - **API Health Endpoint**: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)
   - **Interactive Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **OpenAPI JSON**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

### Step 3.2: Frontend Setup

1. **Open a new terminal and navigate to the frontend directory**:
   ```powershell
   cd d:\CODING\Projects\frontend
   ```
   *(On Linux/macOS: `cd frontend`)*

2. **Install frontend npm dependencies**:
   ```powershell
   npm install
   ```

3. **Start the Vite development server**:
   ```powershell
   npm run dev
   ```
   - **Frontend Application UI**: [http://localhost:5173](http://localhost:5173)
   *(Vite automatically proxies all `/api` requests to `http://127.0.0.1:8000`).*

---

## 4. Running the Automated Test Suites

### Backend Test Suite (pytest)
To execute all 117 automated unit and integration tests covering data models, physical calculations, N-body integrators, AI grounding, and research evaluation:

```powershell
cd d:\CODING\Projects\backend
.\venv\Scripts\activate
pytest
```
*Or using the Python binary directly:*
```powershell
.\venv\Scripts\python.exe -m pytest -v
```

**Expected Result**:
```
====================== 117 passed, 12 warnings in ~7.7s =======================
```

### Frontend Code Quality & Linting
To check TypeScript and code quality standards using Oxlint:
```powershell
cd d:\CODING\Projects\frontend
npm run lint
```
**Expected Result**: `Found 0 errors.`

---

## 5. Building the Production Frontend

To compile and bundle the production-ready static assets:

```powershell
cd d:\CODING\Projects\frontend
npm run build
```

This runs `tsc -b && vite build`:
- Validates all TypeScript types across 58 source files.
- Generates the production bundle in `frontend/dist/`.
- Optimizes CSS and JavaScript chunks.

To preview the production build locally:
```powershell
npm run preview
```
Accessible at [http://localhost:4173](http://localhost:4173).

---

## 6. Environment Configuration (`.env`)

NEBULA is designed to work **completely offline with zero configuration** using its local seed catalog (23 bodies) and deterministic astronomical knowledge synthesis engine.

To customize settings or enable remote LLM providers, copy the template:
```powershell
# In project root
cp .env.example .env

# Or in backend directory
cd backend
cp .env.example .env
```

### Available Environment Variables:
```env
# Server
ENVIRONMENT=development
DEBUG=True
PORT=8000
HOST=0.0.0.0

# Database
DATABASE_URL=sqlite:///./nebula.db

# Simulation Engine Default (ias15 | whfast | leapfrog)
DEFAULT_INTEGRATOR=ias15

# Optional AI Provider Configuration
# Supported options: auto | gemini | openai | anthropic | ollama | fallback
DEFAULT_AI_PROVIDER=auto
GEMINI_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
OLLAMA_BASE_URL=http://localhost:11434
```

---

## 7. Containerized Local Deployment (Docker)

To run the complete platform inside isolated Docker containers:

```bash
# In the project root (requires Docker & Docker Compose)
docker-compose up --build
```

- **Frontend Container**: [http://localhost:5173](http://localhost:5173) (served via Nginx).
- **Backend Container**: [http://localhost:8000](http://localhost:8000) (served via FastAPI / Uvicorn).
- **Stop Containers**: `docker-compose down`.

---

## 8. Verification Checklist

After setup, verify system integrity:
1. `GET http://127.0.0.1:8000/api/health` returns `{"status": "healthy"}`.
2. `GET http://127.0.0.1:8000/api/v1/objects` returns 23 celestial objects.
3. [http://localhost:5173/explorer](http://localhost:5173/explorer) displays the interactive catalog table and 3D preview.
4. [http://localhost:5173/simulation](http://localhost:5173/simulation) computes N-body trajectories with energy conservation drift plotted.
5. Mode switcher in TopNav toggles between Citizen, Student, and Researcher views.
