# NEBULA N-Body Gravitational Simulation Engine (Phase 6)

NEBULA provides an interactive, scientifically rigorous N-body gravitational dynamics engine designed to demonstrate orbital stability, mean-motion resonances, chaotic three-body interactions, and symplectic Hamiltonian energy conservation.

---

## 1. Architecture & Integrator Selection

The simulation engine is separated into `backend/app/simulation/` and decoupled from FastAPI presentation routes.

### 1.1 REBOUND C-Accelerated Engine (Rein & Liu)
NEBULA incorporates the high-performance **REBOUND** astronomical simulation package (v5.2.2):
- **IAS15 Integrator**: 15th-order adaptive Gauss-Radau integrator. Recommended for close encounters, hierarchical three-body systems (e.g., Sun-Earth-Moon), and chaotic interactions. Tracks trajectories with machine precision (relative energy drift $\Delta E / |E_0| \sim 10^{-15}$ to $10^{-16}$).
- **WHFast Integrator**: Symplectic Wisdom-Holman mapping designed for long-term integration of planetary systems orbiting a central dominant mass (e.g., Solar System, TRAPPIST-1). Preserves phase-space volume and Keplerian orbital invariants with bounded Hamiltonian error.
- **Leapfrog Integrator**: 2nd-order symplectic Velocity-Verlet integrator.

### 1.2 Pure NumPy Symplectic Leapfrog Fallback
To guarantee 100% offline operability even if external C extensions fail, NEBULA implements a vectorized Velocity-Verlet integrator in pure NumPy:

$$\mathbf{r}_{n+1} = \mathbf{r}_n + \mathbf{v}_n \Delta t + \frac{1}{2} \mathbf{a}_n \Delta t^2$$
$$\mathbf{a}_{n+1} = \mathbf{a}(\mathbf{r}_{n+1})$$
$$\mathbf{v}_{n+1} = \mathbf{v}_n + \frac{1}{2} (\mathbf{a}_n + \mathbf{a}_{n+1}) \Delta t$$

A gravitational softening parameter $\epsilon = 10^{-6}$ is applied to eliminate infinite acceleration singularities during close encounters.

---

## 2. Hamiltonian Conservation Laws & Stability Metrics

At every output sampling interval $t_k$, the engine computes:

### 2.1 Mechanical Energy
$$\text{Kinetic Energy: } T = \frac{1}{2} \sum_{i=1}^N m_i \|\mathbf{v}_i\|^2$$
$$\text{Gravitational Potential: } V = - \sum_{i=1}^N \sum_{j > i}^N \frac{G m_i m_j}{\|\mathbf{r}_i - \mathbf{r}_j\|}$$
$$\text{Total Energy: } E(t) = T(t) + V(t)$$

### 2.2 Relative Energy Drift
$$\text{Relative Error: } \frac{\Delta E}{|E_0|} = \frac{|E(t) - E(0)|}{|E(0)|}$$

Symplectic integrators exhibit bounded oscillatory drift around the true energy surface without artificial secular dissipation.

### 2.3 Angular Momentum Vector
$$\mathbf{L} = \sum_{i=1}^N m_i (\mathbf{r}_i \times \mathbf{v}_i)$$

---

## 3. Preconfigured Scientific Scenarios

All scenarios are defined with explicit physical initial conditions in astronomical units ($AU, M_\odot, \text{yr}, \text{AU/yr}$ with $G = 4\pi^2 \approx 39.4784176$), or normalized units ($G = 1.0$):

| Scenario ID | Name | Bodies Included | Integrator | Physical Focus |
| :--- | :--- | :--- | :--- | :--- |
| `sun_earth` | Sun - Earth | Sun, Earth | WHFast | 2-body circular Keplerian orbit ($r = 1.000\text{ AU}$, $P = 1.000\text{ yr}$). |
| `earth_moon_sun` | Sun - Earth - Moon | Sun, Earth, Moon | IAS15 | Hierarchical 3-body system showing lunar orbital precession under solar tidal forces. |
| `solar_system_inner` | Inner Solar System | Sun, Mercury, Venus, Earth, Mars | WHFast | Multi-planet terrestrial system with mutual gravitational perturbations. |
| `solar_system_full` | Full Solar System | Sun + 8 Major Planets | WHFast | 9-body simulation demonstrating gas giant perturbations and secular resonances. |
| `trappist_1_resonance` | TRAPPIST-1 Resonant Chain | Star + 7 Exoplanets | WHFast | 24:15:9:6:4:3:2 Laplace resonance chain in compact orbital architecture. |
| `lagrange_trojans` | Sun-Jupiter Trojans | Sun, Jupiter, L4 & L5 Asteroids | WHFast | Restricted 3-body stability of equilateral Lagrange points. |
| `figure_eight_choreography` | Figure-8 Choreography | 3 Equal-Mass Stars | IAS15 | Chenciner-Montgomery zero-angular-momentum periodic solution ($G=1$). |
| `chaotic_three_body` | Chaotic Three-Body | 3 Equal-Mass Stars | IAS15 | Pythagorean 3-4-5 triangle initial configuration showing gravitational ejection. |
| `binary_circumbinary` | Binary + Planet | Star A, Star B, Planet | IAS15 | Stable circumbinary planetary orbit outside stellar barycenter ($a > a_{\text{crit}}$). |

---

## 4. Parameter Controls & Safe Limits

To ensure robust local execution on typical hardware, the simulation engine enforces strict validation boundaries:

- **Duration ($T$)**: $0.001 \le T \le 100.0\text{ years}$.
- **Timestep ($\Delta t$)**: $10^{-6} \le \Delta t \le T$. Safe internal limit capped at $\le 500,000$ iterations.
- **Output Resolution ($N_{\text{steps}}$)**: $5 \le N_{\text{steps}} \le 1000$ snapshots.
- **Body Selection**: Minimum 2 gravitationally interacting bodies required.

---

## 5. REST API Specification

Mounted under `/api/v1/`:

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/simulations` | `POST` | Creates a simulation job (`auto_run=True` executes immediately). |
| `/api/v1/simulations` | `GET` | Lists all registered simulation runs in session history. |
| `/api/v1/simulations/{id}` | `GET` | Retrieves metadata, parameters, and status (`created`, `running`, `completed`, `stopped`). |
| `/api/v1/simulations/{id}/run` | `POST` | Executes or resumes simulation by ID. |
| `/api/v1/simulations/{id}/stop` | `POST` | Stops or cancels simulation execution. |
| `/api/v1/simulations/{id}/results` | `GET` | Returns full computed trajectories, velocities, distances, and energy curves. |
| `/api/v1/simulations/scenarios` | `GET` | Lists all preconfigured scenarios. |
| `/api/v1/simulations/scenarios/{id}` | `GET` | Returns scenario initial conditions, assumptions, and units. |
| `/api/v1/simulation/run` | `POST` | Direct synchronous execution endpoint (backward compatible). |

---

## 6. Scientific Transparency & Disclaimer

### 6.1 Reproducibility Metadata
Every simulation result payload includes a `reproducibility` dictionary recording:
- Scenario identifier and descriptive name
- Software versions: REBOUND version, NumPy version, Python interpreter version
- Complete initial state vectors $(m, x_0, y_0, z_0, vx_0, vy_0, vz_0)$
- Documented physical assumptions and unit definitions
- UTC timestamp of execution

### 6.2 Scientific Disclaimer
> **Never claim that the simulation perfectly reproduces reality:**  
> Classical N-body gravitational simulations are numerical approximations of point-mass Newtonian mechanics. Trajectories are subject to floating-point truncation, numerical integrator discretization drift, and physical chaos horizons (positive Lyapunov exponents). Minor perturbations exponentially diverge over orbital timescales. Real-world planetary ephemerides additionally involve general relativity, oblateness ($J_2$), and non-gravitational radiation forces.
