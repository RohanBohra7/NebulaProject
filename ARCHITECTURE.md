# NEBULA Architecture Documentation

## 1. System Philosophy & Architectural Vision

**NEBULA: Intelligent Astronomical Data Visualization & Exploration Platform** is architected around a central tenet:  
**One Common Scientific Foundation, Three Dynamically Adaptive Experiences.**

Rather than segregating users into isolated silos or creating watered-down approximations, NEBULA establishes a single, uncompromised astronomical foundation:
1. Physical and orbital mechanics are evaluated with full mathematical rigor.
2. The empirical data layer acts as the single source of truth for physical parameters.
3. The presentation layer dynamically adapts its cognitive depth, mathematical formalism, visual scale, and AI scaffolding to match three user personas: **Researcher**, **Student**, and **Citizen**.

```
+-------------------------------------------------------------------------------------------------+
|                                    PRESENTATION LAYER (React 19)                                |
|                                                                                                 |
|   [ Researcher Workspace ]            [ Student Learning Hub ]            [ Citizen Space ]     |
|   - Formal LaTeX ($a, e, i, \mu$)     - Scaffolding & analogies           - Plain language      |
|   - Astrometric state vectors         - Kepler sandbox                    - Everyday comparisons|
|   - Symplectic energy drift           - Active quizzes                    - 3D Planetarium      |
+-------------------------------------------------------------------------------------------------+
                                                 ^
                                                 |  (ModeContext & Query Parameters)
+-------------------------------------------------------------------------------------------------+
|                                    GROUNDED AI SERVICE LAYER                                    |
|                                                                                                 |
|   - Abstractions: AIService, AIProvider, ContextBuilder, ToolRegistry, PromptManager           |
|   - Fallback Engine: High-fidelity deterministic knowledge engine for 100% offline usage        |
|   - Response Segregation: [NEBULA Data], [Computed Result], [Context], [General Explanation]    |
+-------------------------------------------------------------------------------------------------+
                                                 ^
                                                 |  (Context Injection & Tool Invocations)
+-------------------------------------------------------------------------------------------------+
|                                  SCIENTIFIC COMPUTATION & SIMULATION                            |
|                                                                                                 |
|   - Astropy Bridge: IAU 2015 / CODATA 2018 constants, unit-aware conversions                    |
|   - Orbital Mechanics: Vis-Viva, Hohmann transfers, Hill spheres, Roche limits, Resonances      |
|   - N-Body Dynamics: REBOUND IAS15/WHFast + NumPy Symplectic Leapfrog (Velocity-Verlet)        |
+-------------------------------------------------------------------------------------------------+
                                                 ^
                                                 |  (Normalized Astronomical Queries)
+-------------------------------------------------------------------------------------------------+
|                                     ASTRONOMICAL DATA LAYER                                     |
|                                                                                                 |
|   - Normalized Data Model: 23 celestial objects (Planets, Moons, Stars, Exoplanets, Deep Sky)   |
|   - Pluggable Providers: Local Verified Seed, NASA JPL Horizons, NASA Exoplanet Archive, SIMBAD|
|   - Quality Assurance: Volume-density, surface gravity, thermodynamics, and Astropy validation |
+-------------------------------------------------------------------------------------------------+
```

---

## 2. Frontend Architecture (`frontend/src/`)

The frontend is built using **React 19**, **TypeScript**, **Three.js / React Three Fiber**, and **Tailwind CSS**. It is organized into a modular component hierarchy:

```
frontend/src/
├── components/
│   ├── layout/          # AppShell, TopNav, Sidebar, Footer, Breadcrumbs
│   ├── visualization/   # SolarSystemCanvas, Object3DViewer, ObjectInspectorPanel
│   ├── simulation/      # NBodyCanvas, SimulationCharts, ScientificTransparencyPanel
│   └── ui/              # Button, Card, Modal, LoadingState, ErrorState, EmptyState, StatBadge
├── context/
│   ├── ModeContext.tsx  # Global persona state (researcher | student | citizen) & unit system
│   └── ToastContext.tsx # User feedback notifications
├── pages/
│   ├── LandingPage.tsx            # Platform hero, research motivation, statistics
│   ├── ModeSelectionPage.tsx      # Interactive persona comparison and selection
│   ├── CitizenDashboard.tsx       # Plain language, curiosities, everyday weight comparison
│   ├── StudentDashboard.tsx       # Kepler sandbox, astronomy concepts, quizzes, AI tutor
│   ├── ResearcherDashboard.tsx    # Hohmann delta-v, surface gravity, resonance, telemetry
│   ├── ExplorerPage.tsx           # Search, sort, filter, pagination, cards vs table
│   ├── ObjectDetailPage.tsx       # Tabbed physical/orbital telemetry, 3D model, Hohmann
│   ├── ComparisonPage.tsx         # Side-by-side parametric matrix (2-6 objects), radar chart
│   ├── VisualizationPage.tsx      # Interactive 3D Keplerian visualizer with live telemetry
│   ├── SimulationPage.tsx         # REBOUND N-body workbench, parameters, energy drift
│   ├── AIAssistantPage.tsx        # Multi-persona grounded chat with context integration
│   ├── ResearchEvaluationPage.tsx # Benchmark tasks, empirical validation, telemetry KPIs
│   ├── DataManagementPage.tsx     # Provenance badges, data sync, CSV/JSON export
│   └── SettingsPage.tsx           # Persona defaults, unit preferences, AI keys
├── services/
│   └── api.ts           # Type-safe client for all versioned backend endpoints
├── types/
│   └── astronomy.ts     # TypeScript interfaces mirroring backend schemas
└── App.tsx              # React Router v7 route definitions and provider tree
```

### Key Frontend Patterns:
- **Global `ModeContext`**: Propagates the active persona throughout the entire component tree. When a user switches modes, all cards, descriptions, formulas, and AI prompt directives immediately re-render.
- **Three.js WebGL Rendering**:
  - `SolarSystemCanvas`: Multi-body Keplerian orbit system with adjustable non-linear scale adaptations (relative scientific vs. visibility-enhanced modes), planetary textures, axial tilts, and speed multipliers (1x–500x).
  - `Object3DViewer`: High-resolution single-body showcase with atmospheric glows, axial rotation, and Saturnian ring meshes.
  - `NBodyCanvas`: Interactive 3D particle trajectory renderer with trails, velocity vectors, and camera orbit controls.

---

## 3. Backend Architecture (`backend/app/`)

The backend is built with **FastAPI**, **Pydantic v2**, and **SQLAlchemy 2.0**:

```
backend/app/
├── api/                 # REST routing layer
│   ├── v1/              # Versioned API router (/api/v1) & health endpoints
│   ├── objects.py       # Catalog query, search, filtering, and 3D orbit polyline
│   ├── comparison.py    # Multi-target comparison matrix and delta ratios
│   ├── calculations.py  # Scientific calculations (gravity, orbital, coordinate, units)
│   ├── simulation.py    # N-body simulation lifecycle (scenarios, run, stop, results)
│   ├── ai.py            # Grounded AI multi-persona chat, tools, explanations
│   ├── research.py      # Benchmark tasks, empirical validation, telemetry KPIs
│   └── data_management.py # Source status, data quality validation, CSV/JSON export
├── core/                # Configuration, logging, and custom exception handlers
│   ├── config.py        # Settings via pydantic-settings (.env management)
│   ├── exceptions.py    # Structured JSON error responses (NebulaException)
│   └── logging.py       # Formatted application logger
├── data/                # Data layer
│   ├── catalog.py       # SQLite catalog database queries
│   ├── seed_data.py     # 23 curated empirical celestial bodies
│   ├── sources.py       # External source manager
│   ├── validation.py    # Data quality validator and physical consistency engine
│   └── providers/       # Data provider abstraction (Local, NASA, SIMBAD, Composite)
├── scientific/          # Scientific Computation Engine
│   ├── constants.py     # CODATA 2018 & IAU 2015 fundamental physical constants
│   ├── gravity.py       # Universal gravitation, surface gravity, potential, tidal acceleration
│   ├── orbital.py       # Kepler solvers, Vis-Viva, Hohmann, Hill sphere, Roche limits, Resonances
│   ├── distances.py     # Euclidean distance, light travel time, angular diameter, distance modulus
│   ├── coordinates.py   # Cartesian, Spherical, Equatorial, and Ecliptic coordinate transformations
│   ├── units.py         # Astropy-powered dimensional analysis and unit conversions
│   └── ephemeris.py     # 3D Keplerian ellipse polyline generator and ephemeris propagator
├── simulation/          # N-Body Dynamics Engine
│   ├── nbody_engine.py  # REBOUND (IAS15, WHFast) + pure NumPy Symplectic Leapfrog
│   ├── scenarios.py     # 7 preconfigured scientific scenarios with physical initial conditions
│   ├── manager.py       # Simulation lifecycle state manager
│   └── conservation.py  # Hamiltonian energy, angular momentum, and relative drift calculations
├── ai/                  # Grounded AI Subsystem
│   ├── service.py       # AIService coordinator
│   ├── base.py          # AIProvider abstract base class
│   ├── providers.py     # GeminiProvider, OpenAIProvider, LocalDeterministicProvider
│   ├── tools.py         # ToolRegistry with 9 executable analytical functions
│   ├── context_builder.py # Entity detector and grounded telemetry builder
│   ├── prompt_manager.py # Multi-persona prompt formatting
│   └── response_validator.py # Scientific distinction and hallucination checker
├── evaluation/          # Research Evaluation Engine
│   ├── metrics.py       # FKGL, Coleman-Liau, and technical jargon density analyzer
│   ├── task_system.py   # Predefined benchmark task specifications and runner
│   ├── scientific_validation.py # 9-point benchmark validation against IAU/NASA truth
│   └── telemetry.py     # Non-sensitive interaction and performance event logger
└── db/                  # Relational database layer
    ├── database.py      # SQLAlchemy session factory and engine
    └── models.py        # ObjectRecord, SimulationRunRecord, EvaluationRecord, TelemetryRecord
```

---

## 4. Astronomical Data Layer

### 4.1 Normalized Data Model
All celestial bodies conform to the `NormalizedCelestialBody` schema (`backend/app/schemas/celestial.py`), supporting:
- Core identification: `id`, `name`, `category` (Planet, Moon, Star, Exoplanet, Asteroid, Comet, Deep-Sky).
- Physical properties: `mass_kg`, `mass_earth_relative`, `radius_km`, `radius_earth_relative`, `mean_density_g_cm3`, `surface_gravity_m_s2`, `escape_velocity_km_s`, `surface_temperature_k`.
- Orbital elements: `semi_major_axis_au`, `eccentricity`, `orbital_inclination_deg`, `orbital_period_days`, `mean_orbital_velocity_km_s`, `parent_body_id`.
- Provenance metadata: `data_source`, `source_url`, `confidence_level`, `provenance_badge`.
- Tri-mode descriptions: `description_citizen`, `description_student`, `description_researcher`.

### 4.2 Pluggable Data Providers
The data architecture implements the Provider pattern (`backend/app/data/providers/`):
- **`LocalDataProvider`**: Embedded offline catalog of 23 bodies verified against NASA JPL Horizons and Gaia DR3.
- **`NASAProvider`**: Caltech/IPAC TAP query adapter for the NASA Exoplanet Archive with automatic local fallback.
- **`SIMBADProvider`**: CDS Strasbourg astronomical query adapter for stellar parallax and photometry.
- **`CompositeDataProvider`**: Orchestrates provider priorities, handles network failures gracefully, and provides caching.

### 4.3 Data Quality & Physical Validation Engine
The validator (`backend/app/data/validation.py`) enforces:
1. Physical boundaries: Non-negative mass and radius; Third Law of Thermodynamics ($T > 0\text{ K}$); orbital eccentricity bound ($0 \le e < 1.0$).
2. Physical consistency scoring:
   $$\rho \approx \frac{3M}{4\pi R^3}, \quad g \approx \frac{GM}{R^2}, \quad v_{\text{esc}} \approx \sqrt{\frac{2GM}{R}}$$
3. Catalog-wide automated score: **96.0% physical consistency across all 23 catalog objects (0 errors).**

---

## 5. Scientific Computation Layer (`backend/app/scientific/`)

The scientific engine isolates pure astronomical computations from web routing:
- **Unit Discipline**: Uses SI units ($\text{kg}, \text{m}, \text{s}$) internally and provides pre-computed conversions using **Astropy Units** ($M_\odot, M_J, M_\oplus, R_\odot, R_J, R_\oplus, \text{AU}, \text{pc}, \text{ly}$, Gees, Celsius).
- **Newton-Raphson Kepler Solver**: Solves Kepler's transcendental equation:
  $$M = E - e \sin E$$
  to machine precision ($\epsilon < 10^{-12}$) and converts true anomaly $\nu$ to 3D Cartesian coordinates $(x, y, z, v_x, v_y, v_z)$.
- **Orbital Mechanics Tools**:
  - Vis-Viva equation: $v(r) = \sqrt{\mu (2/r - 1/a)}$.
  - Hohmann transfer: Calculates departure burn $\Delta v_1$, arrival burn $\Delta v_2$, total $\Delta v$, and transfer time $\tau$.
  - Hill sphere: $r_H \approx a(1-e) \sqrt[3]{m / 3M}$.
  - Roche limits: Rigid ($d = R(2\rho_M/\rho_m)^{1/3}$) and fluid ($d = 2.44 R(\rho_M/\rho_m)^{1/3}$) tidal disruption boundaries.
  - Mean-motion resonance scanner: Detects $p:q$ period commensurabilities up to 8th order.
  - Lagrange points: Calculates spatial equilibrium coordinates for L1, L2, L3, L4, and L5 in the CR3BP regime.

---

## 6. N-Body Simulation Engine (`backend/app/simulation/`)

### 6.1 Dual Integrators
1. **REBOUND IAS15** (15th-Order Gauss-Radau):
   - Adaptive step-size integrator designed for non-Hamiltonian and high-eccentricity orbital configurations.
   - Preserves relative energy errors within machine precision ($\Delta E / |E_0| \sim 10^{-14}$ to $10^{-16}$).
2. **NumPy Symplectic Leapfrog (Velocity-Verlet)**:
   - Volume-preserving 2nd-order symplectic integrator.
   - Exhibits strictly bounded oscillatory energy drift with zero secular dissipation.
   - Includes gravitational softening parameter $\epsilon = 10^{-6}$ to prevent numerical acceleration singularities.

### 6.2 Preconfigured Scenarios
- **Scenario 1 (`sun_earth`)**: Isolated two-body Keplerian baseline ($P = 1.000\text{ yr}$).
- **Scenario 2 (`earth_moon_sun`)**: Hierarchical 3-body system demonstrating lunar orbital precession under solar tidal perturbation.
- **Scenario 3 (`solar_system_inner`)**: 5-body coplanar inner solar system (Sun + Mercury, Venus, Earth, Mars).
- **Scenario 4 (`solar_system_full`)**: Complete 9-body major planet system showing outer gas giant perturbations.
- **Scenario 5 (`trappist_1_resonance`)**: 7-planet Laplace resonance chain ($24:15:9:6:4:3:2$).
- **Scenario 6 (`lagrange_trojans`)**: Equilateral L4 and L5 Trojan asteroid stability around Jupiter.
- **Scenario 7 (`figure_eight_choreography`)**: Chenciner-Montgomery zero-angular-momentum periodic 3-body solution.
- **Scenario 8 (`chaotic_three_body`)**: Pythagorean 3-4-5 right triangle demonstrating deterministic chaos and body ejection.

### 6.3 Validation & Safe Computational Limits
To prevent CPU denial-of-service:
- Max duration capped at $25.0\text{ years}$ (or 500 snapshot steps).
- Mandatory minimum of 2 bodies.
- Timestep validated against dynamical crossing times.

---

## 7. Grounded AI Subsystem (`backend/app/ai/`)

NEBULA rejects generic ungrounded chatbots. Its AI assistant is structured around factual grounding and scientific verification:

```
User Query + Active Context (Target / Sim / Compare)
                     │
                     ▼
             ContextBuilder
   (Entity extraction, Intent classification)
                     │
                     ▼
                ToolRegistry
   (Invokes catalog, analytical solvers, N-body state)
                     │
                     ▼
            PromptManager + Persona Directives
   (Formats grounded sections: [NEBULA Data], [Computed Result], [Context])
                     │
                     ▼
                 AIService
   (Dispatches to Gemini, OpenAI, Anthropic, or Local Deterministic Engine)
                     │
                     ▼
             ResponseValidator
   (Audits physical statements, enforces section segregation)
                     │
                     ▼
             Final Verified Response
```

### 7.1 Deterministic Offline Fallback
When external LLM credentials are absent, the `LocalDeterministicProvider` generates complete, factual, persona-calibrated responses by directly assembling catalog telemetry, Vis-Viva calculations, and pedagogical templates.

---

## 8. Multi-Persona Adaptive Continuum

| Architectural Dimension | 🔬 Researcher Mode | 🎓 Student Mode | 🌌 Citizen Mode |
| :--- | :--- | :--- | :--- |
| **Cognitive Grade Level** | **12.0 – 18.0** (Postgraduate) | **8.5 – 11.0** (Secondary/College) | **5.0 – 7.0** (Plain Language) |
| **Technical Jargon Density** | **10% – 22%** | **4% – 8%** | **< 3%** |
| **Reading Ease (FRE)** | **20 – 45** (Dense Academic) | **55 – 70** (Standard Educational) | **75 – 90** (Accessible Prose) |
| **Mathematical Detail** | Full LaTeX formulas, state vectors | Guided Kepler/Newton analogies | Everyday scales (flight time, weight) |
| **Orbital Visualizer** | True scale, live orbital state | Kepler laws interactive sandbox | Visual-enhanced scale, time warp |
| **N-Body Focus** | Energy drift ($\Delta E/E_0$), WHFast | Guided multi-body resonance tours | Scenic orbital trajectories |

---

## 9. Research Evaluation & Metrics Engine (`backend/app/evaluation/`)

NEBULA provides an empirical evaluation workbench (`/research`):
1. **6 Canonical Benchmark Tasks**:
   - `task_1`: Object Discovery (Find Europa in under 30s).
   - `task_2`: Parametric Comparison (Compare Earth vs Mars).
   - `task_3`: N-body Trajectory Simulation (Run Sun + Earth + Moon).
   - `task_4`: Grounded AI Query (Ask AI about TRAPPIST-1e habitability).
   - `task_5`: Readability Differentiation (Evaluate persona divergence).
   - `task_6`: Scientific Validation Suite (Run 9-point benchmark suite).
2. **Empirical Ground Truth Validation Suite**:
   Compares calculated physical properties against IAU/NASA ground truth with explicit physical tolerances ($\pm\epsilon$), documenting zero fabricated precision claims.
3. **Operational Telemetry System**:
   Persists non-sensitive system KPIs (task completion durations, discovery latencies, 3D interaction events, solver runtimes, page load latencies) with strict zero-PII guarantees.
