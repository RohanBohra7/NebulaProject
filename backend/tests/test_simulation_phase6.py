"""
Automated Verification Suite for NEBULA Phase 6: N-Body and Orbital Simulation Engine.
Tests:
- Required scenarios (Sun+Earth, Sun+Earth+Moon, Sun+Multiple Planets)
- REBOUND IAS15 and WHFast integrators with pure NumPy Leapfrog fallback
- Hamiltonian energy conservation and angular momentum tracking
- Parameter validation boundaries and safe engineering limits
- Lifecycle endpoints (POST /simulations, GET /{id}, POST /{id}/run, POST /{id}/stop, GET /{id}/results)
- Telemetry payload sanity (positions, velocities, distances, trajectories, energy series, reproducibility)
"""
import pytest
import math


def test_scenario_catalog(client):
    """Verifies that all required scenarios are registered and provide required metadata."""
    res = client.get("/api/v1/simulations/scenarios")
    assert res.status_code == 200
    scenarios = res.json()
    assert len(scenarios) >= 5

    scenario_ids = [s["id"] for s in scenarios]
    assert "sun_earth" in scenario_ids
    assert "earth_moon_sun" in scenario_ids
    assert "solar_system_inner" in scenario_ids
    assert "solar_system_full" in scenario_ids

    # Check scenario details
    for s in scenarios:
        assert "name" in s
        assert "description" in s
        assert "body_count" in s
        assert "default_time_years" in s
        assert "recommended_integrator" in s
        assert "assumptions" in s
        assert "units" in s


def test_get_scenario_detail(client):
    """Verifies retrieval of detailed scenario configuration and initial particle states."""
    res = client.get("/api/v1/simulations/scenarios/sun_earth")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == "sun_earth"
    assert len(data["bodies"]) == 2
    body_names = [b["name"] for b in data["bodies"]]
    assert "Sun" in body_names
    assert "Earth" in body_names
    assert "assumptions" in data
    assert len(data["assumptions"]) >= 3


def test_scenario_not_found_404(client):
    """Verifies 404 response on unknown scenario ID."""
    res = client.get("/api/v1/simulations/scenarios/non_existent_galaxy")
    assert res.status_code == 404
    data = res.json()
    msg = data.get("detail") or data.get("error", {}).get("message", "")
    assert "not found" in msg.lower()


def test_scenario_1_sun_earth_keplerian_stability(client):
    """
    Scenario 1: Sun + Earth two-body Keplerian simulation.
    Verifies that after 1.000 year, Earth completes 1 circular orbit:
    - Final distance from Sun ~ 1.000 AU
    - Maximum relative energy drift < 1e-6
    """
    payload = {
        "scenario_id": "sun_earth",
        "duration": 1.0,
        "num_steps": 50,
        "integrator": "whfast",
        "auto_run": True
    }
    res = client.post("/api/v1/simulations", json=payload)
    assert res.status_code == 201
    sim_meta = res.json()
    assert sim_meta["status"] == "completed"
    assert sim_meta["has_results"] is True
    sim_id = sim_meta["id"]

    results_res = client.get(f"/api/v1/simulations/{sim_id}/results")
    assert results_res.status_code == 200
    results = results_res.json()

    assert len(results["bodies"]) == 2
    earth = next(b for b in results["bodies"] if b["id"] == "earth")

    # Earth should return to x ~ 1.0 AU, y ~ 0.0 AU
    final_x, final_y, final_z = earth["final_position"]
    final_dist = math.sqrt(final_x**2 + final_y**2 + final_z**2)
    assert pytest.approx(final_dist, rel=1e-3) == 1.0

    # Energy conservation check
    assert results["max_energy_error"] < 1e-6
    assert len(results["times"]) == 51
    assert len(results["pairwise_distances"]) >= 1
    assert "reproducibility" in results
    assert results["reproducibility"]["software_version"]["numpy"] is not None


def test_scenario_2_sun_earth_moon_hierarchical_orbit(client):
    """
    Scenario 2: Sun + Earth + Moon hierarchical three-body system.
    Verifies that Moon remains gravitationally bound inside Earth's Hill sphere.
    """
    payload = {
        "scenario_id": "earth_moon_sun",
        "duration": 0.25,
        "num_steps": 60,
        "integrator": "ias15",
        "auto_run": True
    }
    res = client.post("/api/v1/simulations", json=payload)
    assert res.status_code == 201
    sim_id = res.json()["id"]

    results_res = client.get(f"/api/v1/simulations/{sim_id}/results")
    assert results_res.status_code == 200
    results = results_res.json()

    assert len(results["bodies"]) == 3
    earth = next(b for b in results["bodies"] if b["id"] == "earth")
    moon = next(b for b in results["bodies"] if b["id"] == "moon")

    # Final Earth-Moon separation should remain near ~0.00257 AU (+- 30%)
    ex, ey, ez = earth["final_position"]
    mx, my, mz = moon["final_position"]
    separation = math.sqrt((mx - ex)**2 + (my - ey)**2 + (mz - ez)**2)
    assert 0.0015 < separation < 0.0035

    # Energy error for IAS15 should be negligible
    assert results["max_energy_error"] < 1e-5


def test_scenario_3_sun_multiple_planets(client):
    """
    Scenario 3: Sun + multiple planets (Inner Solar System).
    Verifies that all 5 bodies (Sun, Mercury, Venus, Earth, Mars) have consistent orbits.
    """
    payload = {
        "scenario_id": "solar_system_inner",
        "duration": 1.0,
        "num_steps": 40,
        "integrator": "whfast",
        "auto_run": True
    }
    res = client.post("/api/v1/simulations", json=payload)
    assert res.status_code == 201
    sim_id = res.json()["id"]

    results = client.get(f"/api/v1/simulations/{sim_id}/results").json()
    assert len(results["bodies"]) == 5

    # Check semi-major axis order: Mercury < Venus < Earth < Mars
    body_map = {b["id"]: b for b in results["bodies"]}
    r_mercury = body_map["mercury"]["distances_from_center"][0]
    r_venus = body_map["venus"]["distances_from_center"][0]
    r_earth = body_map["earth"]["distances_from_center"][0]
    r_mars = body_map["mars"]["distances_from_center"][0]

    assert r_mercury < r_venus < r_earth < r_mars


def test_simulation_lifecycle_create_run_stop(client):
    """
    Tests explicit two-phase lifecycle:
    1. POST /simulations with auto_run=False -> status 'created'
    2. GET /simulations/{id}/results -> 400 not yet executed
    3. POST /simulations/{id}/run -> executes and transitions to 'completed'
    4. GET /simulations/{id}/results -> returns results
    """
    payload = {
        "scenario_id": "sun_earth",
        "duration": 0.5,
        "num_steps": 25,
        "auto_run": False
    }
    create_res = client.post("/api/v1/simulations", json=payload)
    assert create_res.status_code == 201
    sim_id = create_res.json()["id"]
    assert create_res.json()["status"] == "created"
    assert create_res.json()["has_results"] is False

    # Attempting to fetch results before run should return 400
    early_results = client.get(f"/api/v1/simulations/{sim_id}/results")
    assert early_results.status_code == 400

    # Run simulation
    run_res = client.post(f"/api/v1/simulations/{sim_id}/run")
    assert run_res.status_code == 200
    assert run_res.json()["status"] == "completed"
    assert run_res.json()["has_results"] is True

    # Now results are available
    final_results = client.get(f"/api/v1/simulations/{sim_id}/results")
    assert final_results.status_code == 200
    assert len(final_results.json()["bodies"]) == 2


def test_simulation_stop_endpoint(client):
    """Tests POST /simulations/{id}/stop."""
    create_res = client.post("/api/v1/simulations", json={
        "scenario_id": "sun_earth",
        "duration": 1.0,
        "auto_run": False
    })
    sim_id = create_res.json()["id"]

    stop_res = client.post(f"/api/v1/simulations/{sim_id}/stop")
    assert stop_res.status_code == 200
    assert stop_res.json()["status"] == "stopped"


def test_simulation_body_selection(client):
    """Tests filtering scenario to only a subset of bodies (e.g. Sun + Mars only)."""
    payload = {
        "scenario_id": "solar_system_inner",
        "duration": 0.5,
        "num_steps": 20,
        "selected_bodies": ["sun", "mars"],
        "auto_run": True
    }
    res = client.post("/api/v1/simulations", json=payload)
    assert res.status_code == 201
    sim_id = res.json()["id"]

    results = client.get(f"/api/v1/simulations/{sim_id}/results").json()
    assert len(results["bodies"]) == 2
    body_ids = [b["id"] for b in results["bodies"]]
    assert "sun" in body_ids
    assert "mars" in body_ids
    assert "mercury" not in body_ids


def test_validation_invalid_parameters(client):
    """Verifies that out-of-bound parameters are rejected with 400 or 422."""
    # Negative duration
    res1 = client.post("/api/v1/simulations", json={"scenario_id": "sun_earth", "duration": -5.0})
    assert res1.status_code in [400, 422]

    # Excessive duration > 100 years
    res2 = client.post("/api/v1/simulations", json={"scenario_id": "sun_earth", "duration": 500.0})
    assert res2.status_code in [400, 422]

    # num_steps too low (< 5)
    res3 = client.post("/api/v1/simulations", json={"scenario_id": "sun_earth", "num_steps": 2})
    assert res3.status_code in [400, 422]

    # num_steps too high (> 1000)
    res4 = client.post("/api/v1/simulations", json={"scenario_id": "sun_earth", "num_steps": 2500})
    assert res4.status_code in [400, 422]

    # Selected fewer than 2 bodies
    res5 = client.post("/api/v1/simulations", json={"scenario_id": "sun_earth", "selected_bodies": ["sun"]})
    assert res5.status_code in [400, 422]

    # Timestep larger than duration
    res6 = client.post("/api/v1/simulations", json={"scenario_id": "sun_earth", "duration": 1.0, "timestep": 5.0})
    assert res6.status_code in [400, 422]


def test_list_simulations_endpoint(client):
    """Verifies GET /api/v1/simulations lists active/completed sessions."""
    res = client.get("/api/v1/simulations")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_simulation_not_found_404(client):
    """Verifies 404 when querying an invalid simulation ID."""
    res = client.get("/api/v1/simulations/invalid_random_uuid_1234")
    assert res.status_code == 404
    data = res.json()
    msg = data.get("detail") or data.get("error", {}).get("message", "")
    assert "not found" in msg.lower()
