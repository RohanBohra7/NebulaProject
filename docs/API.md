# NEBULA REST API Reference

Base URL: `http://localhost:8000/api`  
Interactive OpenAPI Documentation: `http://localhost:8000/docs`

---

## 1. Astronomical Objects API

### `GET /api/objects/`
Retrieves all celestial bodies with optional filtering.
- **Query Parameters**:
  - `category` (string, optional): Filter by `Planet`, `Star`, `Exoplanet`, `Moon`, `Deep-Sky`, `Asteroid`, `Comet`.
  - `search` (string, optional): Case-insensitive search on object name or identifier.
- **Response**: Array of `AstronomicalObject` objects.

### `GET /api/objects/{object_id}`
Retrieves full astrophysical and orbital metadata for a specific celestial body.
- **Path Parameters**:
  - `object_id` (string, required): e.g. `earth`, `jupiter`, `trappist-1e`, `betelgeuse`.
- **Response**: Full object dictionary including computed `orbit_path_3d` coordinates.

### `GET /api/objects/{object_id}/orbit-path`
Generates 3D polygonal vertices for the object's Keplerian orbital ellipse.
- **Query Parameters**:
  - `samples` (int, default: 120): Number of polyline samples.

### `GET /api/objects/{object_id}/ephemeris`
Propagates the body along its orbit at a designated elapsed time.
- **Query Parameters**:
  - `elapsed_days` (float, required): Elapsed time in Earth days.

---

## 2. Scientific Calculations API

### `POST /api/calculate/hohmann`
Calculates coplanar Hohmann transfer orbit parameters between two bodies or orbital radii.
- **Request Body**:
  ```json
  {
    "origin_id": "earth",
    "target_id": "mars",
    "r1_au": 1.0,
    "r2_au": 1.524
  }
  ```
- **Response**:
  ```json
  {
    "origin_name": "Earth",
    "target_name": "Mars",
    "delta_v1_km_s": 2.945,
    "delta_v2_km_s": 2.651,
    "total_delta_v_km_s": 5.596,
    "transfer_time_days": 258.9,
    "transfer_semi_major_axis_au": 1.262,
    "transfer_eccentricity": 0.2076
  }
  ```

### `POST /api/calculate/hill-sphere`
Calculates the gravitational Hill sphere radius.
- **Request Body**: `{"object_id": "earth"}` or `{"semi_major_axis_au": 1.0, "body_mass_kg": 5.9722e24}`

### `POST /api/calculate/roche-limit`
Calculates rigid and fluid tidal disruption boundaries.
- **Request Body**: `{"primary_radius_km": 69911, "primary_density_g_cm3": 1.33, "secondary_density_g_cm3": 3.0}`

### `POST /api/calculate/resonance`
Detects near-integer mean-motion orbital resonances.
- **Request Body**: `{"period_days_1": 60189.0, "period_days_2": 90560.0, "max_order": 8}`

### `POST /api/calculate/lagrange-points`
Computes spatial coordinates for the five Lagrange equilibrium points L1-L5.
- **Request Body**: `{"primary_mass_kg": 1.989e30, "secondary_mass_kg": 5.972e24, "separation_au": 1.0}`

---

## 3. N-Body Simulation API

### `GET /api/simulation/scenarios`
Lists all preconfigured scientific simulation scenarios.

### `POST /api/simulation/run`
Executes N-body gravitational integration and records conservation metrics.
- **Request Body**:
  ```json
  {
    "scenario_id": "solar_system_inner",
    "integrator": "ias15",
    "total_time_years": 2.0,
    "num_steps": 150
  }
  ```
- **Response**:
  - `engine_used`: Integrator identifier.
  - `runtime_ms`: Milliseconds taken to compute.
  - `max_energy_error`: Maximum relative Hamiltonian energy drift $\Delta E / |E_0|$.
  - `bodies`: Array of particles with 3D trajectories `[[x, y, z], ...]`.
  - `energy_drift_series`: Step-by-step energy and error tracking.

---

## 4. Grounded AI API

### `POST /api/ai/chat`
Submits a query to the persona-adapted, grounded AI service.
- **Request Body**:
  ```json
  {
    "prompt": "Explain the atmosphere of Titan.",
    "mode": "student",
    "target_object_id": "titan"
  }
  ```
- **Response**:
  ```json
  {
    "response": "...",
    "mode": "student",
    "provider": "NEBULA Grounded Scientific Knowledge Engine",
    "used_fallback": false,
    "grounding_meta": {
      "grounded_objects": ["Titan"],
      "grounded_points_count": 5,
      "is_grounded": true
    }
  }
  ```

---

## 5. Research & Evaluation API

### `POST /api/research/evaluate`
Runs a prompt across Researcher, Student, and Citizen personas in parallel and computes quantitative complexity metrics.
- **Request Body**: `{"query": "How does TRAPPIST-1e compare to Earth?"}`
- **Response**: Side-by-side dictionary containing readability scores, technical vocabulary density, and LaTeX math count.

### `GET /api/research/benchmarks`
Retrieves aggregate research benchmarks across all personas and simulation runs.

---

## 6. Data Management API

### `GET /api/data/status`
Checks connectivity and caching status for all integrated data sources.

### `GET /api/data/export?format=json|csv`
Exports the complete astronomical catalog in JSON or CSV format.
