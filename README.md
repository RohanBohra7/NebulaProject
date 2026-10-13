# NEBULA: Intelligent Astronomical Data Visualization & Exploration Platform

[![BTech CSE Capstone](https://img.shields.io/badge/Project-BTech_CSE_Capstone-blue.svg)](file:///d:/CODING/Projects)
[![Backend](https://img.shields.io/badge/Backend-Python_3.14_FastAPI-green.svg)](file:///d:/CODING/Projects/backend)
[![Frontend](https://img.shields.io/badge/Frontend-React_19_TypeScript_Vite-cyan.svg)](file:///d:/CODING/Projects/frontend)
[![3D Engine](https://img.shields.io/badge/3D_Engine-Three.js_WebGL-orange.svg)](file:///d:/CODING/Projects/frontend/src/components/visualization)
[![Physics Integrator](https://img.shields.io/badge/N--Body-REBOUND_IAS15_%2B_Symplectic_Leapfrog-purple.svg)](file:///d:/CODING/Projects/backend/app/simulation)
[![License](https://img.shields.io/badge/License-Academic_Research-lightgrey.svg)](file:///d:/CODING/Projects)

> **NEBULA** is a research-oriented platform integrating normalized empirical astronomical datasets, high-precision scientific computation, interactive 3D WebGL visualizations, symplectic N-body gravitational simulations, and a fact-grounded Socratic AI assistant across three adaptive user interaction tiers: **RESEARCHER**, **STUDENT**, and **CITIZEN**.

---

## 1. Project Overview

Modern astronomy tools generally bifurcate into two extremes: either high-density command-line ephemeris solvers (e.g. SPICE, JPL Horizons) inaccessible to non-specialists, or consumer planetarium applications (e.g. Stellarium, Google Sky) that omit rigorous physical derivations, unit systems, and Hamiltonian numerical verification.

**NEBULA** bridges this gap. It provides a single, unified backend computational foundation and empirical catalog (23 normalized celestial bodies), presenting the data through three dynamically calibrated user experiences:
1. **Researcher Mode**: High-density numerical telemetry, formal LaTeX derivations ($a, e, i, \Omega, \omega, \nu$), full Keplerian orbital elements, Hohmann transfer delta-v curves, Hamiltonian energy conservation tracking ($\Delta E / |E_0|$), and academic citations.
2. **Student Mode**: Pedagogical scaffolding, interactive Kepler's laws and Newton's gravity sandboxes, guided orbital tours, comprehension quizzes, and a Socratic AI physics tutor.
3. **Citizen Mode**: Plain-language cosmic narratives, everyday analogies (e.g., flight times and comparative body weight across worlds), cinematic 3D orbital visualizers, and wonder-inspiring curiosity spotlights.

---

## 2. Research Motivation

The academic thesis of NEBULA is:
$$\text{Astronomical Data} + \text{Scientific Computation} + \text{Interactive 3D} + \text{N-Body Simulation} + \text{Grounded AI} + \text{Adaptive Persona Interaction}$$

The platform investigates:
1. **Multi-Persona Cognitive Adaptation**: Can a single empirical dataset adapt its terminology, complexity, and presentation dynamically while guaranteeing mathematical consistency? (Evaluated via live Flesch-Kincaid Grade Level, Coleman-Liau index, and technical jargon density).
2. **AI Grounding Fidelity**: Can conversational astronomical agents eliminate physical hallucination by injecting verified catalog parameters, analytical equations, and N-body trajectories into prompt context?
3. **Symplectic Integration vs. WebGL Performance**: Can high-order gravitational integrators (15th-order Gauss-Radau REBOUND IAS15 and 2nd-order Symplectic Leapfrog) run alongside hardware-accelerated 3D WebGL renderers at 60 FPS without numerical degradation?

---

## 3. Key Features

- **Empirical Astronomical Catalog**: 23 verified celestial bodies across Planets, Moons, Stars, Exoplanets (TRAPPIST-1 system), Asteroids, Comets, and Deep-Sky objects with complete IAU 2015 and CODATA 2018/2022 physical parameters.
- **Parametric Comparison Matrix**: Side-by-side comparative analysis of 2 to 6 celestial worlds, computing exact physical ratios, absolute deltas, percentage differences, Recharts radar charts, and proportional planetary scales.
- **Interactive 3D Keplerian Visualizer**: Hardware-accelerated Three.js / React Three Fiber canvas supporting speed multipliers (1x–500x), focus tracking, true Keplerian elliptic geometry, and dual planetary systems (Solar System and TRAPPIST-1).
- **Dual-Engine N-Body Laboratory**:
  - **REBOUND IAS15**: 15th-order adaptive Gauss-Radau integrator for close gravitational encounters ($\Delta E / |E_0| < 10^{-14}$).
  - **REBOUND WHFast & NumPy Symplectic Leapfrog**: Volume-preserving symplectic integrators exhibiting zero secular energy drift over orbital epochs.
  - **Preconfigured Scenarios**: Sun + Earth, Sun + Earth + Moon, Inner Solar System, Full 9-Body Solar System, TRAPPIST-1 7-planet Laplace resonance chain, Lagrange L4/L5 Trojans, Figure-8 Choreography, and Chaotic 3-Body Pythagorean system.
- **Grounded AI Astronomy Assistant**:
  - Provider-agnostic engine supporting Google Gemini, OpenAI, Anthropic, Ollama, and an offline deterministic knowledge engine.
  - Grounding pipeline that strictly segregates `[NEBULA Data]`, `[Computed Result]`, `[External Scientific Context]`, and `[General Explanation]`.
- **Tri-Persona Adaptation**:
  - Live mode switcher across TopNav, Sidebar, Mode Hub, and Settings.
  - Dynamically altered readability metrics, nomenclature, and UI density.
- **Research Evaluation Benchmarks**:
  - 6 canonical evaluation benchmark tasks with interactive stopwatch tracking.
  - 9-point scientific empirical validation suite comparing calculated properties to IAU/NASA ground truth with explicit physical tolerances ($\pm\epsilon$).
  - Non-sensitive operational telemetry and zero-PII guarantee.

---

## 4. Architecture

```
+-------------------------------------------------------------------------------------------------+
|                                     FRONTEND PRESENTATION LAYER                                 |
|                                                                                                 |
|   [ Researcher Workspace ]            [ Student Learning Hub ]            [ Citizen Space ]     |
|   - Astrometric telemetry             - Kepler sandbox                    - Plain language      |
|   - Formal LaTeX expressions          - Guided tours                      - Everyday analogies  |
|   - Hamiltonian energy drift          - Socratic AI tutor                 - 3D planetarium      |
+-------------------------------------------------------------------------------------------------+
                                                 ^
                                                 |  (ModeContext & Query Parameters)
+-------------------------------------------------------------------------------------------------+
|                                    GROUNDED AI SERVICE LAYER                                    |
|                                                                                                 |
|   - Provider Abstraction: Gemini | OpenAI | Anthropic | Ollama | Local Deterministic Engine     |
|   - Tool Registry: get_object, compare_objects, calculate_orbital_property, explain_simulation  |
|   - Response Validator: Distinguishes empirical data, computed results, and scientific context |
+-------------------------------------------------------------------------------------------------+
                                                 ^
                                                 |  (Grounded Parameters & Analytical Solvers)
+-------------------------------------------------------------------------------------------------+
|                                  SCIENTIFIC & SIMULATION ENGINE                                 |
|                                                                                                 |
|   - Astropy Bridge: IAU 2015 / CODATA 2018 constants and unit-aware conversions                |
|   - Orbital Mechanics: Vis-Viva, Hohmann Delta-v, Hill spheres, Roche limits, Resonances        |
|   - N-Body Dynamics: REBOUND IAS15/WHFast + NumPy Symplectic Leapfrog (Velocity-Verlet)        |
+-------------------------------------------------------------------------------------------------+
                                                 ^
                                                 |  (Empirical Relational Queries)
+-------------------------------------------------------------------------------------------------+
|                                     ASTRONOMICAL DATA LAYER                                     |
|                                                                                                 |
|   - High-Precision Local Seed Catalog (23 bodies) & SQLite Database                            |
|   - External Adapters: NASA JPL Horizons, NASA Exoplanet Archive TAP, SIMBAD CDS Strasbourg   |
|   - Quality Assurance: Volume-density, surface gravity, thermodynamics, and Astropy validation |
+-------------------------------------------------------------------------------------------------+
```

For complete architectural details, see [ARCHITECTURE.md](file:///d:/CODING/Projects/ARCHITECTURE.md).

---

## 5. Technology Stack

### Backend Stack
- **Runtime**: Python 3.10+ (tested on Python 3.14.0)
- **Web Framework**: FastAPI (asynchronous ASGI framework)
- **Data Validation & Settings**: Pydantic v2 & `pydantic-settings`
- **Database ORM**: SQLAlchemy 2.0 with SQLite engine (`nebula.db`)
- **Astrophysics & Units**: Astropy 6.0+ (IAU 2015 constants)
- **Numerical Solvers**: SciPy 1.15+ & NumPy 2.2+
- **N-Body Dynamics**: REBOUND 4.4+ (IAS15, WHFast, Symplectic Leapfrog)
- **Testing**: pytest (117 automated unit and integration tests)

### Frontend Stack
- **Runtime & Toolchain**: Node.js 18+ (tested on Node v22/v24) & Vite 6.0+
- **UI Framework**: React 19 with TypeScript 5.7+
- **3D Graphics**: Three.js, React Three Fiber (`@react-three/fiber`), and Drei (`@react-three/drei`)
- **Styling**: Tailwind CSS (custom cosmic glassmorphism theme)
- **Charts & Telemetry**: Recharts 2.15+ (SVG/Canvas multi-series and radar charts)
- **Icons**: Lucide React
- **Linter**: Oxlint (0 errors)

---

## 6. Screenshots Section Placeholder

> *Screenshots demonstrating the multi-persona user interface across viewports:*

| View | Mode | Description |
| :--- | :--- | :--- |
| **Interactive 3D Visualizer** | Citizen | Real-time Keplerian orbital visualizer showing the Solar System with time-multiplier controls. |
| **Kepler's Laws Sandbox** | Student | Interactive sliders for semi-major axis ($a$) and eccentricity ($e$) calculating aphelion/perihelion velocities. |
| **Direct Parametric Matrix** | Researcher | Side-by-side comparative matrix of 4 worlds with Astropy unit conversions and radar chart. |
| **N-Body Laboratory** | Researcher | REBOUND IAS15 trajectory canvas with Hamiltonian energy conservation drift plot ($\Delta E / \|E_0\|$). |
| **Grounded AI Assistant** | Student | Socratic AI physics tutor highlighting grounded data pills and scientific distinctions. |
| **Research Dashboard** | Researcher | Multi-persona readability divergence curves (FKGL) and NASA JPL empirical benchmark validation. |

*(Visual capture assets are stored in `frontend/public/screenshots/`)*

---

## 7. Setup & Installation

For a step-by-step setup guide, see [SETUP.md](file:///d:/CODING/Projects/SETUP.md).

### Quick Launch (Windows)
Double-click `start_all.bat` or run in PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_all.ps1
```

### Manual Installation

#### 1. Backend Setup
```powershell
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate   # Windows
# source venv/bin/activate # Linux/macOS

# Install requirements
pip install -r requirements.txt

# Start backend server
python run.py
```
Backend API will be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000) (Swagger docs at `/docs`).

#### 2. Frontend Setup
```powershell
# In a new terminal, navigate to frontend directory
cd frontend

# Install npm dependencies
npm install

# Start Vite development server
npm run dev
```
Frontend will be accessible at [http://localhost:5173](http://localhost:5173).

---

## 8. Development Workflow

- **Backend Development**: Auto-reloads using `uvicorn app.main:app --reload` on port 8000.
- **Frontend Development**: Instant HMR using Vite dev server on port 5173 with automatic `/api` proxying.
- **Code Standards**:
  - Python: PEP 8 guidelines, typed Pydantic models, and strict docstrings.
  - TypeScript: Strict typing, zero `any` in public APIs, and Oxlint code quality verification.

---

## 9. Automated Testing

### Backend Test Suite
The backend includes 117 automated unit and integration tests covering data models, physical calculations, N-body integrators, AI grounding, and research evaluation:
```powershell
cd backend
.\venv\Scripts\python.exe -m pytest
```
*Current Status: 117 passed, 100% green (~7.7s).*

### Frontend Linting & Build Verification
```powershell
cd frontend
# Check code quality and rules
npm run lint

# Build production bundle (TypeScript type-checking + Vite build)
npm run build
```
*Current Status: 0 lint errors, 0 build errors (3,070 modules transformed).*

---

## 10. Environment Variables

NEBULA requires **zero API keys** to run completely offline. If you wish to enable remote LLM providers, configure `.env` based on `.env.example`:

```env
# ====================================================================
# NEBULA Environment Configuration
# ====================================================================

ENVIRONMENT=development
DEBUG=True
PORT=8000
HOST=0.0.0.0

# Database (defaults to local SQLite database)
DATABASE_URL=sqlite:///./nebula.db

# N-Body Simulation Default Integrator (ias15 | whfast | leapfrog)
DEFAULT_INTEGRATOR=ias15

# Optional AI Provider Configuration
DEFAULT_AI_PROVIDER=auto
GEMINI_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
OLLAMA_BASE_URL=http://localhost:11434
```

See [.env.example](file:///d:/CODING/Projects/.env.example) for documentation on every parameter.

---

## 11. AI Configuration & Offline Resilience

NEBULA features a provider-agnostic AI subsystem (`backend/app/ai/`):
- **Automatic Provider Detection**: When `DEFAULT_AI_PROVIDER=auto`, the system checks for `GEMINI_API_KEY`, then `OPENAI_API_KEY`, then `ANTHROPIC_API_KEY`, and falls back to the local deterministic engine.
- **Local Deterministic Fallback**: If no keys are provided or network is offline, NEBULA uses its embedded knowledge engine to generate grounded, persona-tailored answers with verified mathematical calculations.
- **Zero Secrets Policy**: Never commit `.env` to source control. The repository includes an active `.gitignore` protecting credentials and database files.

For architecture and grounding details, see [AI.md](file:///d:/CODING/Projects/AI.md).

---

## 12. Deployment

### Local Containerized Deployment (Docker & Docker Compose)
The project includes production-ready Docker configurations for one-command containerized local demonstration:
```bash
# Build and launch both backend and frontend containers
docker-compose up --build
```
- Frontend: Accessible at [http://localhost:5173](http://localhost:5173) (served via Nginx).
- Backend: Accessible at [http://localhost:8000](http://localhost:8000) (served via Uvicorn).

### Production Cloud Deployment Guidance
- **Backend (Render / Railway / AWS ECS / GCP Cloud Run)**:
  - Run container using `backend/Dockerfile` or as a Python web service with `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
  - Set `ENVIRONMENT=production` and `DATABASE_URL` (persistent SQLite volume or PostgreSQL).
- **Frontend (Vercel / Netlify / Cloudflare Pages)**:
  - Connect repository with build command `npm run build` and output directory `dist`.
  - Configure reverse proxy or set `VITE_API_URL` to point to the backend domain.

---

## 13. Limitations & Future Scope

While NEBULA achieves high empirical fidelity and multi-persona integration, the following physical and computational limitations are documented:
1. **Unperturbed Keplerian Visualizer**: The real-time 3D orbit visualizer uses analytical Keplerian orbital elements at epoch J2000.0 rather than live relativistic numerical integration to ensure smooth 60 FPS client performance.
2. **Point-Mass Gravitation**: N-body simulations treat celestial bodies as spherically symmetric point masses, omitting non-spherical gravitational harmonics ($J_2, J_4$), tidal dissipation, and general relativistic frame dragging.
3. **Coplanar Assumptions in Hohmann Tool**: The Hohmann transfer calculator models coplanar circular-to-circular transfers; real interplanetary missions require non-coplanar Lambert targeters with gravitational slingshots.
4. **Offline AI Knowledge Breadth**: The deterministic fallback engine focuses strictly on the 23 catalog bodies and standard astrophysics questions; open-ended queries outside astrophysics require an external LLM key.

---

## 📖 Complete Documentation Index

- [SETUP.md](file:///d:/CODING/Projects/SETUP.md) — Comprehensive environment setup and verification manual.
- [ARCHITECTURE.md](file:///d:/CODING/Projects/ARCHITECTURE.md) — Detailed specifications for all 8 subsystems.
- [API.md](file:///d:/CODING/Projects/API.md) — Complete REST API reference for all implemented endpoints.
- [DATA_SOURCES.md](file:///d:/CODING/Projects/DATA_SOURCES.md) — Empirical catalog provenance, units, and limitations.
- [SCIENTIFIC_METHODS.md](file:///d:/CODING/Projects/SCIENTIFIC_METHODS.md) — Mathematical formulas and astrophysical derivations.
- [SIMULATION.md](file:///d:/CODING/Projects/SIMULATION.md) — N-body algorithms, integrators, and scenarios.
- [AI.md](file:///d:/CODING/Projects/AI.md) — Grounded AI architecture, tools, and persona prompts.
- [RESEARCH_EVALUATION.md](file:///d:/CODING/Projects/RESEARCH_EVALUATION.md) — Empirical benchmarks, tasks, and telemetry methodology.
- [NEBULA_IMPLEMENTATION_STATUS.md](file:///d:/CODING/Projects/NEBULA_IMPLEMENTATION_STATUS.md) — Detailed phase-by-phase implementation tracking.
