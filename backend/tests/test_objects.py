def test_list_objects(client):
    res = client.get("/api/v1/objects/")
    assert res.status_code == 200
    objects = res.json()
    assert len(objects) >= 20
    # Ensure Earth is present
    ids = [o["id"] for o in objects]
    assert "earth" in ids
    assert "sun" in ids
    assert "jupiter" in ids

def test_filter_objects_by_category(client):
    res = client.get("/api/v1/objects/?category=Planet")
    assert res.status_code == 200
    planets = res.json()
    assert len(planets) >= 8
    for p in planets:
        assert p["category"] == "Planet"

def test_get_object_by_id(client):
    res = client.get("/api/v1/objects/earth")
    assert res.status_code == 200
    obj = res.json()
    assert obj["name"] == "Earth"
    assert obj["mass_kg"] == 5.9722e24
    assert obj["semi_major_axis_au"] == 1.0
    assert "orbit_path_3d" in obj
    assert len(obj["orbit_path_3d"]) > 0

def test_get_object_not_found(client):
    res = client.get("/api/v1/objects/nonexistent_superstar_999")
    assert res.status_code == 404
