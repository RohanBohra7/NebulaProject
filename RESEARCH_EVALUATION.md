# NEBULA Research Evaluation & Reproducibility Methodology

This document outlines the evaluation methodology, reproducibility guidelines, experimental benchmarks, and empirical tolerances for **NEBULA: Intelligent Astronomical Data Visualization, Simulation, and Multi-Persona Exploration Platform**.

NEBULA investigates a platform architecture integrating:
$$\text{Astronomical Data} + \text{Scientific Computation} + \text{Interactive 3D Visualization} + \text{N-Body Simulation} + \text{Grounded AI} + \text{Adaptive Multi-Persona Interaction}$$

The system provides measurable application metrics and empirical physical validation **without fabricated findings or arbitrary precision claims**.

---

## 1. Datasets Used

NEBULA anchors all physical parameters, orbital elements, and visual models to authoritative, peer-reviewed astronomical datasets:

1. **NASA Planetary Fact Sheet (NSSDC / Goddard Space Flight Center)**
   - Primary source for solar system planets, the Moon, and dwarf planets.
   - Reference metrics: Mean radii, sidereal orbital periods, rotational periods, surface gravities ($1\text{ bar}$ boundary for gas giants), volumetric mean densities, and escape velocities.
   - URL: `https://nssdc.gsfc.nasa.gov/planetary/factsheet/`

2. **NASA JPL Horizons Ephemeris System (DE440 / DE441)**
   - Used for Keplerian osculating orbital elements (semi-major axis $a$, eccentricity $e$, inclination $i$, longitude of ascending node $\Omega$, argument of periapsis $\omega$, mean anomaly $M$).
   - Epoch: J2000.0 ($TDB = 2000\text{ Jan }1\text{d }12\text{h }00\text{m }00\text{s}$).

3. **Open Exoplanet Catalogue & NASA Exoplanet Archive**
   - Source for confirmed exoplanet systems (TRAPPIST-1 system, Proxima Centauri b).
   - Parameters: Host star spectral types, stellar luminosities, semi-major axes, transit orbital periods, planetary masses, and calculated equilibrium temperatures.

4. **Minor Planet Center (MPC) & Asteroid Fact Sheets**
   - Source for main-belt asteroids (Ceres, Vesta, Eros).
   - Parameters: Orbital parameters, rotational periods, and mean diameters.

5. **CODATA 2018 Recommended Values of the Fundamental Physical Constants**
   - Newtonian constant of gravitation: $G = 6.67430 \times 10^{-11}\text{ m}^3\text{ kg}^{-1}\text{ s}^{-2}$.
   - Standard Earth acceleration of gravity ($g_0$): $9.80665\text{ m/s}^2$ (WGS84 standard: $9.807\text{ m/s}^2$).
   - Standard Astronomical Unit ($1\text{ AU}$): $149,597,870,700\text{ m}$.
   - Speed of light in vacuum ($c$): $299,792,458\text{ m/s}$.

6. **IAU 2015 Resolution B3 (Nominal Solar and Planetary Conversion Constants)**
   - Nominal solar mass parameter: $(GM)_\odot = 1.3271244 \times 10^{20}\text{ m}^3\text{ s}^{-2}$, yielding $M_\odot \approx 1.98847 \times 10^{30}\text{ kg}$.
   - Nominal Earth mass parameter: $(GM)_\oplus = 3.986004 \times 10^{14}\text{ m}^3\text{ s}^{-2}$, yielding $M_\oplus \approx 5.9722 \times 10^{24}\text{ kg}$.

---

## 2. Software Versions & Computational Stack

| Layer | Component | Version | Role / Responsibility |
| :--- | :--- | :--- | :--- |
| **Backend Runtime** | Python | `3.14.0` | Core scientific execution environment |
| **Web Framework** | FastAPI | `0.115+` | High-throughput asynchronous RESTful API |
| **Data Validation** | Pydantic v2 | `2.13+` | Strict schema validation and serialization |
| **Database ORM** | SQLAlchemy | `2.0+` | Normalized relational models & telemetry persistence |
| **Storage Engine** | SQLite | `3.45+` | Zero-configuration local database (`nebula.db`) |
| **N-Body Engine** | REBOUND | `4.4+` | Symplectic and adaptive high-order gravitational integrators |
| **Astrophysics Library** | Astropy | `7.0+` | Unit-aware quantities and astronomical conversions |
| **Scientific Computing** | SciPy | `1.15+` | Numerical root-finding and differential equation solvers |
| **Linear Algebra** | NumPy | `2.2+` | Vectorized coordinate operations and fallback integrator |
| **Frontend Runtime** | Node.js | `22+` / `npm 10+` | Modern web frontend build toolchain |
| **UI Framework** | React | `19.0.0` | Declarative multi-mode component rendering |
| **Language** | TypeScript | `5.7+` | Type-safe astronomical interfaces |
| **Build Bundler** | Vite | `6.0+` | Instant Hot Module Replacement and production bundling |
| **3D Visualization** | Three.js / R3F | `0.170+` / `9.0+` | WebGL hardware-accelerated 3D planetary rendering |
| **Charts** | Recharts | `2.15+` | Responsive SVG/Canvas visualization of metrics |
| **Styling** | Tailwind CSS | `3.4+` | Space-themed dark/light mode responsive design |

---

## 3. Simulation Parameters & Physical Units

### 3.1 Astronomical Unit Scaling
Solar and planetary N-body simulations adopt Gaussian astronomical units:
- Length: Astronomical Unit ($1\text{ AU} = 1.495978707 \times 10^{11}\text{ m}$)
- Time: Julian Year ($1\text{ yr} = 365.25\text{ days} = 31,557,600\text{ s}$)
- Mass: Solar Mass ($1\ M_\odot = 1.98847 \times 10^{30}\text{ kg}$)
- Gravitational Constant:
  $$G = 4\pi^2\text{ AU}^3\text{ }M_\odot^{-1}\text{ yr}^{-2} \approx 39.47841760435743\text{ AU}^3\text{ }M_\odot^{-1}\text{ yr}^{-2}$$

### 3.2 Integrator Configurations
1. **REBOUND IAS15** (Primary):
   - 15th-order Gauss-Radau integrator with adaptive timestepping.
   - Internal accuracy parameter: $\epsilon = 1.0 \times 10^{-9}$.
   - Recommended for close encounters, hierarchical triples (Sun-Earth-Moon), and relativistic approximations.
   - Hamiltonian relative energy drift: $\max_t |(E(t) - E_0) / E_0| < 1.0 \times 10^{-14}$ (machine precision).

2. **REBOUND WHFast** (Planetary):
   - 2nd-order Symplectic Wisdom-Holman integrator.
   - Fixed timestep: $\Delta t = 0.001\text{ yr} \approx 8.766\text{ hours}$.
   - Guarantees bounded energy oscillations without secular drift over long time horizons.

3. **NumPy Symplectic Leapfrog (Velocity-Verlet)** (Deterministic Fallback):
   - Vectorized 2nd-order symplectic integrator.
   - Fixed timestep: $\Delta t = 0.5\text{ days} \approx 0.001369\text{ yr}$.
   - Energy error bound: $\max_t |(E(t) - E_0) / E_0| \le 1.0 \times 10^{-3}$ over $1.0\text{ yr}$ baseline.

---

## 4. Hardware Assumptions & Operational Constraints

1. **Host Hardware Specifications**:
   - Processor: Any modern dual-core or quad-core x86_64 or ARM64 CPU ($2.0\text{ GHz}+$ base clock).
   - Memory: Minimum $4\text{ GB}$ system RAM ($8\text{ GB}$ recommended for concurrently rendering Three.js particle systems, high-res canvas textures, and N-body history buffers).
   - Storage: $< 250\text{ MB}$ disk footprint including SQLite database, Python packages, and built frontend distribution.
   - Display: WebGL 2.0 compatible GPU (integrated Intel/AMD graphics or dedicated NVIDIA GPU).

2. **Network Independence**:
   - Zero external cloud services required.
   - Seed astronomical catalog operates fully offline from local SQLite database.
   - AI service includes a deterministic grounded fallback engine with comprehensive rule-based astrophysical synthesis when no remote LLM API key is present.

---

## 5. Predefined Evaluation Task Framework

NEBULA incorporates 6 structured canonical evaluation tasks that systematically verify platform capability across all core domains:

| Task ID | Canonical Task Name | Category | Route Target | Target Body | Success / Verification Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`task_1`** | Find Earth's Orbital Period | Data Exploration | `/object/earth` | Earth | Earth catalog entry retrieved; orbital period verified within $[365.0, 365.5]\text{ days}$ (reference: $365.256\text{ d}$). |
| **`task_2`** | Compare Earth and Mars | Comparative Analysis | `/compare` | Earth, Mars | Side-by-side payload generated; mass ratio $> 8.0:1$ ($5.97 \times 10^{24}\text{ kg}$ vs $6.42 \times 10^{23}\text{ kg}$), gravity ratio $> 2.0:1$ ($9.8\text{ m/s}^2$ vs $3.7\text{ m/s}^2$). |
| **`task_3`** | Locate Jupiter in 3D | Interactive Visualization | `/visualizer` | Jupiter | 3D solar system viewport targets Jupiter; semi-major axis resolved within $[5.0, 5.4]\text{ AU}$ ($5.2044\text{ AU}$ reference), texture preset verified. |
| **`task_4`** | Run an Earth-Sun Simulation | N-Body Simulation | `/simulation` | Sun, Earth | Numerical integration computes $\ge 50$ steps over $1.0\text{ yr}$; Hamiltonian energy drift $\Delta E / \|E_0\| < 1.0 \times 10^{-5}$. |
| **`task_5`** | Interpret Resulting Trajectory | Trajectory Analysis | `/simulation` | Sun, Earth | Trajectory distance bounds verified; Earth distance to Sun remains bounded in $[0.98, 1.02]\text{ AU}$ with zero unphysical escape. |
| **`task_6`** | Ask AI to Explain Orbital Period | Grounded AI Assistant | `/ai-assistant` | Earth | Query generates response referencing Kepler's Third Law ($T^2 \propto a^3$) grounded in catalog figures without hallucination. |

Both **interactive stopwatch recording** (user initiates task in UI, completes task, and logs actual elapsed time) and **server-side automated end-to-end execution** are supported via `/api/v1/research/tasks`.

---

## 6. Scientific Empirical Validation Benchmarks

Calculated physical and orbital properties are benchmarked against empirical references with **explicit physical tolerances ($\pm\epsilon$)**. Exact equality is neither claimed nor scientifically expected, as standard astronomical formulations employ spherical and point-mass approximations:

$$\text{Condition for Pass: } |\text{Computed} - \text{Reference}| \le \epsilon$$

| Benchmark Property | Category | Mathematical Formulation | Computed Value | Empirical Reference | Physical Units | Tolerance ($\pm\epsilon$) | Absolute Error | Status | Reference Source |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **Earth Sidereal Orbital Period** | Orbital Period | $T = 2\pi\sqrt{\frac{a^3}{G(M_\odot + M_\oplus)}}$ | `365.2563` | `365.2560` | $\text{days}$ | $\pm 0.05$ | `0.00035` | **PASSED** | NASA JPL Planetary Fact Sheet |
| **Mars Sidereal Orbital Period** | Orbital Period | $T = 2\pi\sqrt{\frac{a^3}{G(M_\odot + M_\text{Mars})}}$ | `686.9598` | `686.9800` | $\text{days}$ | $\pm 0.50$ | `0.02022` | **PASSED** | NASA JPL Mars Fact Sheet |
| **Earth Surface Gravity** | Surface Gravity | $g = \frac{GM_\oplus}{R_\oplus^2}$ | `9.7984` | `9.8070` | $\text{m/s}^2$ | $\pm 0.03$ | `0.00860` | **PASSED** | CODATA 2018 / WGS84 Standard |
| **Jupiter Surface Gravity** | Surface Gravity | $g = \frac{GM_\text{Jup}}{R_\text{eq}^2}$ | `24.7875` | `24.7900` | $\text{m/s}^2$ | $\pm 0.10$ | `0.00250` | **PASSED** | NASA Jupiter Fact Sheet ($1\text{ bar}$) |
| **Earth Escape Velocity** | Escape Velocity | $v_\text{esc} = \sqrt{\frac{2GM_\oplus}{R_\oplus}}$ | `11.1799` | `11.1860` | $\text{km/s}$ | $\pm 0.05$ | `0.00609` | **PASSED** | NASA Earth Fact Sheet |
| **Moon Escape Velocity** | Escape Velocity | $v_\text{esc} = \sqrt{\frac{2GM_\text{Moon}}{R_\text{Moon}}}$ | `2.3751` | `2.3800` | $\text{km/s}$ | $\pm 0.04$ | `0.00494` | **PASSED** | NASA Moon Fact Sheet |
| **Earth Mean Orbital Velocity** | Orbital Velocity | $v_\text{circ} = \sqrt{\frac{GM_\odot}{r}}$ | `29.7847` | `29.7800` | $\text{km/s}$ | $\pm 0.15$ | `0.00469` | **PASSED** | NASA JPL Horizons Mean Speed |
| **Earth-to-Mars Hohmann Transfer $\Delta v$** | Transfer Trajectory | $\Delta v_\text{tot} = \|v_{t1} - v_{c1}\| + \|v_{c2} - v_{t2}\|$ | `5.5960` | `5.5900` | $\text{km/s}$ | $\pm 0.10$ | `0.00600` | **PASSED** | Bate, Mueller, White Astrodynamics |
| **N-Body Energy Conservation Drift** | Simulation Stability | $\max_t \left\|\frac{E(t) - E_0}{E_0}\right\|$ | `4.57 \times 10^{-16}` | `0.0000` | dimensionless | $1.0 \times 10^{-5}$ | `4.57 \times 10^{-16}` | **PASSED** | Analytical Hamiltonian Invariant |

---

## 7. Application Telemetry Tracking & Privacy Architecture

### 7.1 Tracked Telemetry Dimensions
NEBULA tracks operational performance metrics across user interactions:
- **Task Execution**: Start time, completion time, duration ($\text{ms}$), outcome (success/failure), category.
- **Object Discovery**: Search term, discovery latency ($\text{ms}$), target celestial object ID.
- **Comparison Completion**: Objects selected, mode used, duration ($\text{ms}$).
- **3D Visualization Interactions**: Viewport interactions (orbit rotate, zoom, pan, body selection, visibility scale toggle).
- **Simulation Completion**: Scenario identifier, integrator selected, steps computed, solver duration ($\text{ms}$), max energy error drift.
- **AI Interactions**: Prompt category, response mode (researcher/student/citizen), latency ($\text{ms}$), tool invocations, grounding confirmation.
- **System Performance & Errors**: Route navigation load time ($\text{ms}$), API response time, uncaught client/server errors.

### 7.2 Strict Privacy Protection & Zero PII Guarantee
NEBULA implements a strict privacy-preserving data protocol:
- **No IP Addresses**: Client IP addresses are never parsed or stored.
- **No Personal Identifiers**: Usernames, email addresses, passwords, phone numbers, and persistent device identifiers are strictly filtered.
- **Sanitization Pipeline**: All incoming telemetry payloads pass through an automatic filter stripping authorization headers, tokens, and credentials.
- **Local SQLite Retention**: Telemetry is retained in the local database instance and never transmitted to external third-party tracking services (Google Analytics, Mixpanel, etc.).

---

## 8. Multi-Persona Cognitive Divergence Methodology

NEBULA measures how adaptive presentation varies cognitive load while preserving identical empirical truth across three personas:

1. **Flesch Reading Ease (FRE)**:
   $$\text{FRE} = 206.835 - 1.015 \left(\frac{\text{Words}}{\text{Sentences}}\right) - 84.6 \left(\frac{\text{Syllables}}{\text{Words}}\right)$$
   - *Target: Citizen $75-90$ (Plain language) vs Researcher $20-45$ (Dense academic).*

2. **Flesch-Kincaid Grade Level (FKGL)**:
   $$\text{FKGL} = 0.39 \left(\frac{\text{Words}}{\text{Sentences}}\right) + 11.8 \left(\frac{\text{Syllables}}{\text{Words}}\right) - 15.59$$
   - *Target: Citizen $5-7$ (Elementary/Public) vs Student $8-11$ (High School) vs Researcher $14-18$ (Postgraduate).*

3. **Technical Terminology Density ($D_\text{tech}$)**:
   Percentage of words matching the astrophysically curated lexicon $V_\text{astro}$ ($70+$ terms including *barycenter, perihelion, aphelion, keplerian, roche, hydrostatic equilibrium, spectroscopy*).

4. **Mathematical Expression Count ($N_\text{math}$)**:
   Count of LaTeX formulas ($\$...\$$ or $\$ \$...\$ \$$) presenting formal physical relationships.

5. **Empirical Grounding Score**:
   Percentage of retrieved catalog attributes accurately represented in the generated text.

---

## 9. Limitations & Assumptions

1. **Point-Mass Gravitation**:
   - The N-body integrator treats bodies as spherically symmetric point masses.
   - Non-spherical gravitational potentials (e.g., Earth's $J_2 = 1.08263 \times 10^{-3}$ oblateness quadrupole moment, Moon mascons) are omitted in the standard solar system model.

2. **Newtonian Mechanics**:
   - Computations utilize Newtonian mechanics and Keplerian two-body approximations.
   - General relativistic corrections (e.g., Mercury's perihelion advance of $42.98''/\text{century}$, gravitational redshift, light deflection) are treated analytically in researcher notes rather than directly integrated into the coordinate equations of motion.

3. **Coplanar Circular Hohmann Transfers**:
   - Hohmann trajectory derivations assume initial and target orbits are coplanar and circular. Planetary orbital inclinations (e.g., Mars inclination $i = 1.85^\circ$) and eccentricities ($e = 0.0934$) necessitate hyperbolic mid-course trajectory corrections in actual spaceflight.

4. **Local AI Deterministic Fallback**:
   - When no external LLM API credentials are configured, the assistant utilizes a deterministic, grounded template engine. This ensures $100\%$ uptime and reproducible evaluations without external network dependencies.
