import pytest
from app.data.seed_data import ASTRONOMICAL_CATALOG
from app.schemas.celestial import (
    Planet,
    Moon,
    Star,
    Exoplanet,
    Asteroid,
    Comet,
    GenericCelestialObject,
    create_astronomical_object,
    NormalizedCelestialBody
)
from app.data.providers.local_provider import LocalDataProvider
from app.data.validation import validate_celestial_object, validate_catalog

def test_specialized_models_instantiation():
    """Verify concrete specialized models don't force irrelevant fields."""
    # 1. Star
    sun_data = next(o for o in ASTRONOMICAL_CATALOG if o["id"] == "sun")
    sun = create_astronomical_object(sun_data)
    assert isinstance(sun, Star)
    assert sun.object_type == "Star"
    assert sun.mass == 1.98847e30
    assert sun.radius == 696340.0
    assert sun.gravity == 274.0
    assert sun.temperature == 5778.0
    assert sun.rotation_period is not None
    assert not hasattr(sun, "distance_from_sun") or getattr(sun, "distance_from_sun", None) is None

    # 2. Planet
    earth_data = next(o for o in ASTRONOMICAL_CATALOG if o["id"] == "earth")
    earth = create_astronomical_object(earth_data)
    assert isinstance(earth, Planet)
    assert earth.object_type == "Planet"
    assert earth.parent_object == "sun"
    assert earth.distance_from_sun == 1.0
    assert earth.orbital_period == 365.256
    assert earth.mass == 5.9722e24
    assert earth.radius == 6371.0
    assert earth.units["mass"] == "kg"
    assert earth.units["distance_from_sun"] == "AU"
    assert earth.orbital_parameters["eccentricity"] == 0.0167

    # 3. Moon
    moon_data = next(o for o in ASTRONOMICAL_CATALOG if o["id"] == "moon")
    moon = create_astronomical_object(moon_data)
    assert isinstance(moon, Moon)
    assert moon.object_type == "Moon"
    assert moon.parent_object == "earth"
    assert round(moon.orbital_period, 2) == 27.32
    assert moon.gravity == 1.62

    # 4. Exoplanet
    trap_data = next(o for o in ASTRONOMICAL_CATALOG if o["id"] == "trappist-1e")
    trap = create_astronomical_object(trap_data)
    assert isinstance(trap, Exoplanet)
    assert trap.object_type == "Exoplanet"
    assert trap.parent_object == "trappist-1"
    assert round(trap.orbital_period, 1) == 6.1

    # 5. Asteroid
    ceres_data = next(o for o in ASTRONOMICAL_CATALOG if o["id"] == "ceres")
    ceres = create_astronomical_object(ceres_data)
    assert isinstance(ceres, Asteroid)
    assert ceres.object_type == "Asteroid"
    assert ceres.distance_from_sun == 2.767

    # 6. Comet
    halley_data = next(o for o in ASTRONOMICAL_CATALOG if o["id"] == "1p-halley")
    halley = create_astronomical_object(halley_data)
    assert isinstance(halley, Comet)
    assert halley.object_type == "Comet"
    assert halley.orbital_period == 27500.0

    # 7. Generic
    sgra_data = next(o for o in ASTRONOMICAL_CATALOG if o["id"] == "sagittarius-a-star")
    sgra = create_astronomical_object(sgra_data)
    assert isinstance(sgra, GenericCelestialObject)
    assert sgra.mass == 8.26e36

@pytest.mark.anyio
async def test_local_data_provider():
    """Verify LocalDataProvider functions offline with all Phase 2 methods."""
    provider = LocalDataProvider()
    assert provider.provider_id == "local_curated"
    assert "NASA" in provider.get_source_metadata().source_name

    # Fetch all
    objs = await provider.fetch_all_objects()
    assert len(objs) >= 20

    # Fetch by ID
    mars = await provider.fetch_object_by_id("mars")
    assert mars is not None
    assert mars.name == "Mars"
    assert mars.object_type == "Planet"
    assert mars.distance_from_sun == 1.524

    # Search
    search_res = await provider.search_objects("jupiter", limit=5)
    assert len(search_res) >= 1
    assert any(o.id == "jupiter" for o in search_res)

    # Filter by type
    planets = await provider.filter_by_type("planet")
    assert len(planets) >= 8
    for p in planets:
        assert p.object_type == "Planet" or p.category == "Planet"

    # Health check
    health = await provider.health_check()
    assert health["is_offline_capable"] is True
    assert health["objects_available"] >= 20

def test_core_minimum_solar_system_present(client):
    """Verify at minimum Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune."""
    res = client.get("/api/v1/objects/")
    assert res.status_code == 200
    objs = res.json()
    ids = {o["id"] for o in objs}
    required = {
        "sun", "mercury", "venus", "earth", "moon",
        "mars", "jupiter", "saturn", "uranus", "neptune"
    }
    for req_id in required:
        assert req_id in ids, f"Required core celestial body '{req_id}' missing from catalog!"

def test_get_object_detail_phase2_fields(client):
    """Verify GET /api/v1/objects/{id} returns full normalized fields."""
    res = client.get("/api/v1/objects/jupiter")
    assert res.status_code == 200
    jup = res.json()

    # Core normalized Phase 2 fields
    assert jup["id"] == "jupiter"
    assert jup["name"] == "Jupiter"
    assert jup["object_type"] == "Planet"
    assert "description" in jup and len(jup["description"]) > 0
    assert jup["mass"] > 1e27
    assert jup["radius"] > 60000
    assert jup["gravity"] > 20
    assert jup["distance_from_sun"] > 5.0
    assert jup["orbital_period"] > 4000
    assert jup["rotation_period"] is not None
    assert jup["orbital_velocity"] > 10
    assert jup["temperature"] is not None
    assert jup["parent_object"] == "sun"
    assert "orbital_parameters" in jup
    assert "discovery_information" in jup
    assert "source" in jup
    assert "source_url" in jup
    assert "units" in jup
    assert jup["units"]["mass"] == "kg"
    assert jup["units"]["distance_from_sun"] == "AU"
    assert "metadata" in jup

def test_search_endpoint(client):
    """Verify GET /api/v1/objects/search?q="""
    res = client.get("/api/v1/objects/search?q=mars")
    assert res.status_code == 200
    data = res.json()
    assert data["total_matches"] >= 1
    assert any(r["id"] == "mars" for r in data["results"])

def test_filter_by_type_endpoint(client):
    """Verify GET /api/v1/objects/type/{type}"""
    # Planet
    res = client.get("/api/v1/objects/type/Planet")
    assert res.status_code == 200
    planets = res.json()
    assert len(planets) >= 8

    # Moon
    res_moon = client.get("/api/v1/objects/type/Moon")
    assert res_moon.status_code == 200
    moons = res_moon.json()
    assert len(moons) >= 3

    # Star
    res_star = client.get("/api/v1/objects/type/Star")
    assert res_star.status_code == 200
    stars = res_star.json()
    assert len(stars) >= 3

def test_pagination_and_sorting(client):
    """Verify pagination and sorting."""
    # Page 1
    res1 = client.get("/api/v1/objects/?page=1&page_size=5&sort_by=name&sort_order=asc&format=paginated")
    assert res1.status_code == 200
    p1 = res1.json()
    assert len(p1["items"]) == 5
    assert p1["page"] == 1
    assert p1["total_pages"] >= 4
    assert p1["has_next"] is True
    assert p1["has_prev"] is False

    # Page 2
    res2 = client.get("/api/v1/objects/?page=2&page_size=5&sort_by=name&sort_order=asc&format=paginated")
    assert res2.status_code == 200
    p2 = res2.json()
    assert len(p2["items"]) == 5
    assert p2["page"] == 2
    assert p2["has_prev"] is True

    # Items on p1 and p2 must be distinct
    p1_ids = {x["id"] for x in p1["items"]}
    p2_ids = {x["id"] for x in p2["items"]}
    assert p1_ids.isdisjoint(p2_ids)

def test_invalid_object_id_404(client):
    """Verify non-existent object ID returns 404."""
    res = client.get("/api/v1/objects/non_existent_celestial_body_999")
    assert res.status_code == 404

    res_type = client.get("/api/v1/objects/type/NonExistentCategory999")
    assert res_type.status_code == 404

def test_validation_engine_rules():
    """Verify validation engine catches missing, negative, and invalid values."""
    # Valid object
    valid_obj = {
        "id": "europa",
        "name": "Europa",
        "category": "Moon",
        "mass_kg": 4.8e22,
        "radius_km": 1560.8,
        "surface_gravity_m_s2": 1.315,
        "surface_temperature_k": 102.0,
        "orbital_period_days": 3.55,
        "semi_major_axis_au": 0.00448,
        "description_citizen": "Icy moon of Jupiter."
    }
    v_res = validate_celestial_object(valid_obj)
    assert v_res.is_valid is True

    # Invalid empty ID
    invalid_empty = {**valid_obj, "id": ""}
    assert validate_celestial_object(invalid_empty).is_valid is False

    # Invalid slug characters
    invalid_slug = {**valid_obj, "id": "INVALID SLUG WITH SPACES!"}
    assert validate_celestial_object(invalid_slug).is_valid is False

    # Negative mass
    invalid_mass = {**valid_obj, "mass_kg": -100.0}
    assert validate_celestial_object(invalid_mass).is_valid is False

    # Negative radius
    invalid_radius = {**valid_obj, "radius_km": -50.0}
    assert validate_celestial_object(invalid_radius).is_valid is False

    # Temperature below absolute zero
    invalid_temp = {**valid_obj, "surface_temperature_k": -1.0}
    assert validate_celestial_object(invalid_temp).is_valid is False

    # Test catalog validation with duplicate IDs
    cat_with_dup = [valid_obj, {**valid_obj, "name": "Europa Clone"}]
    report = validate_catalog(cat_with_dup)
    assert "europa" in report.duplicate_ids
    assert report.total_errors >= 1
