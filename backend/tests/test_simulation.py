def test_list_simulation_scenarios(client):
    res = client.get("/api/v1/simulation/scenarios")
    assert res.status_code == 200
    scenarios = res.json()
    assert len(scenarios) >= 5
    ids = [s["id"] for s in scenarios]
    assert "solar_system_inner" in ids
    assert "figure_eight_choreography" in ids

def test_run_nbody_simulation(client):
    payload = {
        "scenario_id": "solar_system_inner",
        "integrator": "ias15",
        "total_time_years": 0.5,
        "num_steps": 50
    }
    res = client.post("/api/v1/simulation/run", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["bodies"]) == 5
    assert "energy_drift_series" in data
    assert "initial_energy" in data
