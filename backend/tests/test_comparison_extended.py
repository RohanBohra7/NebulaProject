def test_comparison_three_objects(client):
    payload = {
        "object_ids": ["earth", "mars", "jupiter"],
        "mode": "researcher"
    }
    res = client.post("/api/v1/compare/", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["compared_objects"]) == 3
    assert data["primary_reference"] == "Earth"
    assert len(data["calculated_ratios"]) == 2
    assert len(data["absolute_differences"]) == 2
    assert "radar_chart_metrics" in data
    assert "comparative_insights" in data
    assert "citizen" in data["comparative_insights"]
    assert "researcher" in data["comparative_insights"]

def test_comparison_four_objects(client):
    payload = {
        "object_ids": ["earth", "venus", "mars", "mercury"],
        "mode": "student"
    }
    res = client.post("/api/v1/compare/", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["compared_objects"]) == 4

def test_comparison_invalid_under_two(client):
    res = client.post("/api/v1/compare/", json={"object_ids": ["earth"]})
    assert res.status_code == 422 or res.status_code == 400

def test_comparison_invalid_object_id(client):
    res = client.post("/api/v1/compare/", json={"object_ids": ["earth", "nonexistent_planet_xyz"]})
    assert res.status_code == 404

def test_comparison_heterogeneous_types_missing_data(client):
    payload = {
        "object_ids": ["sun", "earth"],
        "mode": "researcher"
    }
    res = client.post("/api/v1/compare/", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["compared_objects"]) == 2
    assert "Sun" in data["primary_reference"]
    ratio = data["calculated_ratios"][0]
    assert ratio["target_id"] == "earth"
    assert ratio["mass_ratio"] is not None
    # Sun has no orbital period/distance/velocity around sun, so those ratios relative to Sun should handle missing data gracefully
    assert ratio["period_ratio"] is None or isinstance(ratio["period_ratio"], (float, int))

def test_comparison_with_distance_and_orbital_velocity(client):
    payload = {
        "object_ids": ["earth", "mars"],
        "mode": "student"
    }
    res = client.post("/api/v1/compare/", json=payload)
    assert res.status_code == 200
    data = res.json()
    ratio = data["calculated_ratios"][0]
    assert ratio["distance_ratio"] is not None
    assert ratio["distance_ratio"] > 1.0  # Mars is farther than Earth (1.52 AU vs 1.0 AU)
    assert ratio["velocity_ratio"] is not None
    assert ratio["velocity_ratio"] < 1.0  # Mars orbits slower than Earth (~24 km/s vs ~29.8 km/s)
    diff = data["absolute_differences"][0]
    assert diff["distance_diff_au"] is not None
    assert diff["orbital_velocity_diff_km_s"] is not None
