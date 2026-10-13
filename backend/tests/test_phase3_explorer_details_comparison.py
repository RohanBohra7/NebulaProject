import pytest
from starlette.testclient import TestClient

def test_phase3_explorer_search_endpoint(client: TestClient):
    """Verify search endpoint returns relevant results with snippets."""
    res = client.get("/api/v1/objects/search?q=earth")
    assert res.status_code == 200
    data = res.json()
    assert "query" in data
    assert data["query"] == "earth"
    assert data["total_matches"] >= 1
    assert any(r["id"] == "earth" for r in data["results"])

    # Test search for non-existent target
    res_none = client.get("/api/v1/objects/search?q=xyznonexistentworld999")
    assert res_none.status_code == 200
    data_none = res_none.json()
    assert data_none["total_matches"] == 0
    assert len(data_none["results"]) == 0

def test_phase3_explorer_filters_and_pagination(client: TestClient):
    """Verify object type filtering, sorting, and pagination."""
    # Filter by category
    res_planets = client.get("/api/v1/objects/?category=Planet")
    assert res_planets.status_code == 200
    planets = res_planets.json()
    items = planets if isinstance(planets, list) else planets.get("items", [])
    assert len(items) >= 8
    assert all(p["category"] == "Planet" or p.get("object_type") == "Planet" for p in items)

    # Filter by Moon
    res_moons = client.get("/api/v1/objects/?category=Moon")
    assert res_moons.status_code == 200
    moons = res_moons.json()
    moon_items = moons if isinstance(moons, list) else moons.get("items", [])
    assert any(m["id"] == "moon" for m in moon_items)

    # Paginated format
    res_paginated = client.get("/api/v1/objects/?format=paginated&page=1&page_size=4")
    assert res_paginated.status_code == 200
    pag = res_paginated.json()
    assert "items" in pag
    assert "total" in pag
    assert len(pag["items"]) == 4
    assert pag["page"] == 1
    assert pag["page_size"] == 4
    assert pag["has_next"] is True

def test_phase3_explorer_sorting(client: TestClient):
    """Verify sorting by mass, distance, and name."""
    res_mass_asc = client.get("/api/v1/objects/?format=paginated&sort_by=mass&sort_order=asc")
    assert res_mass_asc.status_code == 200
    data_mass = res_mass_asc.json()["items"]
    valid_masses = [x["mass_earth_relative"] for x in data_mass if x.get("mass_earth_relative") is not None]
    assert valid_masses == sorted(valid_masses)

    res_name_desc = client.get("/api/v1/objects/?format=paginated&sort_by=name&sort_order=desc")
    assert res_name_desc.status_code == 200
    names = [x["name"] for x in res_name_desc.json()["items"]]
    assert names == sorted(names, key=str.lower, reverse=True)

def test_phase3_object_details_complete_telemetry(client: TestClient):
    """Verify detailed object endpoint delivers all required sections and units."""
    res = client.get("/api/v1/objects/earth")
    assert res.status_code == 200
    obj = res.json()

    # Overview & Identification
    assert obj["id"] == "earth"
    assert obj["name"] == "Earth"
    assert obj["category"] == "Planet"
    assert "description_citizen" in obj
    assert "description_student" in obj
    assert "description_researcher" in obj

    # Physical Properties
    assert obj["mass_kg"] == pytest.approx(5.972e24, rel=1e-2)
    assert obj["radius_km"] == pytest.approx(6371.0, rel=1e-2)
    assert obj["surface_gravity_m_s2"] == pytest.approx(9.807, rel=1e-2)
    assert obj["mean_density_g_cm3"] == pytest.approx(5.514, rel=1e-2)
    assert obj["escape_velocity_km_s"] == pytest.approx(11.19, rel=1e-2)
    assert obj["surface_temperature_k"] is not None

    # Orbital Properties
    assert obj["semi_major_axis_au"] == pytest.approx(1.0, rel=1e-2)
    assert obj["orbital_period_days"] == pytest.approx(365.25, rel=1e-2)
    assert obj["mean_orbital_velocity_km_s"] == pytest.approx(29.78, rel=1e-2)
    assert obj["eccentricity"] == pytest.approx(0.0167, rel=1e-2)

    # Scientific Information (Astropy)
    assert "astropy_units" in obj
    assert obj["astropy_units"] is not None
    assert "mass_solar" in obj["astropy_units"]
    assert "radius_solar" in obj["astropy_units"]

    # Related Objects
    assert "related_objects" in obj
    assert isinstance(obj["related_objects"], list)
    assert any(r["id"] == "moon" for r in obj["related_objects"])

    # Source Provenance
    assert "source_metadata" in obj
    assert obj["source_metadata"]["confidence_level"] is not None
    assert "units" in obj
    assert obj["units"]["mass"] == "kg"
    assert obj["units"]["radius"] == "km"

def test_phase3_object_details_invalid_404(client: TestClient):
    """Verify accessing nonexistent celestial body returns clean 404."""
    res = client.get("/api/v1/objects/fictional_death_star_999")
    assert res.status_code == 404
    err = res.json()
    err_str = str(err).lower()
    assert "not found" in err_str

def test_phase3_comparison_two_objects(client: TestClient):
    """Verify comparing 2 objects computes dynamic ratios, differences, and charts."""
    payload = {
        "object_ids": ["earth", "mars"],
        "mode": "student"
    }
    res = client.post("/api/v1/compare/", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["compared_objects"]) == 2
    assert data["primary_reference"] == "Earth"

    # Ratios check
    assert len(data["calculated_ratios"]) == 1
    r = data["calculated_ratios"][0]
    assert r["target_name"] == "Mars"
    assert r["relative_to"] == "Earth"
    assert r["mass_ratio"] is not None
    assert r["mass_ratio"] < 1.0  # Mars is ~0.107 M_earth
    assert r["radius_ratio"] < 1.0  # Mars is smaller than Earth
    assert r["distance_ratio"] > 1.0  # Mars is further out (1.52 AU)

    # Absolute differences check
    assert len(data["absolute_differences"]) == 1
    d = data["absolute_differences"][0]
    assert d["radius_diff_km"] < 0  # Mars radius minus Earth radius is negative
    assert d["distance_diff_au"] > 0  # Mars is 0.52 AU further than Earth

    # Charts metrics check
    assert "radar_chart_metrics" in data
    assert len(data["radar_chart_metrics"]) >= 5
    assert "comparative_insights" in data
    assert "student" in data["comparative_insights"]

def test_phase3_comparison_four_objects(client: TestClient):
    """Verify comparing 4 objects scales up dynamically."""
    payload = {
        "object_ids": ["earth", "venus", "mars", "mercury"],
        "mode": "researcher"
    }
    res = client.post("/api/v1/compare/", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["compared_objects"]) == 4
    assert len(data["calculated_ratios"]) == 3
    assert len(data["absolute_differences"]) == 3

def test_phase3_comparison_missing_data_heterogeneous(client: TestClient):
    """Verify comparing heterogeneous classes (Star vs Planet) handles missing attributes gracefully without crashing."""
    payload = {
        "object_ids": ["sun", "earth", "moon"],
        "mode": "researcher"
    }
    res = client.post("/api/v1/compare/", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["compared_objects"]) == 3
    # Sun has no orbital velocity around sun or distance from sun, so target ratios for distance relative to Sun handle missing values cleanly
    for ratio in data["calculated_ratios"]:
        assert ratio["mass_ratio"] is not None  # Both Earth and Moon have mass relative to Sun
