def test_hohmann_transfer(client):
    payload = {
        "origin_id": "earth",
        "target_id": "mars"
    }
    res = client.post("/api/v1/calculate/hohmann", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["origin_name"] == "Earth"
    assert data["target_name"] == "Mars"
    assert 5.0 < data["total_delta_v_km_s"] < 6.5
    assert 240 < data["transfer_time_days"] < 280

def test_hill_sphere(client):
    payload = {
        "object_id": "earth"
    }
    res = client.post("/api/v1/calculate/hill-sphere", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert 1400000 < data["hill_radius_km"] < 1600000

def test_roche_limit(client):
    payload = {
        "primary_radius_km": 6371.0,
        "primary_density_g_cm3": 5.51,
        "secondary_density_g_cm3": 3.34
    }
    res = client.post("/api/v1/calculate/roche-limit", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["rigid_roche_limit_km"] > 6371.0
    assert data["fluid_roche_limit_km"] > data["rigid_roche_limit_km"]

def test_resonance(client):
    payload = {
        "period_days_1": 60189.0, # Neptune
        "period_days_2": 90560.0, # Pluto
        "max_order": 8
    }
    res = client.post("/api/v1/calculate/resonance", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["has_resonance"] is True
    ratios = [r["ratio_str"] for r in data["resonances_found"]]
    assert "3:2" in ratios
