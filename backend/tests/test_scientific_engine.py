"""
Automated numerical test suite for NEBULA Scientific Computation Engine.
Validates gravitational physics, Keplerian orbital mechanics, distance metrics,
coordinate frames, and Astropy unit conversions against known empirical benchmarks.
"""
import pytest
import math
from starlette.testclient import TestClient
import numpy as np

from app.scientific import (
    # Constants
    G_CONST,
    M_SUN,
    M_EARTH,
    R_EARTH,
    R_EARTH_MEAN,
    AU_METERS,
    SPEED_OF_LIGHT,
    # Gravity
    calculate_gravitational_force,
    calculate_gravitational_force_vector,
    calculate_surface_gravity,
    calculate_gravitational_potential,
    # Orbital
    calculate_circular_velocity,
    calculate_vis_viva_velocity,
    calculate_escape_velocity,
    calculate_apsidal_velocities,
    calculate_orbital_period,
    calculate_synodic_period,
    calculate_orbital_parameters,
    # Distances
    calculate_euclidean_distance,
    calculate_light_travel_time,
    calculate_angular_diameter,
    calculate_distance_modulus,
    calculate_distance_from_modulus,
    # Coordinates
    cartesian_to_spherical,
    spherical_to_cartesian,
    ecliptic_to_equatorial,
    equatorial_to_ecliptic,
    # Units
    convert_units
)

# ==================== 1. GRAVITATIONAL FORCE TESTS ====================

def test_gravitational_force_earth_sun():
    """Verify gravitational attraction between Sun and Earth at 1 AU (~3.54e22 N)."""
    res = calculate_gravitational_force(M_SUN, M_EARTH, AU_METERS)
    expected_force = G_CONST * M_SUN * M_EARTH / (AU_METERS ** 2)
    assert res["force_newtons"] == pytest.approx(expected_force, rel=1e-5)
    assert res["force_newtons"] == pytest.approx(3.54e22, rel=0.02)
    assert res["force_kilonewtons"] == pytest.approx(res["force_newtons"] / 1000.0)

def test_gravitational_force_vector():
    """Verify vector gravitational force points along the displacement vector."""
    pos1 = [0.0, 0.0, 0.0]
    pos2 = [AU_METERS, 0.0, 0.0]
    res = calculate_gravitational_force_vector(M_SUN, M_EARTH, pos1, pos2)
    assert res["force_magnitude_n"] == pytest.approx(3.54e22, rel=0.02)
    assert res["force_vector_n"][0] == pytest.approx(res["force_magnitude_n"], rel=1e-5)
    assert res["force_vector_n"][1] == pytest.approx(0.0, abs=1e-5)
    assert res["force_vector_n"][2] == pytest.approx(0.0, abs=1e-5)

def test_surface_gravity_earth():
    """Verify standard Earth surface gravity g ~ 9.81 m/s^2 (1.00 gee)."""
    res = calculate_surface_gravity(M_EARTH, R_EARTH_MEAN)
    assert res["gravity_m_s2"] == pytest.approx(9.82, rel=0.01)
    assert res["gravity_earth_gees"] == pytest.approx(1.0, rel=0.01)

def test_gravitational_potential():
    """Verify gravitational potential of the Sun at 1 AU."""
    res = calculate_gravitational_potential(M_SUN, AU_METERS, M_EARTH)
    expected_phi = -G_CONST * M_SUN / AU_METERS
    assert res["potential_j_kg"] == pytest.approx(expected_phi, rel=1e-5)
    assert res["potential_j_kg"] == pytest.approx(-8.87e8, rel=0.02)
    assert res["potential_energy_joules"] == pytest.approx(expected_phi * M_EARTH, rel=1e-5)

# ==================== 2. ORBITAL VELOCITY TESTS ====================

def test_circular_orbital_velocity_earth():
    """Verify Earth's mean orbital speed is ~29.78 km/s."""
    res = calculate_circular_velocity(M_SUN, AU_METERS)
    assert res["velocity_km_s"] == pytest.approx(29.78, rel=0.01)
    assert res["velocity_m_s"] == pytest.approx(29780.0, rel=0.01)

def test_escape_velocity_earth():
    """Verify Earth's surface escape velocity is ~11.19 km/s (sqrt(2) * v_circ)."""
    res = calculate_escape_velocity(M_EARTH, R_EARTH_MEAN)
    assert res["escape_velocity_km_s"] == pytest.approx(11.19, rel=0.01)

def test_vis_viva_velocity_at_perihelion():
    """Verify vis-viva equation matches apsidal velocity for eccentric orbit."""
    a = 1.0 * AU_METERS
    e = 0.2
    r_peri = a * (1.0 - e)
    vis = calculate_vis_viva_velocity(M_SUN, r_peri, a)
    aps = calculate_apsidal_velocities(M_SUN, a, e)
    assert vis["velocity_km_s"] == pytest.approx(aps["periapsis_velocity_km_s"], rel=1e-5)
    assert aps["periapsis_velocity_km_s"] > aps["apoapsis_velocity_km_s"]

# ==================== 3. ORBITAL PERIOD TESTS ====================

def test_orbital_period_earth_kepler():
    """Verify 1 AU orbit around Sun yields ~365.25 days."""
    res = calculate_orbital_period(AU_METERS, M_SUN, M_EARTH)
    assert res["period_days"] == pytest.approx(365.25, rel=0.005)
    assert res["period_years"] == pytest.approx(1.0, rel=0.005)

def test_synodic_period_earth_mars():
    """Verify synodic period between Earth (365.25d) and Mars (686.98d) is ~780 days."""
    res = calculate_synodic_period(365.25, 686.98)
    assert res["synodic_period_days"] == pytest.approx(779.9, rel=0.01)
    assert res["synodic_period_years"] == pytest.approx(2.135, rel=0.01)

def test_orbital_parameters_ellipse():
    """Verify geometric parameters of Keplerian ellipse: b, p, energy, angular momentum."""
    a = 10.0 * AU_METERS
    e = 0.5
    res = calculate_orbital_parameters(a, e, M_SUN)
    assert res["orbit_type"] == "Elliptic"
    assert res["semi_minor_axis_m"] == pytest.approx(a * math.sqrt(1 - 0.25), rel=1e-5)
    assert res["semi_latus_rectum_m"] == pytest.approx(a * (1 - 0.25), rel=1e-5)
    assert res["periapsis_distance_m"] == pytest.approx(a * 0.5, rel=1e-5)
    assert res["apoapsis_distance_m"] == pytest.approx(a * 1.5, rel=1e-5)
    assert res["specific_orbital_energy_j_kg"] < 0  # Bound orbit has negative energy

# ==================== 4. DISTANCE & LIGHT TRAVEL TESTS ====================

def test_light_travel_time_sun_to_earth():
    """Verify light travel time from Sun to Earth is ~499 seconds (~8.32 minutes)."""
    res = calculate_light_travel_time(AU_METERS)
    assert res["light_time_seconds"] == pytest.approx(499.0, rel=0.005)
    assert res["light_time_minutes"] == pytest.approx(8.317, rel=0.005)

def test_angular_diameter_sun():
    """Verify apparent angular diameter of the Sun from 1 AU is ~32 arcminutes (0.53 deg)."""
    d_sun = 2.0 * 6.957e8
    res = calculate_angular_diameter(d_sun, AU_METERS)
    assert res["angular_diameter_deg"] == pytest.approx(0.533, rel=0.01)
    assert res["angular_diameter_arcmin"] == pytest.approx(32.0, rel=0.01)

def test_distance_modulus_10pc():
    """Verify distance modulus at 10 pc is 0.0 mag, and round-trip inversion matches."""
    res = calculate_distance_modulus(10.0)
    assert res["distance_modulus_mag"] == pytest.approx(0.0, abs=1e-5)

    inv = calculate_distance_from_modulus(res["distance_modulus_mag"])
    assert inv["distance_pc"] == pytest.approx(10.0, rel=1e-5)

    res_100pc = calculate_distance_modulus(100.0)
    assert res_100pc["distance_modulus_mag"] == pytest.approx(5.0, abs=1e-5)

# ==================== 5. COORDINATE TRANSFORMATION TESTS ====================

def test_cartesian_to_spherical_and_back():
    """Verify 3D Cartesian and Spherical coordinate round-trip consistency."""
    x, y, z = 3.0, 4.0, 5.0
    sph = cartesian_to_spherical(x, y, z)
    assert sph["radius"] == pytest.approx(math.sqrt(50), rel=1e-5)

    cart = spherical_to_cartesian(sph["radius"], sph["theta_rad"], sph["phi_rad"])
    assert cart["x"] == pytest.approx(x, rel=1e-5)
    assert cart["y"] == pytest.approx(y, rel=1e-5)
    assert cart["z"] == pytest.approx(z, rel=1e-5)

def test_ecliptic_equatorial_vernal_equinox():
    """Verify vernal equinox (0 deg, 0 deg) transforms to (0 deg RA, 0 deg Dec)."""
    eq = ecliptic_to_equatorial(0.0, 0.0)
    assert eq["right_ascension_deg"] == pytest.approx(0.0, abs=1e-5)
    assert eq["declination_deg"] == pytest.approx(0.0, abs=1e-5)

    # Round trip
    ecl = equatorial_to_ecliptic(eq["right_ascension_deg"], eq["declination_deg"])
    assert ecl["ecliptic_lon_deg"] == pytest.approx(0.0, abs=1e-5)
    assert ecl["ecliptic_lat_deg"] == pytest.approx(0.0, abs=1e-5)

def test_ecliptic_summer_solstice():
    """Verify summer solstice (90 deg ecliptic longitude) declination matches Earth obliquity (~23.44 deg)."""
    eq = ecliptic_to_equatorial(90.0, 0.0)
    assert eq["right_ascension_deg"] == pytest.approx(90.0, rel=1e-3)
    assert eq["declination_deg"] == pytest.approx(23.439, rel=1e-3)

# ==================== 6. ASTROPY UNIT CONVERSION TESTS ====================

def test_unit_conversions_astronomy():
    """Verify exact dimensional conversions for solar mass, AU, parsecs, and velocity."""
    # 1 Solar mass to kg
    res_m = convert_units(1.0, "M_sun", "kg")
    assert res_m["converted_value"] == pytest.approx(M_SUN, rel=1e-4)

    # 1 AU to meters
    res_au = convert_units(1.0, "AU", "m")
    assert res_au["converted_value"] == pytest.approx(AU_METERS, rel=1e-5)

    # 1 Parsec to light-years (~3.26 ly)
    res_pc = convert_units(1.0, "pc", "ly")
    assert res_pc["converted_value"] == pytest.approx(3.26156, rel=0.005)

    # Temperature conversion (0 C = 273.15 K)
    res_temp = convert_units(0.0, "celsius", "kelvin")
    assert res_temp["converted_value"] == pytest.approx(273.15, rel=1e-5)

    # Speed of light in km/s (~299792 km/s)
    res_c = convert_units(1.0, "c", "km/s")
    assert res_c["converted_value"] == pytest.approx(299792.458, rel=1e-4)

# ==================== 7. INVALID INPUTS & BOUNDARY TESTS ====================

def test_invalid_negative_mass_force():
    """Verify negative mass raises ValueError."""
    with pytest.raises(ValueError, match="strictly positive"):
        calculate_gravitational_force(-5.0, 100.0, 1000.0)

def test_invalid_zero_distance_gravity():
    """Verify zero distance raises ValueError."""
    with pytest.raises(ValueError, match="strictly positive"):
        calculate_surface_gravity(1e24, 0.0)

def test_invalid_eccentricity_vis_viva():
    """Verify parabolic/hyperbolic eccentricity (> 1) raises ValueError for apsidal velocity."""
    with pytest.raises(ValueError, match="Eccentricity for bound"):
        calculate_apsidal_velocities(M_SUN, AU_METERS, 1.2)

def test_invalid_unit_conversion_incompatible():
    """Verify dimensionally incompatible conversion (e.g. mass to length) raises ValueError."""
    with pytest.raises(ValueError, match="Dimensionally incompatible"):
        convert_units(100.0, "kg", "AU")

def test_invalid_temperature_below_absolute_zero():
    """Verify temperature below absolute zero raises ValueError."""
    with pytest.raises(ValueError, match="absolute zero"):
        convert_units(-300.0, "deg_C", "K")

# ==================== 8. REST API INTEGRATION TESTS ====================

def test_api_gravity_force_endpoint(client: TestClient):
    """Verify /api/v1/calculate/gravity/force endpoint computes Earth-Sun attraction."""
    payload = {
        "object1_id": "sun",
        "object2_id": "earth",
        "distance_au": 1.0
    }
    res = client.post("/api/v1/calculate/gravity/force", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["name1"] == "Sun (Sol)"
    assert data["name2"] == "Earth"
    assert data["force_newtons"] == pytest.approx(3.54e22, rel=0.03)

def test_api_orbital_velocity_endpoint(client: TestClient):
    """Verify /api/v1/calculate/orbital-velocity endpoint returns circular and escape velocity."""
    payload = {
        "object_id": "earth",
        "distance_au": 1.0,
        "semi_major_axis_au": 1.0
    }
    res = client.post("/api/v1/calculate/orbital-velocity", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "circular_velocity" in data
    assert data["circular_velocity"]["velocity_km_s"] == pytest.approx(29.78, rel=0.02)

def test_api_orbital_period_endpoint(client: TestClient):
    """Verify /api/v1/calculate/orbital-period endpoint computes 365.25 days for Earth."""
    payload = {
        "semi_major_axis_au": 1.0,
        "central_mass_kg": M_SUN
    }
    res = client.post("/api/v1/calculate/orbital-period", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["period_days"] == pytest.approx(365.25, rel=0.01)

def test_api_unit_conversion_endpoint(client: TestClient):
    """Verify /api/v1/calculate/unit-conversion endpoint converts 1 M_sun to Earth masses."""
    payload = {
        "value": 1.0,
        "from_unit": "M_sun",
        "to_unit": "M_earth"
    }
    res = client.post("/api/v1/calculate/unit-conversion", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["converted_value"] == pytest.approx(332946.0, rel=0.01)

def test_api_coordinates_endpoint(client: TestClient):
    """Verify /api/v1/calculate/coordinates endpoint converts Cartesian to spherical."""
    payload = {
        "conversion_type": "cartesian_to_spherical",
        "x": 1.0,
        "y": 1.0,
        "z": 0.0
    }
    res = client.post("/api/v1/calculate/coordinates", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["radius"] == pytest.approx(math.sqrt(2.0), rel=1e-5)
    assert data["phi_deg"] == pytest.approx(45.0, rel=1e-5)

def test_api_invalid_input_validation(client: TestClient):
    """Verify API handles invalid input with HTTP 400 error response."""
    # Negative mass
    res = client.post("/api/v1/calculate/gravity/force", json={"m1_kg": -10, "m2_kg": 50, "distance_m": 1000})
    assert res.status_code in (400, 422)

    # Incompatible units
    res_units = client.post("/api/v1/calculate/unit-conversion", json={"value": 10, "from_unit": "kg", "to_unit": "AU"})
    assert res_units.status_code == 400
    assert "incompatible" in str(res_units.json()).lower()
