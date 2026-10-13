# NEBULA N-Body Gravitational Dynamics Engine

**NEBULA: Intelligent Astronomical Data Visualization & Exploration Platform** includes an interactive, scientifically rigorous N-body gravitational simulation engine designed to demonstrate multi-body orbital stability, mean-motion resonances, chaotic interactions, and Hamiltonian conservation.

---

## 1. Dual-Engine Architecture

The simulation engine is located in `backend/app/simulation/` and implements two complementary numerical integrators:

### 1.1 REBOUND C-Accelerated Engine (`rebound`)
NEBULA integrates the industry-standard **REBOUND** multi-purpose N-body code developed by Hanno Rein & Shang-Fei Liu:
- **REBOUND IAS15**: 15th-order adaptive Gauss-Radau integrator. Extremely high accuracy for chaotic systems, highly eccentric trajectories, and close gravitational encounters. Relative Hamiltonian energy error is typically preserved to machine precision ($\Delta E / |E_0| \sim 10^{-14}$ to $10^{-16}$).
- **REBOUND WHFast**: 2nd-order Symplectic Wisdom-Holman mapping designed for fast long-term integration of planetary systems. It separates the Hamiltonian into exact Keplerian motion and mutual interaction perturbations:
  $$H = H_{\text{Kepler}} + H_{\text{Interaction}}$$
  Preserves phase-space volume and exhibits zero secular energy drift over astronomical timescales.

### 1.2 NumPy Symplectic Leapfrog (Velocity-Verlet)
To ensure 100% offline portability on systems without C-compiler extensions, NEBULA implements a vectorized, pure Python/NumPy Symplectic Leapfrog integrator in `backend/app/simulation/nbody_engine.py`:

$$\mathbf{r}_{n+1} = \mathbf{r}_n + \mathbf{v}_n \Delta t + \frac{1}{2} \mathbf{a}_n \Delta t^2$$
$$\mathbf{a}_{n+1} = \mathbf{a}(\mathbf{r}_{n+1})$$
$$\mathbf{v}_{n+1} = \mathbf{v}_n + \frac{1}{2} (\mathbf{a}_n + \mathbf{a}_{n+1}) \Delta t$$

- **Gravitational Softening**: A Plummer softening parameter $\epsilon = 1.0 \times 10^{-6}\text{ AU}$ is applied to eliminate infinite acceleration singularities during close encounters:
  $$\mathbf{a}_i = - \sum_{j \neq i} \frac{G m_j (\mathbf{r}_i - \mathbf{r}_j)}{\left(\|\mathbf{r}_i - \mathbf{r}_j\|^2 + \epsilon^2\right)^{3/2}}$$

---

## 2. Hamiltonian Energy & Angular Momentum Conservation

The simulation tracks the total mechanical energy $E(t) = T(t) + V(t)$ and total angular momentum vector $\mathbf{L}(t)$ at every output step:

$$T(t) = \frac{1}{2} \sum_{i=1}^N m_i \|\mathbf{v}_i\|^2$$
$$V(t) = - \sum_{i=1}^N \sum_{j > i}^N \frac{G m_i m_j}{\|\mathbf{r}_i - \mathbf{r}_j\|}$$
$$\mathbf{L}(t) = \sum_{i=1}^N m_i (\mathbf{r}_i \times \mathbf{v}_i)$$

### Relative Energy Drift Metric:
$$\text{Relative Energy Drift}(t) = \frac{|E(t) - E(0)|}{|E(0)|}$$

- **Symplectic Guarantee**: Symplectic integrators (WHFast and Leapfrog) exhibit strictly bounded oscillatory energy error around the true energy surface without artificial energy dissipation or unbounded secular drift.
- **Drift Display**: Real-time energy drift curves are plotted dynamically in the UI via Recharts (`SimulationCharts.tsx`).

---

## 3. Preconfigured Scientific Scenarios

All scenarios are defined in `backend/app/simulation/scenarios.py` with scientifically grounded initial conditions:

| Scenario ID | Name | Bodies Simulated | Default Duration | Recommended Integrator | Scientific Focus |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `sun_earth` | **Sun - Earth** | Sun, Earth | $1.0\text{ yr}$ | `whfast` / `ias15` | Fundamental two-body Keplerian circular orbit ($P = 1.000\text{ yr}$). |
| `earth_moon_sun` | **Sun - Earth - Moon** | Sun, Earth, Moon | $0.25\text{ yr}$ | `ias15` | Hierarchical 3-body perturbation showing lunar orbital precession under solar tides. |
| `solar_system_inner` | **Inner Solar System** | Sun, Mercury, Venus, Earth, Mars | $2.0\text{ yr}$ | `whfast` | Coplanar terrestrial planetary orbits with mutual gravitational perturbations. |
| `solar_system_full` | **Full Solar System** | Sun + 8 Major Planets | $12.0\text{ yr}$ | `whfast` | Complete 9-body system capturing gas giant secular resonances. |
| `trappist_1_resonance` | **TRAPPIST-1 Chain** | M-Dwarf Star + 7 Planets | $0.15\text{ yr}$ | `whfast` | Ultra-compact Laplace resonance chain ($24:15:9:6:4:3:2$). |
| `lagrange_trojans` | **Sun - Jupiter Trojans**| Sun, Jupiter, L4 & L5 Asteroids | $12.0\text{ yr}$ | `whfast` | Equilateral restricted 3-body Lagrange point stability in CR3BP regime. |
| `figure_eight_choreography`| **Figure-8 Choreography**| 3 Equal-Mass Stars | $2.0\text{ normalized}$| `ias15` | Chenciner-Montgomery zero-angular-momentum periodic 3-body solution. |
| `chaotic_three_body` | **Chaotic 3-Body** | 3 Stars (Masses 3, 4, 5) | $1.5\text{ normalized}$| `ias15` | Pythagorean problem demonstrating extreme sensitive dependence and ejection. |

---

## 4. Parameter Validation & Computational Safety

To prevent accidental denial-of-service or browser freezing during large computations, `validate_simulation_parameters()` enforces:
1. **Minimum Body Count**: At least 2 bodies must be selected ($\ge 2$).
2. **Maximum Time Duration**: Capped at $25.0\text{ years}$ (or $25.0\text{ normalized units}$).
3. **Maximum Snapshot Steps**: Capped at $500\text{ steps}$.
4. **Adaptive IAS15 Step Size**: IAS15 automatically decreases step size near perihelion and increases it in deep space.

---

## 5. REST Simulation API Lifecycle

The simulation subsystem exposes complete lifecycle endpoints:
- `GET /api/v1/simulations/scenarios`: Lists all scenarios.
- `GET /api/v1/simulations/scenarios/{id}`: Returns initial state vectors and assumptions.
- `POST /api/v1/simulations`: Creates and optionally executes integration.
- `GET /api/v1/simulations/{id}/results`: Returns trajectory coordinates and energy drift.
- `POST /api/v1/simulation/run`: Direct one-shot simulation runner.
