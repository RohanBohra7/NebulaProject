import pytest
from app.data.validation import validate_celestial_object, validate_catalog

def test_validate_valid_object():
    obj = {
        "id": "mars",
        "name": "Mars",
        "category": "Planet",
        "mass_kg": 6.4171e23,
        "radius_km": 3389.5,
        "surface_gravity_m_s2": 3.72,
        "mean_density_g_cm3": 3.93,
        "surface_temperature_k": 210.0,
        "semi_major_axis_au": 1.524,
        "orbital_period_days": 686.98,
        "description_citizen": "The Red Planet.",
        "description_student": "Fourth planet from the Sun.",
        "description_researcher": "Terrestrial planet with thin atmosphere."
    }
    result = validate_celestial_object(obj)
    assert result.is_valid is True
    assert len([i for i in result.issues if i.issue_type == "error"]) == 0
    assert result.physical_consistency_score >= 80.0

def test_validate_invalid_object_bounds():
    obj = {
        "id": "INVALID SLUG!",
        "name": "Broken Object",
        "category": "Planet",
        "mass_kg": -100.0, # Negative mass error
        "radius_km": 0.0,   # Zero radius error
        "surface_temperature_k": -5.0 # Below absolute zero error
    }
    result = validate_celestial_object(obj)
    assert result.is_valid is False
    error_fields = [i.field for i in result.issues if i.issue_type == "error"]
    assert "id" in error_fields
    assert "mass_kg" in error_fields
    assert "radius_km" in error_fields
    assert "surface_temperature_k" in error_fields

def test_validate_catalog_endpoint(client):
    res = client.get("/api/v1/data/validate")
    assert res.status_code == 200
    report = res.json()
    assert report["total_objects_inspected"] >= 20
    assert report["total_errors"] == 0
    assert report["quality_score_percent"] >= 90.0
    assert len(report["units_validated"]) > 0
