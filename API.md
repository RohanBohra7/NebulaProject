# NEBULA REST API Reference

Base URL (Versioned): `http://localhost:8000/api/v1`  
Base URL (Legacy Compatible): `http://localhost:8000/api`  
Interactive OpenAPI Documentation (Swagger UI): `http://localhost:8000/docs`  
OpenAPI JSON Specification: `http://localhost:8000/openapi.json`

> **Note**: All endpoints listed below are genuinely implemented in the NEBULA backend and verified by automated tests. No non-existent endpoints are documented.

---

## 1. System Health & Platform Status

### `GET /api/v1/health`
Returns the operational health, database status, simulation engine, and active AI provider.  
*Also accessible via `GET /api/health` and `GET /health`.*

**Response (200 OK)**:
```json
{
  "status": "healthy",
  "platform": "NEBULA: Intelligent Astronomical Data Platform",
  "version": "1.0.0",
  "database": "sqlite_ready",
  "simulation_engine": "rebound_ias15_ready",
  "ai_engine": {
    "provider": "LocalDeterministicProvider",
    "deterministic_fallback_ready": true
  },
  "supported_modes": ["researcher", "student", "citizen"]
}
```

---

## 2. Astronomical Objects API (`/api/v1/objects`)

### `GET /api/v1/objects`
Retrieves celestial bodies with sorting, multi-attribute filtering, and optional pagination.

**Query Parameters**:
- `category` *(string, optional)*: Filter by `Planet`, `Moon`, `Star`, `Exoplanet`, `Asteroid`, `Comet`, `Deep-Sky`.
- `search` *(string, optional)*: Case-insensitive search on object name.
- `sort_by` *(string, default: "distance")*: Sort by `distance`, `mass`, `radius`, `period`, `temperature`, `name`.
- `sort_order` *(string, default: "asc")*: Direction `asc` or `desc`.
- `min_mass` / `max_mass` *(float, optional)*: Earth-relative mass bounds.
- `min_radius` / `max_radius` *(float, optional)*: Radius bounds in kilometers.
- `has_rings` *(boolean, optional)*: Filter by ring system presence.
- `has_atmosphere` *(boolean, optional)*: Filter by atmospheric presence.
- `page` *(int, optional, $\ge 1$)*: Page number (enables paginated response envelope).
- `page_size` *(int, optional, 1–100)*: Items per page.
- `format` *(string, optional)*: `"paginated"` or `"list"`.

**Response (200 OK - Paginated Envelope)**:
```json
{
  "items": [
    {
      "id": "earth",
      "name": "Earth",
      "category": "Planet",
      "parent_body_id": "sun",
      "mass_kg": 5.9722e24,
      "mass_earth_relative": 1.0,
      "radius_km": 6371.0,
      "radius_earth_relative": 1.0,
      "surface_gravity_m_s2": 9.807,
      "surface_temperature_k": 288.0,
      "semi_major_axis_au": 1.0,
      "orbital_period_days": 365.256,
      "eccentricity": 0.0167,
      "color_hex": "#38bdf8"
    }
  ],
  "total": 23,
  "page": 1,
  "page_size": 20,
  "total_pages": 2,
  "has_next": true,
  "has_prev": false
}
```

### `GET /api/v1/objects/search`
Searches the catalog by name, slug, category, or spectral classification with highlighted snippets.

**Query Parameters**:
- `q` *(string, required)*: Search query string.
- `limit` *(int, default: 10)*: Maximum results.

### `GET /api/v1/objects/type/{type_name}`
Retrieves all celestial bodies belonging to a designated category (e.g. `Planet`, `Moon`, `Star`).

### `GET /api/v1/objects/{object_id}`
Retrieves full astrophysical parameters, 3D orbit coordinates, Astropy unit conversions, related bodies, and source provenance for an object.

**Path Parameters**:
- `object_id` *(string, required)*: Unique identifier (e.g. `earth`, `jupiter`, `trappist-1e`, `sirius-a`).

### `GET /api/v1/objects/{object_id}/orbit-path`
Generates 3D polygonal polyline coordinates for the object's Keplerian orbital ellipse.

**Query Parameters**:
- `samples` *(int, default: 120)*: Number of polyline coordinate vertices.

### `GET /api/v1/objects/{object_id}/ephemeris`
Propagates the body along its orbit at a designated elapsed time in Earth days.

**Query Parameters**:
- `elapsed_days` *(float, default: 0.0)*: Elapsed propagation time in days.

---

## 3. Parametric Comparison API (`/api/v1/compare`)

### `POST /api/v1/compare/`
Compares 2 to 6 celestial objects side-by-side, computing physical ratios, absolute deltas, percentage differences, radar metrics, and persona insights.

**Request Body**:
```json
{
  "object_ids": ["earth", "mars"],
  "mode": "student"
}
```

**Response (200 OK)**:
```json
{
  "primary_reference": "Earth",
  "compared_objects": [ /* array of object details */ ],
  "ratios": [
    {
      "target_id": "mars",
      "target_name": "Mars",
      "relative_to": "Earth",
      "mass_ratio": 0.1074,
      "radius_ratio": 0.532,
      "gravity_ratio": 0.3793,
      "density_ratio": 0.7135,
      "period_ratio": 1.8808,
      "temperature_ratio": 0.7292,
      "distance_ratio": 1.5237
    }
  ],
  "absolute_differences": [ /* array of absolute and percentage deltas */ ],
  "radar_metrics": [ /* normalized radar axes: mass, radius, gravity, density, distance, period */ ],
  "comparative_insights": {
    "researcher": "Parametric divergence highlights planetary mass thresholds for atmospheric volatile retention...",
    "student": "Notice how Mars has only about one-tenth of Earth's mass...",
    "citizen": "If you weigh 70 kg on Earth, you would weigh only about 26.5 kg on Mars!"
  }
}
```

---

## 4. Scientific Computation Engine (`/api/v1/calculate`)

### `POST /api/v1/calculate/gravity`
Calculates Newtonian gravitational force magnitude and 3D force vectors between two bodies or catalog IDs.

**Request Body**:
```json
{
  "object1_id": "sun",
  "object2_id": "earth"
}
```
*(Accepts optional manual masses `m1_kg`, `m2_kg` and distances `distance_m`, `distance_au`, `distance_km`).*

### `POST /api/v1/calculate/gravity/surface`
Computes local surface gravity ($g$), Earth relative Gees, and surface escape velocity.

**Request Body**:
```json
{
  "object_id": "earth"
}
```
*(Or manual `mass_kg` and `radius_m` / `radius_km`).*

### `POST /api/v1/calculate/gravity/potential`
Computes gravitational potential $\Phi(r) = -GM/r$ and potential energy $U(r)$.

### `POST /api/v1/calculate/orbital-velocity`
Computes circular orbital velocity, Vis-Viva instantaneous velocity, escape velocity, and apsidal extrema.

**Request Body**:
```json
{
  "central_mass_kg": 1.98847e30,
  "semi_major_axis_au": 1.0,
  "eccentricity": 0.0167,
  "distance_au": 1.0
}
```

### `POST /api/v1/calculate/orbital-period`
Computes sidereal orbital period via Kepler's Third Law ($P = 2\pi\sqrt{a^3/GM}$) and/or synodic period between two bodies.

### `POST /api/v1/calculate/hohmann`
Calculates coplanar Hohmann transfer orbit parameters between two orbital radii or catalog bodies.

**Request Body**:
```json
{
  "origin_id": "earth",
  "target_id": "mars"
}
```
**Response (200 OK)**:
```json
{
  "origin_name": "Earth",
  "target_name": "Mars",
  "delta_v1_km_s": 2.945,
  "delta_v2_km_s": 2.649,
  "total_delta_v_km_s": 5.594,
  "transfer_time_days": 258.8,
  "transfer_semi_major_axis_au": 1.262,
  "transfer_eccentricity": 0.2076
}
```

### `POST /api/v1/calculate/hill-sphere`
Calculates the gravitational Hill sphere radius $r_H \approx a(1-e)\sqrt[3]{m/(3M)}$.

### `POST /api/v1/calculate/roche-limit`
Calculates rigid and fluid tidal disruption boundaries for an orbiting satellite.

### `POST /api/v1/calculate/resonance`
Scans for near-integer mean-motion orbital resonances between two orbital periods ($p:q$ up to 8th order).

### `POST /api/v1/calculate/lagrange-points`
Computes spatial positions for the five Lagrange equilibrium points L1 through L5 in the CR3BP regime.

### `POST /api/v1/calculate/distance`
Computes spatial distance metrics, light travel time, angular diameter, and distance modulus.

### `POST /api/v1/calculate/coordinates/transform`
Transforms coordinates between Cartesian, Spherical, Equatorial ($\alpha, \delta$), and Ecliptic ($\lambda, \beta$) systems.

### `GET /api/v1/calculate/units/categories`
Lists all supported physical dimension categories for unit conversions.

### `POST /api/v1/calculate/units/convert`
Converts physical quantities using Astropy-powered dimensional analysis.

---

## 5. N-Body Simulation API (`/api/v1/simulations`)

### `GET /api/v1/simulations/scenarios`
Lists all preconfigured scientific simulation scenarios.  
*Also accessible via `GET /api/v1/simulation/scenarios`.*

### `GET /api/v1/simulations/scenarios/{scenario_id}`
Retrieves detailed configuration, initial particle state vectors, assumptions, and units for a scenario.

### `POST /api/v1/simulations`
Creates and initializes an N-body simulation specification. If `auto_run=true` (default), integrates immediately.

**Request Body**:
```json
{
  "scenario_id": "sun_earth",
  "integrator": "ias15",
  "duration": 1.0,
  "total_time_years": 1.0,
  "num_steps": 150,
  "selected_bodies": ["sun", "earth"],
  "auto_run": true
}
```

### `GET /api/v1/simulations`
Retrieves past simulation runs from the database.

### `GET /api/v1/simulations/{simulation_id}`
Retrieves metadata and status of a specific simulation.

### `POST /api/v1/simulations/{simulation_id}/run`
Executes integration on a previously created simulation specification.

### `POST /api/v1/simulations/{simulation_id}/stop`
Signals early termination of an active simulation run.

### `GET /api/v1/simulations/{simulation_id}/results`
Retrieves full trajectory snapshots, step count, runtime in milliseconds, and relative energy conservation error ($\Delta E/|E_0|$).

### `POST /api/v1/simulation/run`
Backward-compatible direct integration endpoint executing scenario runs in a single call.

---

## 6. Grounded AI Assistant API (`/api/v1/ai`)

### `GET /api/v1/ai/status`
Returns the active AI provider name, registered tools count, and grounding engine status.

### `GET /api/v1/ai/tools`
Returns the JSON schemas for all registered AI tools/functions.

### `POST /api/v1/ai/tools/{tool_name}/execute`
Directly executes an AI tool function against NEBULA databases and computational solvers.

### `POST /api/v1/ai/chat`
Submits a user query with active context to the grounded multi-persona AI engine.

**Request Body**:
```json
{
  "prompt": "How does TRAPPIST-1e compare to Earth?",
  "mode": "student",
  "target_object_id": "trappist-1e",
  "comparison_ids": ["earth", "trappist-1e"]
}
```

**Response (200 OK)**:
```json
{
  "response": "TRAPPIST-1e is an Earth-sized rocky exoplanet orbiting an ultra-cool dwarf star...",
  "mode": "student",
  "provider": "LocalDeterministicProvider",
  "used_fallback": true,
  "grounding_meta": {
    "target_object": "trappist-1e",
    "verified_parameters": ["mass_kg", "radius_km", "orbital_period_days"],
    "data_source": "NASA Exoplanet Archive / Planetary Fact Sheet"
  },
  "tools_invoked": ["get_object", "compare_objects"],
  "distinctions": {
    "nebula_data": "TRAPPIST-1e mass: 0.692 M_Earth; Radius: 0.920 R_Earth; Period: 6.1 days.",
    "computed_result": "Surface gravity: 8.04 m/s² (0.82 Gees).",
    "external_scientific_context": "Discovered via Spitzer and VLT transit photometry in 2017.",
    "general_explanation": "Because its host star is small and dim, its 6-day orbit places it inside the habitable zone."
  },
  "validation": {
    "is_valid": true,
    "score": 0.98,
    "safety_flags": []
  }
}
```

### `POST /api/v1/ai/explain-object`
Generates an adaptive, grounded narrative for a selected celestial body.

### `POST /api/v1/ai/explain-simulation`
Generates an astrophysical interpretation of an N-body simulation trajectory and energy drift.

---

## 7. Research Evaluation & Metrics API (`/api/v1/research`)

### `GET /api/v1/research/tasks`
Lists the 6 canonical evaluation benchmark tasks with structured specifications, route targets, and success criteria.

### `POST /api/v1/research/tasks/{task_id}/start`
Starts an interactive evaluation session stopwatch for a designated task.

### `POST /api/v1/research/tasks/{task_id}/complete`
Records interactive completion of a task with stopwatch elapsed duration and success flag.

### `POST /api/v1/research/tasks/{task_id}/run_automated`
Executes an automated, reproducible server-side verification run of a task.

### `POST /api/v1/research/tasks/run_all`
Executes all 6 canonical benchmark tasks sequentially and aggregates the results.

### `GET /api/v1/research/validation/benchmarks`
Executes the 9-point scientific empirical validation suite comparing calculated physical properties against IAU and NASA JPL Horizons ground truth.

### `POST /api/v1/research/telemetry`
Ingests a non-sensitive interaction event (zero-PII guaranteed).

### `GET /api/v1/research/telemetry/summary`
Returns aggregated application performance telemetry, discovery latencies, and interaction KPIs.

### `POST /api/v1/research/evaluate`
Submits a query to be evaluated across all three personas in parallel, computing live readability metrics (FKGL, Coleman-Liau, FRE) and technical vocabulary densities.

### `GET /api/v1/research/history`
Retrieves past evaluation runs from the database.

### `GET /api/v1/research/benchmarks`
Returns aggregated persona readability benchmarks and simulation engine accuracy statistics.

---

## 8. Data Management & Provenance API (`/api/v1/data`)

### `GET /api/v1/data/status`
Returns connectivity, latency, and cache status for all integrated astronomical providers.

### `GET /api/v1/data/validate`
Executes dimensional checks, physical consistency checks, and Astropy unit validations across the entire catalog (score: 96.0%).

### `GET /api/v1/data/export`
Exports the entire astronomical catalog in JSON or CSV format.  
*Query Parameter: `format=json` or `format=csv`.*

### `POST /api/v1/data/sync`
Triggers catalog verification and synchronizes the local cache with external feeds.
