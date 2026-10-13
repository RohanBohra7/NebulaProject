# NEBULA: Intelligent Astronomical Data Visualization & Exploration Platform

[![BTech CSE Capstone](https://img.shields.io/badge/Project-BTech_CSE_Capstone-blue.svg)](file:///d:/CODING/Projects)
[![Python](https://img.shields.io/badge/Backend-Python_3.14_FastAPI-green.svg)](file:///d:/CODING/Projects/backend)
[![React](https://img.shields.io/badge/Frontend-React_19_TypeScript_Vite-cyan.svg)](file:///d:/CODING/Projects/frontend)
[![Three.js](https://img.shields.io/badge/3D_Engine-Three.js_WebGL-orange.svg)](file:///d:/CODING/Projects/frontend/src/components/visualization)
[![REBOUND](https://img.shields.io/badge/N--Body-REBOUND_IAS15_%2B_Symplectic_Leapfrog-purple.svg)](file:///d:/CODING/Projects/backend/app/simulation)

> **NEBULA** is a research-oriented astronomical information, visualization, simulation, and exploration platform. It provides one unified scientific data and computational foundation with three adaptive user interaction modes: **RESEARCHER**, **STUDENT**, and **CITIZEN**.

---

## 🌟 Core Research Contribution

The contribution of NEBULA is **not** claiming the invention of 3D graphics, N-body physics, astronomical databases, or Large Language Models. Rather, the contribution is the **system-level integration and quantitative evaluation** of:

$$\text{Empirical Astronomical Data} + \text{Scientific Computation} + \text{Interactive 3D Visualizer} + \text{Symplectic N-Body Simulation} + \text{Grounded AI} + \text{Adaptive Tri-Persona Interaction}$$

NEBULA makes this adaptive presentation architecture **quantifiably visible and measurable** via live linguistic readability metrics (Flesch-Kincaid Grade Level), technical vocabulary density analysis, mathematical expression density, and empirical data grounding verification.

---

## 🚀 The Three Adaptive Personas

| Capability | 🔬 Researcher Mode | 🎓 Student Mode | 🌌 Citizen Mode |
| :--- | :--- | :--- | :--- |
| **Primary Audience** | Astrophysicists & Scholars | Physics Learners & Educators | General Public & Stargazers |
| **Cognitive Grade Level** | **12.0 – 18.0** (Postgraduate) | **8.5 – 11.0** (High School/College) | **5.0 – 7.0** (Plain Language) |
| **Technical Jargon Density** | **10% – 22%** | **4% – 8%** | **< 3%** |
| **Astrophysical Nomenclature** | Formal LaTeX ($a, e, i, \mu, r_H$) | Guided physical analogies | Everyday relatable scales |
| **Orbital Tools** | Hohmann $\Delta v$, Hill spheres, resonances | Kepler's laws interactive sandbox | Night sky observation guides |
| **Simulation Scope** | Symplectic energy drift ($\Delta E/E_0$) | Guided multi-body orbital tours | Scenic 3D trajectories |
| **AI Assistant Style** | Academic, rigorous derivations | Socratic questioning & quizzes | Inspiring, wonder-filled storytelling |

---

## 📂 System Architecture Overview

```
d:\CODING\Projects/
├── backend/
│   ├── app/
│   │   ├── api/                 # REST endpoints (objects, compare, calculate, simulation, ai, research, data)
│   │   ├── computation/         # Kepler solvers, Cartesian state vectors, Hohmann transfers, Hill spheres, Roche limits
│   │   ├── simulation/          # REBOUND IAS15/WHFast + pure NumPy Symplectic Leapfrog engine
│   │   ├── ai/                  # Provider-agnostic service + grounding pipeline + deterministic fallback engine
│   │   ├── evaluation/          # Readability (FKGL/FRE), technical density, and persona benchmarking
│   │   ├── data/                # High-precision empirical catalog (23 bodies) & adapters (NASA, SIMBAD)
│   │   └── db/                  # SQLite persistence & SQLAlchemy models
│   ├── requirements.txt
│   ├── test_backend.py          # 100% passing test verification suite
│   └── run.py                   # Local backend runner
├── frontend/
│   ├── src/
│   │   ├── components/          # 3D Three.js Solar System, N-Body Canvas, Object Viewer, Layout
│   │   ├── context/             # Global ModeContext (Researcher, Student, Citizen)
│   │   ├── pages/               # 14 complete application pages
│   │   ├── services/            # Typed API client
│   │   └── types/               # TypeScript interfaces
│   ├── package.json
│   └── vite.config.ts           # Vite with /api reverse proxy
├── start_backend.bat            # One-click backend startup script
├── start_frontend.bat           # One-click frontend startup script
└── start_all.bat                # Concurrent one-click platform launch
```

---

## ⚡ Quick Start Instructions

### Prerequisites
- **Python 3.10+** (Tested on Python 3.14 with pre-built scientific wheels)
- **Node.js 18+** & **npm**

### Quick Launch (Windows)
Double-click `start_all.bat` or run in PowerShell:
```powershell
.\start_all.bat
```
This automatically launches the backend at [http://localhost:8000](http://localhost:8000), the frontend at [http://localhost:5173](http://localhost:5173), and opens your default browser.

### Manual Launch

#### 1. Backend Server
```powershell
cd backend
.\venv\Scripts\activate
python run.py
```
* **API Documentation**: Interactive Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Backend Test Suite**: Run `python test_backend.py` (Tests orbital mechanics, N-body IAS15, AI grounding, and evaluation metrics).

#### 2. Frontend Client
```powershell
cd frontend
npm run dev
```
* **Web UI**: Open [http://localhost:5173](http://localhost:5173)

---

## 🔬 Scientific Methodology Highlights

1. **Newton-Raphson Kepler Equation Solver**: Resolves mean anomaly $M = E - e \sin E$ to machine precision ($\epsilon < 10^{-12}$) and maps to 3D Cartesian coordinates $(x, y, z, v_x, v_y, v_z)$.
2. **Dual-Engine N-Body Gravitational Simulation**:
   - **REBOUND IAS15**: 15th-order Gauss-Radau integrator for high-accuracy close encounters.
   - **NumPy Symplectic Leapfrog (Velocity-Verlet)**: Preserves phase-space volume and exhibits zero secular energy decay.
3. **Orbital Mechanics Tools**:
   - Co-planar Hohmann transfer orbits ($\Delta v_1, \Delta v_2$, transfer ellipse, time of flight $\tau$).
   - Hill sphere radius $r_H \approx a(1-e) \sqrt[3]{m/(3M)}$.
   - Rigid & fluid Roche limits for tidal disruption.
   - Mean-motion resonance detector scanning period ratios $p:q$ up to order 8.
4. **Grounded AI Engine**:
   - Every AI prompt is augmented with real empirical parameters extracted from the local catalog and physical calculations.
   - 100% operational offline with zero external API dependencies via the deterministic knowledge synthesis engine.

---

## 📖 Extended Documentation Index
- [ARCHITECTURE.md](file:///d:/CODING/Projects/ARCHITECTURE.md) — Comprehensive architectural specifications.
- [API.md](file:///d:/CODING/Projects/API.md) — Complete REST API reference and payload schemas.
- [SCIENTIFIC_METHODS.md](file:///d:/CODING/Projects/SCIENTIFIC_METHODS.md) — Mathematical formulas and astrophysical derivations.
- [DATA_SOURCES.md](file:///d:/CODING/Projects/DATA_SOURCES.md) — Empirical catalog provenance (NASA, JPL, Gaia DR3).
- [AI.md](file:///d:/CODING/Projects/AI.md) — Grounding pipeline and persona prompt engineering.
- [SIMULATION.md](file:///d:/CODING/Projects/SIMULATION.md) — N-body algorithms and Hamiltonian conservation analysis.
- [RESEARCH_EVALUATION.md](file:///d:/CODING/Projects/RESEARCH_EVALUATION.md) — Quantitative evaluation metrics and experimental findings.
- [SETUP.md](file:///d:/CODING/Projects/SETUP.md) — Full environment installation and configuration guide.
- [NEBULA_IMPLEMENTATION_STATUS.md](file:///d:/CODING/Projects/NEBULA_IMPLEMENTATION_STATUS.md) — Feature status and verification logs.
