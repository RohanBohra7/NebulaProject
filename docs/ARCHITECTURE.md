# NEBULA Architecture Documentation

## 1. System Philosophy & Design Goals

NEBULA is architected around a strict principle: **One Common Scientific Foundation, Three Adaptive Presentations**.
Rather than constructing separate silos for researchers, students, and citizens, NEBULA uses an integrated data and computational pipeline where:
1. Physical and orbital calculations are executed with zero approximation compromises.
2. The empirical data layer acts as the single source of ground truth.
3. The presentation, terminology, visual scales, and AI explanations dynamically scale along the cognitive continuum:
   - **Researcher**: High cognitive complexity, quantitative units, LaTeX expressions, peer-reviewed citations.
   - **Student**: Guided educational scaffolding, physical analogies, Kepler's laws sandboxes, active-learning quizzes.
   - **Citizen**: Visually rich, plain English, relatable everyday comparisons, night sky stargazing tips.

```
+-----------------------------------------------------------------------------------------+
|                                    PRESENTATION LAYER                                   |
|                                                                                         |
|   [ Researcher View ]             [ Student View ]                 [ Citizen View ]     |
|   Formal Astrophysics             Guided Educational Sandbox       Stargazing & Wonder  |
|   FKGL: 12 - 18                   FKGL: 8.5 - 11                   FKGL: 5 - 7          |
|   Jargon: 10 - 22%                Jargon: 4 - 8%                   Jargon: < 3%         |
+-----------------------------------------------------------------------------------------+
                                             ^
                                             |  (ModeContext & Adaptive Transformers)
+-----------------------------------------------------------------------------------------+
|                                GROUNDED AI SERVICE LAYER                                |
|                                                                                         |
|   Provider-Agnostic Engine: Gemini | OpenAI | Ollama | Deterministic Fallback           |
|   Grounding Pipeline: Injects verified empirical parameters & orbital mechanics results |
+-----------------------------------------------------------------------------------------+
                                             ^
                                             |  (Dynamically Injected Context)
+-----------------------------------------------------------------------------------------+
|                               COMPUTATION & SIMULATION ENGINE                           |
|                                                                                         |
|   - Keplerian State Vector Converter (a, e, i, Omega, omega, nu)                        |
|   - Hohmann Transfer Orbit Solver (Delta v1, Delta v2, tau)                             |
|   - Hill Sphere & Roche Limit Calculators                                               |
|   - Orbital Resonance Commensurability Scanner                                          |
|   - Dual N-Body Simulator: REBOUND IAS15/WHFast + NumPy Symplectic Leapfrog (Verlet)    |
+-----------------------------------------------------------------------------------------+
                                             ^
                                             |  (Empirical Queries)
+-----------------------------------------------------------------------------------------+
|                                 EMPIRICAL DATA LAYER                                    |
|                                                                                         |
|   - 23 Curated Scientific Bodies (Planets, Moons, Stars, Exoplanets, Deep Sky)          |
|   - Source Adapters: Local Verified Cache, NASA Exoplanet Archive TAP, SIMBAD CDS       |
|   - SQLite Database + SQLAlchemy Models                                                 |
+-----------------------------------------------------------------------------------------+
```

---

## 2. Component Breakdown

### 2.1 Backend (`/backend`)
- **FastAPI Core**: Asynchronous REST service mounted at `/api` with CORS middleware and auto-generated OpenAPI documentation.
- **Data Layer (`/app/data`)**:
  - `seed_data.py`: High-precision empirical astronomical catalog containing 23 celestial objects with orbital elements and physical properties.
  - `sources.py`: Modular adapter design supporting local cache, NASA Exoplanet Archive TAP API, and SIMBAD with automated fallbacks.
  - `catalog.py`: Querying, filtering, and database synchronization.
- **Computation Layer (`/app/computation`)**:
  - `orbital_mechanics.py`: Kepler solvers, Cartesian state vector conversions, Hohmann transfer orbits, Hill spheres, Roche limits, and Lagrange points.
  - `ephemeris.py`: 3D Keplerian ellipse trajectory sampling and ephemeris time propagation.
- **Simulation Layer (`/app/simulation`)**:
  - `nbody_engine.py`: Integrates REBOUND (IAS15, WHFast) and pure NumPy Symplectic Leapfrog fallback.
  - `scenarios.py`: 7 scientific initial-condition scenarios (Solar System Inner, Earth-Moon-Sun, TRAPPIST-1 Resonance, Lagrange Trojans, Figure-8 Choreography, Chaotic 3-Body, Binary Star).
  - `conservation.py`: Hamiltonian total energy $E = T + V$, angular momentum vector $\mathbf{L}$, and relative energy drift $\Delta E / |E_0|$.
- **Grounded AI Layer (`/app/ai`)**:
  - `personas.py`: Linguistic guidelines and prompt engineering for Researcher, Student, and Citizen modes.
  - `grounding.py`: Context extraction that scans queries, extracts empirical figures, and attaches them to the prompt.
  - `service.py`: Provider-agnostic engine with fallback to the deterministic knowledge engine.
- **Research Evaluation Layer (`/app/evaluation`)**:
  - `metrics.py`: Computes Flesch-Kincaid Grade Level, Flesch Reading Ease, and technical vocabulary density.
  - `evaluator.py`: Orchestrates parallel multi-persona queries and generates comparative benchmark telemetry.

### 2.2 Frontend (`/frontend`)
- **React 19 + TypeScript**: Modular component hierarchy with strict typing.
- **Three.js**: Custom WebGL rendering for 3D planetary orbits, celestial bodies, and N-body trajectories with smooth 60 FPS performance.
- **Tailwind CSS**: Glassmorphic, modern cosmic theme with custom gradients and dark-mode styling.
- **Recharts**: Data visualization for Hamiltonian energy drift curves, multi-attribute comparisons, and readability metrics.
- **React Router**: Client-side routing across 14 dedicated views.
- **ModeContext**: Global state management ensuring persona selections persist across all views.
