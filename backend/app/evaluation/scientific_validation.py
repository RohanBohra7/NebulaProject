"""
Scientific Validation Suite for NEBULA.
Empirically verifies calculated physical, orbital, and simulation properties
against IAU, NASA JPL Horizons, and Planetary Fact Sheet reference values.
Uses explicit physical tolerances without fabricated accuracy claims.
"""
import math
from typing import Dict, Any, List

from app.scientific.constants import (
    G_CONST,
    M_SUN,
    M_EARTH,
    R_EARTH,
    AU_METERS,
    G_EARTH_SURFACE
)
from app.scientific.gravity import calculate_surface_gravity
from app.scientific.orbital import (
    calculate_orbital_period,
    calculate_escape_velocity,
    calculate_circular_velocity
)
from app.scientific.orbital_mechanics import calculate_hohmann_transfer
from app.simulation.nbody_engine import simulate_scenario


def run_scientific_validation_suite() -> Dict[str, Any]:
    """
    Executes rigorous quantitative comparisons between NEBULA scientific solvers
    and peer-reviewed empirical ground truth datasets.
    """
    benchmarks: List[Dict[str, Any]] = []

    # 1. Earth Orbital Period (Kepler's Third Law with two-body correction)
    # Reference: NASA JPL Planetary Fact Sheet sidereal orbital period: 365.256 days
    res_period_earth = calculate_orbital_period(
        semi_major_axis_m=1.0 * AU_METERS,
        central_mass_kg=M_SUN,
        secondary_mass_kg=M_EARTH
    )
    val_period_earth = res_period_earth["period_days"]
    ref_period_earth = 365.256
    tol_period_earth = 0.05  # days tolerance
    abs_err_period_earth = abs(val_period_earth - ref_period_earth)
    benchmarks.append({
        "id": "val_earth_orbital_period",
        "property_name": "Earth Sidereal Orbital Period",
        "category": "orbital_period",
        "formula": "T = 2π * sqrt(a³ / (G * (M_☉ + M_⊕)))",
        "computed_value": round(val_period_earth, 4),
        "reference_value": ref_period_earth,
        "reference_source": "NASA JPL Planetary Fact Sheet (Sidereal Orbit)",
        "units": "days",
        "tolerance": tol_period_earth,
        "absolute_error": round(abs_err_period_earth, 5),
        "relative_error_pct": round((abs_err_period_earth / ref_period_earth) * 100.0, 4),
        "passed": bool(abs_err_period_earth <= tol_period_earth),
        "methodology_notes": "Two-body Newtonian Keplerian period at 1.000000 AU semi-major axis."
    })

    # 2. Mars Orbital Period
    # Mars semi-major axis: 1.523662 AU. Reference sidereal period: 686.980 days
    m_mars_kg = 6.4171e23
    r_mars_semi_major_m = 1.523662 * AU_METERS
    res_period_mars = calculate_orbital_period(
        semi_major_axis_m=r_mars_semi_major_m,
        central_mass_kg=M_SUN,
        secondary_mass_kg=m_mars_kg
    )
    val_period_mars = res_period_mars["period_days"]
    ref_period_mars = 686.980
    tol_period_mars = 0.50  # days tolerance
    abs_err_period_mars = abs(val_period_mars - ref_period_mars)
    benchmarks.append({
        "id": "val_mars_orbital_period",
        "property_name": "Mars Sidereal Orbital Period",
        "category": "orbital_period",
        "formula": "T = 2π * sqrt(a³ / (G * (M_☉ + M_♂)))",
        "computed_value": round(val_period_mars, 4),
        "reference_value": ref_period_mars,
        "reference_source": "NASA JPL Mars Fact Sheet",
        "units": "days",
        "tolerance": tol_period_mars,
        "absolute_error": round(abs_err_period_mars, 5),
        "relative_error_pct": round((abs_err_period_mars / ref_period_mars) * 100.0, 4),
        "passed": bool(abs_err_period_mars <= tol_period_mars),
        "methodology_notes": "Keplerian formulation with barycentric correction at 1.523662 AU."
    })

    # 3. Earth Surface Gravity
    # Reference: WGS84 standard gravity g0 = 9.80665 m/s²
    res_grav_earth = calculate_surface_gravity(mass_kg=M_EARTH, radius_m=R_EARTH)
    val_grav_earth = res_grav_earth["gravity_m_s2"]
    ref_grav_earth = 9.807
    tol_grav_earth = 0.03  # m/s² tolerance due to spherical radius assumption (6371 km)
    abs_err_grav_earth = abs(val_grav_earth - ref_grav_earth)
    benchmarks.append({
        "id": "val_earth_surface_gravity",
        "property_name": "Earth Surface Gravitational Acceleration",
        "category": "surface_gravity",
        "formula": "g = G * M / R²",
        "computed_value": round(val_grav_earth, 4),
        "reference_value": ref_grav_earth,
        "reference_source": "CODATA 2018 / WGS84 Standard (g₀)",
        "units": "m/s²",
        "tolerance": tol_grav_earth,
        "absolute_error": round(abs_err_grav_earth, 5),
        "relative_error_pct": round((abs_err_grav_earth / ref_grav_earth) * 100.0, 4),
        "passed": bool(abs_err_grav_earth <= tol_grav_earth),
        "methodology_notes": "Volumetric mean radius R = 6371.0 km under spherically symmetric point mass approximation."
    })

    # 4. Jupiter Surface Gravity
    # Mass = 1.8982e27 kg, Equatorial Radius = 7.1492e7 m. Reference: 24.79 m/s²
    m_jupiter_kg = 1.8982e27
    r_jupiter_m = 7.1492e7  # 1-bar standard equatorial radius (71,492 km)
    res_grav_jup = calculate_surface_gravity(mass_kg=m_jupiter_kg, radius_m=r_jupiter_m)
    val_grav_jup = res_grav_jup["gravity_m_s2"]
    ref_grav_jup = 24.79
    tol_grav_jup = 0.10  # m/s² tolerance
    abs_err_grav_jup = abs(val_grav_jup - ref_grav_jup)
    benchmarks.append({
        "id": "val_jupiter_surface_gravity",
        "property_name": "Jupiter Surface Gravity (1-bar level)",
        "category": "surface_gravity",
        "formula": "g = G * M / R²",
        "computed_value": round(val_grav_jup, 4),
        "reference_value": ref_grav_jup,
        "reference_source": "NASA Jupiter Fact Sheet (1 bar level)",
        "units": "m/s²",
        "tolerance": tol_grav_jup,
        "absolute_error": round(abs_err_grav_jup, 5),
        "relative_error_pct": round((abs_err_grav_jup / ref_grav_jup) * 100.0, 4),
        "passed": bool(abs_err_grav_jup <= tol_grav_jup),
        "methodology_notes": "Evaluated at standard 1-bar equatorial radius (R = 71,492 km) standard for gas giants."
    })

    # 5. Earth Escape Velocity
    # Reference: 11.186 km/s
    res_esc_earth = calculate_escape_velocity(mass_kg=M_EARTH, radius_m=R_EARTH)
    val_esc_earth = res_esc_earth["escape_velocity_km_s"]
    ref_esc_earth = 11.186
    tol_esc_earth = 0.05  # km/s tolerance
    abs_err_esc_earth = abs(val_esc_earth - ref_esc_earth)
    benchmarks.append({
        "id": "val_earth_escape_velocity",
        "property_name": "Earth Escape Velocity",
        "category": "escape_velocity",
        "formula": "v_esc = sqrt(2 * G * M / R)",
        "computed_value": round(val_esc_earth, 4),
        "reference_value": ref_esc_earth,
        "reference_source": "NASA Earth Fact Sheet",
        "units": "km/s",
        "tolerance": tol_esc_earth,
        "absolute_error": round(abs_err_esc_earth, 5),
        "relative_error_pct": round((abs_err_esc_earth / ref_esc_earth) * 100.0, 4),
        "passed": bool(abs_err_esc_earth <= tol_esc_earth),
        "methodology_notes": "Unpropelled parabolic trajectory escape speed neglecting atmospheric drag."
    })

    # 6. Moon Escape Velocity
    # Mass = 7.342e22 kg, Radius = 1.7374e6 m. Reference: 2.380 km/s
    m_moon_kg = 7.342e22
    r_moon_m = 1.7374e6
    res_esc_moon = calculate_escape_velocity(mass_kg=m_moon_kg, radius_m=r_moon_m)
    val_esc_moon = res_esc_moon["escape_velocity_km_s"]
    ref_esc_moon = 2.380
    tol_esc_moon = 0.04  # km/s tolerance
    abs_err_esc_moon = abs(val_esc_moon - ref_esc_moon)
    benchmarks.append({
        "id": "val_moon_escape_velocity",
        "property_name": "Moon Escape Velocity",
        "category": "escape_velocity",
        "formula": "v_esc = sqrt(2 * G * M / R)",
        "computed_value": round(val_esc_moon, 4),
        "reference_value": ref_esc_moon,
        "reference_source": "NASA Moon Fact Sheet",
        "units": "km/s",
        "tolerance": tol_esc_moon,
        "absolute_error": round(abs_err_esc_moon, 5),
        "relative_error_pct": round((abs_err_esc_moon / ref_esc_moon) * 100.0, 4),
        "passed": bool(abs_err_esc_moon <= tol_esc_moon),
        "methodology_notes": "Lunar surface escape speed under spherically symmetric point mass model."
    })

    # 7. Earth Mean Orbital Velocity
    # Formula: v_circ = sqrt(G * M_sun / r). Reference: 29.78 km/s
    res_vcirc_earth = calculate_circular_velocity(central_mass_kg=M_SUN, radius_m=1.0 * AU_METERS)
    val_vcirc_earth = res_vcirc_earth["velocity_km_s"]
    ref_vcirc_earth = 29.78
    tol_vcirc_earth = 0.15  # km/s tolerance
    abs_err_vcirc_earth = abs(val_vcirc_earth - ref_vcirc_earth)
    benchmarks.append({
        "id": "val_earth_orbital_velocity",
        "property_name": "Earth Mean Orbital Velocity",
        "category": "orbital_velocity",
        "formula": "v_circ = sqrt(G * M_☉ / r)",
        "computed_value": round(val_vcirc_earth, 4),
        "reference_value": ref_vcirc_earth,
        "reference_source": "NASA JPL Horizons Mean Orbital Speed",
        "units": "km/s",
        "tolerance": tol_vcirc_earth,
        "absolute_error": round(abs_err_vcirc_earth, 5),
        "relative_error_pct": round((abs_err_vcirc_earth / ref_vcirc_earth) * 100.0, 4),
        "passed": bool(abs_err_vcirc_earth <= tol_vcirc_earth),
        "methodology_notes": "Circular approximation at r = 1.0 AU. Instantaneous velocity varies 29.29 to 30.29 km/s."
    })

    # 8. Earth-to-Mars Hohmann Transfer Δv
    # r1 = 1.0 AU, r2 = 1.524 AU. Reference: Total Δv = 5.59 km/s
    res_hohmann = calculate_hohmann_transfer(r1_au=1.0, r2_au=1.524)
    val_hohmann_dv = res_hohmann["total_delta_v_km_s"]
    ref_hohmann_dv = 5.59
    tol_hohmann_dv = 0.10  # km/s tolerance
    abs_err_hohmann = abs(val_hohmann_dv - ref_hohmann_dv)
    benchmarks.append({
        "id": "val_earth_mars_hohmann_dv",
        "property_name": "Earth-to-Mars Hohmann Transfer Total Δv",
        "category": "trajectory_transfer",
        "formula": "Δv_tot = |v_t1 - v_c1| + |v_c2 - v_t2|",
        "computed_value": round(val_hohmann_dv, 4),
        "reference_value": ref_hohmann_dv,
        "reference_source": "Fundamentals of Astrodynamics (Bate, Mueller, White)",
        "units": "km/s",
        "tolerance": tol_hohmann_dv,
        "absolute_error": round(abs_err_hohmann, 5),
        "relative_error_pct": round((abs_err_hohmann / ref_hohmann_dv) * 100.0, 4),
        "passed": bool(abs_err_hohmann <= tol_hohmann_dv),
        "methodology_notes": "Coplanar circular orbit assumption neglecting planetary gravitational wells (heliocentric Δv)."
    })

    # 9. N-body Numerical Conservation Stability (Sun-Earth IAS15/Leapfrog)
    # Conservation of total Hamiltonian energy ΔE / |E_0|
    sim_res = simulate_scenario(
        scenario_id="sun_earth",
        integrator="ias15",
        total_time_years=1.0,
        num_steps=100
    )
    val_energy_err = float(sim_res["max_energy_error"])
    ref_energy_err = 0.0  # Theoretical conservation limit
    tol_energy_err = 1.0e-5  # Maximum permissible relative drift for IAS15
    benchmarks.append({
        "id": "val_nbody_energy_conservation",
        "property_name": "N-Body Hamiltonian Energy Conservation Drift",
        "category": "simulation_stability",
        "formula": "max_t |(E(t) - E_0) / E_0|",
        "computed_value": val_energy_err,
        "reference_value": ref_energy_err,
        "reference_source": "Analytical Hamiltonian Invariant (dE/dt = 0)",
        "units": "dimensionless relative drift",
        "tolerance": tol_energy_err,
        "absolute_error": round(val_energy_err, 9),
        "relative_error_pct": None,  # Reference is 0, percentage division by zero avoided
        "passed": bool(val_energy_err <= tol_energy_err),
        "methodology_notes": f"Simulated 1.0 year of Sun-Earth orbit using {sim_res['integrator']} ({sim_res['engine_used']}). Steps: 100."
    })

    total_benchmarks = len(benchmarks)
    passed_count = sum(1 for b in benchmarks if b["passed"])

    return {
        "suite_name": "NEBULA Empirical Astrophysical Validation Suite",
        "total_benchmarks": total_benchmarks,
        "passed_count": passed_count,
        "failed_count": total_benchmarks - passed_count,
        "all_passed": passed_count == total_benchmarks,
        "benchmarks": benchmarks,
        "scientific_disclaimer": (
            "Comparisons are evaluated with explicit physical tolerances representing "
            "standard astronomical approximations (point mass, unperturbed Keplerian orbits, "
            "spherical geometries). Exact equality is neither claimed nor scientifically expected."
        )
    }
