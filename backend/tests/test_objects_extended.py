def test_paginated_objects_endpoint(client):
    res = client.get("/api/v1/objects/?page=1&page_size=5")
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) == 5
    assert data["page"] == 1
    assert data["page_size"] == 5
    assert data["total_pages"] >= 4
    assert data["has_next"] is True

def test_sorting_objects_by_mass(client):
    res = client.get("/api/v1/objects/?sort_by=mass&sort_order=desc")
    assert res.status_code == 200
    objs = res.json()
    assert len(objs) >= 20
    # First item should be the most massive object (e.g. Andromeda Galaxy or Sagittarius A*)
    assert objs[0]["name"] in ["Messier 31 (Andromeda Galaxy)", "Sagittarius A*", "Sun", "Betelgeuse"]

def test_sorting_objects_by_name(client):
    res = client.get("/api/v1/objects/?sort_by=name&sort_order=asc")
    assert res.status_code == 200
    objs = res.json()
    names = [o["name"].lower() for o in objs]
    assert names == sorted(names)

def test_search_objects_endpoint(client):
    res = client.get("/api/v1/objects/search?q=mars")
    assert res.status_code == 200
    data = res.json()
    assert data["total_matches"] >= 1
    assert any(r["id"] == "mars" for r in data["results"])

def test_get_objects_by_type(client):
    res = client.get("/api/v1/objects/type/Planet")
    assert res.status_code == 200
    planets = res.json()
    assert len(planets) >= 8
    for p in planets:
        assert p["category"] == "Planet"

def test_object_detail_with_astropy_and_related(client):
    res = client.get("/api/v1/objects/jupiter")
    assert res.status_code == 200
    jup = res.json()
    assert jup["name"] == "Jupiter"
    
    # Check Astropy unit breakdown
    assert "astropy_units" in jup
    units = jup["astropy_units"]
    assert units["mass_jupiter"] is not None
    assert 0.9 < units["mass_jupiter"] < 1.1 # ~1.0 M_jup
    assert units["radius_jupiter"] is not None
    assert 0.9 < units["radius_jupiter"] < 1.1 # ~1.0 R_jup
    
    # Check Related objects (Jupiter's moons like Europa)
    assert "related_objects" in jup
    assert len(jup["related_objects"]) > 0
    rel_ids = [r["id"] for r in jup["related_objects"]]
    assert "europa" in rel_ids

    # Check Source metadata
    assert "source_metadata" in jup
    assert jup["source_metadata"]["source_name"] is not None
    assert jup["source_metadata"]["is_demo_seed"] is True

def test_filtering_by_rings_and_atmosphere(client):
    # Test filtering for objects with rings
    res_rings = client.get("/api/v1/objects/?has_rings=true")
    assert res_rings.status_code == 200
    ring_objs = res_rings.json()
    assert len(ring_objs) >= 1
    for o in ring_objs:
        assert o["has_rings"] is True

    # Test filtering for objects with atmosphere
    res_atmo = client.get("/api/v1/objects/?has_atmosphere=true")
    assert res_atmo.status_code == 200
    atmo_objs = res_atmo.json()
    assert len(atmo_objs) >= 1
    for o in atmo_objs:
        assert o["has_atmosphere"] is True

def test_filtering_by_mass_range(client):
    # Filter terrestrial planets (mass_earth_relative between 0.01 and 2.0)
    res = client.get("/api/v1/objects/?min_mass=0.01&max_mass=2.0")
    assert res.status_code == 200
    terrestrial = res.json()
    assert len(terrestrial) >= 3
    for o in terrestrial:
        assert 0.01 <= o["mass_earth_relative"] <= 2.0

def test_astropy_bridge_conversions():
    from app.scientific.astropy_bridge import compute_astropy_units
    earth_like = {
        "mass_kg": 5.9722e24,
        "radius_km": 6371.0,
        "semi_major_axis_au": 1.0,
        "surface_gravity_m_s2": 9.80665,
        "surface_temperature_k": 288.0
    }
    breakdown = compute_astropy_units(earth_like)
    assert breakdown is not None
    assert 0.99 < breakdown.mass_earth < 1.01
    assert 0.99 < breakdown.radius_earth < 1.01
    assert 0.99 < breakdown.surface_gravity_gees < 1.01
    assert 14.0 < breakdown.temperature_celsius < 16.0 # ~14.85 C
    assert breakdown.distance_au == 1.0
    assert breakdown.distance_parsec is not None
    assert breakdown.distance_light_years is not None

