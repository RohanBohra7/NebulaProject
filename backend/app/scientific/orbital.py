"""
Orbital mechanics and trajectory computation engine for NEBULA.
Implements Keplerian orbital elements, vis-viva equations, orbital periods,
velocities, Hohmann transfers, Hill spheres, Roche limits, and Lagrange points.
"""
import math
from typing import Dict, Any, List, Optional
import numpy as np
import astropy.units as u

from app.scientific.constants import (
    G_CONST,
    M_SUN,
    M_EARTH,
    AU_METERS,
    DAY_SECONDS,
    JULIAN_YEAR_DAYS,
    JULIAN_YEAR_SECONDS,
)

# ==================== ORBITAL VELOCITIES ====================

def calculate_circular_velocity(
    central_mass_kg: float,
    radius_m: float
) -> Dict[str, Any]:
    """
    Computes orbital speed for a stable circular orbit around a central mass.
    Formula: v_c = sqrt(G * M / r)

    :param central_mass_kg: Central body mass in kg (> 0)
    :param radius_m: Orbital radius in meters (> 0)
    :return: Velocity in m/s and km/s
    """
    if central_mass_kg <= 0:
        raise ValueError("Central mass must be strictly positive (> 0 kg).")
    if radius_m <= 0:
        raise ValueError("Orbital radius must be strictly positive (> 0 m).")

    mu = G_CONST * central_mass_kg
    v_m_s = math.sqrt(mu / radius_m)

    return {
        "velocity_m_s": float(v_m_s),
        "velocity_km_s": float(v_m_s / 1000.0),
        "central_mass_kg": float(central_mass_kg),
        "radius_m": float(radius_m),
        "radius_au": float(radius_m / AU_METERS),
        "formula": "v_circ = sqrt(G * M / r)"
    }

def calculate_vis_viva_velocity(
    central_mass_kg: float,
    distance_m: float,
    semi_major_axis_m: float
) -> Dict[str, Any]:
    """
    Computes instantaneous orbital speed along an eccentric Keplerian orbit via the Vis-Viva equation.
    Formula: v(r) = sqrt(mu * (2/r - 1/a))

    :param central_mass_kg: Central mass in kg (> 0)
    :param distance_m: Current instantaneous distance from central body in meters (> 0)
    :param semi_major_axis_m: Semi-major axis in meters (> 0)
    """
    if central_mass_kg <= 0:
        raise ValueError("Central mass must be strictly positive (> 0 kg).")
    if distance_m <= 0:
        raise ValueError("Distance must be strictly positive (> 0 m).")
    if semi_major_axis_m <= 0:
        raise ValueError("Semi-major axis must be strictly positive (> 0 m).")

    mu = G_CONST * central_mass_kg
    term = (2.0 / distance_m) - (1.0 / semi_major_axis_m)
    if term < 0:
        raise ValueError("Distance exceeds theoretical bound (2/r < 1/a), resulting in imaginary orbital velocity.")

    v_m_s = math.sqrt(mu * term)

    return {
        "velocity_m_s": float(v_m_s),
        "velocity_km_s": float(v_m_s / 1000.0),
        "distance_m": float(distance_m),
        "semi_major_axis_m": float(semi_major_axis_m),
        "formula": "v(r) = sqrt(G * M * (2/r - 1/a))"
    }

def calculate_escape_velocity(
    mass_kg: float,
    radius_m: float
) -> Dict[str, Any]:
    """
    Computes minimum speed required to break free from a spherical body's gravitational field without further propulsion.
    Formula: v_esc = sqrt(2 * G * M / R)

    :param mass_kg: Body mass in kg (> 0)
    :param radius_m: Body radius in meters (> 0)
    """
    if mass_kg <= 0:
        raise ValueError("Body mass must be strictly positive (> 0 kg).")
    if radius_m <= 0:
        raise ValueError("Body radius must be strictly positive (> 0 m).")

    mu = G_CONST * mass_kg
    v_esc_m_s = math.sqrt(2.0 * mu / radius_m)

    return {
        "escape_velocity_m_s": float(v_esc_m_s),
        "escape_velocity_km_s": float(v_esc_m_s / 1000.0),
        "mass_kg": float(mass_kg),
        "radius_m": float(radius_m),
        "formula": "v_esc = sqrt(2 * G * M / R)"
    }

def calculate_apsidal_velocities(
    central_mass_kg: float,
    semi_major_axis_m: float,
    eccentricity: float
) -> Dict[str, Any]:
    """
    Computes orbital velocity at periapsis (closest approach) and apoapsis (furthest distance).
    Formula:
      v_peri = sqrt((mu/a) * ((1 + e) / (1 - e)))
      v_apo  = sqrt((mu/a) * ((1 - e) / (1 + e)))
    """
    if central_mass_kg <= 0:
        raise ValueError("Central mass must be strictly positive (> 0 kg).")
    if semi_major_axis_m <= 0:
        raise ValueError("Semi-major axis must be strictly positive (> 0 m).")
    if eccentricity < 0 or eccentricity >= 1.0:
        raise ValueError("Eccentricity for bound elliptic orbits must be in the range [0, 1).")

    mu = G_CONST * central_mass_kg
    base = mu / semi_major_axis_m

    v_peri = math.sqrt(base * ((1.0 + eccentricity) / (1.0 - eccentricity)))
    v_apo = math.sqrt(base * ((1.0 - eccentricity) / (1.0 + eccentricity)))

    return {
        "periapsis_velocity_m_s": float(v_peri),
        "periapsis_velocity_km_s": float(v_peri / 1000.0),
        "apoapsis_velocity_m_s": float(v_apo),
        "apoapsis_velocity_km_s": float(v_apo / 1000.0),
        "velocity_ratio": float(v_peri / v_apo) if v_apo > 0 else 1.0,
        "eccentricity": float(eccentricity),
        "semi_major_axis_m": float(semi_major_axis_m)
    }

# ==================== ORBITAL PERIODS ====================

def calculate_orbital_period(
    semi_major_axis_m: float,
    central_mass_kg: float = M_SUN,
    secondary_mass_kg: float = 0.0
) -> Dict[str, Any]:
    """
    Computes Keplerian orbital period using full two-body formulation of Kepler's Third Law.
    Formula: P = 2 * pi * sqrt(a^3 / (G * (M_1 + M_2)))

    :param semi_major_axis_m: Orbit semi-major axis in meters (> 0)
    :param central_mass_kg: Primary body mass in kg (> 0)
    :param secondary_mass_kg: Secondary body mass in kg (>= 0)
    """
    if semi_major_axis_m <= 0:
        raise ValueError("Semi-major axis must be strictly positive (> 0 m).")
    if central_mass_kg <= 0:
        raise ValueError("Central mass must be strictly positive (> 0 kg).")
    if secondary_mass_kg < 0:
        raise ValueError("Secondary mass cannot be negative.")

    total_mass = central_mass_kg + secondary_mass_kg
    mu = G_CONST * total_mass

    period_sec = 2.0 * math.pi * math.sqrt((semi_major_axis_m ** 3) / mu)
    period_days = period_sec / DAY_SECONDS
    period_years = period_days / JULIAN_YEAR_DAYS

    # Mean motion
    mean_motion_rad_s = (2.0 * math.pi) / period_sec
    mean_motion_deg_day = (360.0 / period_days)

    return {
        "period_seconds": float(period_sec),
        "period_days": float(period_days),
        "period_years": float(period_years),
        "mean_motion_rad_s": float(mean_motion_rad_s),
        "mean_motion_deg_day": float(mean_motion_deg_day),
        "semi_major_axis_m": float(semi_major_axis_m),
        "semi_major_axis_au": float(semi_major_axis_m / AU_METERS),
        "formula": "P = 2 * pi * sqrt(a^3 / (G * (M1 + M2)))"
    }

def calculate_synodic_period(
    period1_days: float,
    period2_days: float
) -> Dict[str, Any]:
    """
    Computes synodic period between two bodies in mutual orbit around the same primary.
    Formula: 1 / P_syn = |1 / P1 - 1 / P2|

    :param period1_days: Orbital period of body 1 in days (> 0)
    :param period2_days: Orbital period of body 2 in days (> 0)
    """
    if period1_days <= 0 or period2_days <= 0:
        raise ValueError("Orbital periods must be strictly positive (> 0 days).")
    if math.isclose(period1_days, period2_days, rel_tol=1e-7):
        raise ValueError("Bodies with identical orbital periods have an infinite synodic period.")

    diff = abs((1.0 / period1_days) - (1.0 / period2_days))
    p_syn_days = 1.0 / diff
    p_syn_years = p_syn_days / JULIAN_YEAR_DAYS

    return {
        "synodic_period_days": float(p_syn_days),
        "synodic_period_years": float(p_syn_years),
        "period_inner_days": float(min(period1_days, period2_days)),
        "period_outer_days": float(max(period1_days, period2_days)),
        "formula": "1 / P_syn = |1/P1 - 1/P2|"
    }

# ==================== ORBITAL PARAMETERS ====================

def calculate_orbital_parameters(
    semi_major_axis_m: float,
    eccentricity: float,
    central_mass_kg: float = M_SUN
) -> Dict[str, Any]:
    """
    Computes geometry and conserved dynamic quantities of a Keplerian orbit.
    """
    if semi_major_axis_m <= 0:
        raise ValueError("Semi-major axis must be strictly positive (> 0 m).")
    if eccentricity < 0:
        raise ValueError("Eccentricity cannot be negative.")

    a = semi_major_axis_m
    e = eccentricity
    mu = G_CONST * central_mass_kg

    if e < 1.0:
        orbit_type = "Circular" if e == 0.0 else "Elliptic"
        b = a * math.sqrt(1.0 - e**2)
        p = a * (1.0 - e**2)
        r_peri = a * (1.0 - e)
        r_apo = a * (1.0 + e)
        specific_energy = -mu / (2.0 * a)
        specific_angular_momentum = math.sqrt(mu * p)
    elif e == 1.0:
        orbit_type = "Parabolic"
        b = None
        p = 2.0 * a
        r_peri = a
        r_apo = None
        specific_energy = 0.0
        specific_angular_momentum = math.sqrt(mu * p)
    else:
        orbit_type = "Hyperbolic"
        b = a * math.sqrt(e**2 - 1.0)
        p = a * (e**2 - 1.0)
        r_peri = a * (e - 1.0)
        r_apo = None
        specific_energy = mu / (2.0 * a)
        specific_angular_momentum = math.sqrt(mu * p)

    return {
        "orbit_type": orbit_type,
        "semi_major_axis_m": float(a),
        "semi_major_axis_au": float(a / AU_METERS),
        "eccentricity": float(e),
        "semi_minor_axis_m": float(b) if b is not None else None,
        "semi_minor_axis_au": float(b / AU_METERS) if b is not None else None,
        "semi_latus_rectum_m": float(p),
        "periapsis_distance_m": float(r_peri),
        "periapsis_distance_au": float(r_peri / AU_METERS),
        "apoapsis_distance_m": float(r_apo) if r_apo is not None else None,
        "apoapsis_distance_au": float(r_apo / AU_METERS) if r_apo is not None else None,
        "specific_orbital_energy_j_kg": float(specific_energy),
        "specific_angular_momentum_m2_s": float(specific_angular_momentum),
    }

# ==================== KEPLER SOLVERS & LEGACY COMPATIBILITY ====================

def solve_kepler(
    mean_anomaly_rad: float,
    eccentricity: float,
    tolerance: float = 1e-12,
    max_iter: int = 100
) -> float:
    """
    Solves Kepler's Equation M = E - e*sin(E) for Eccentric Anomaly E using Newton-Raphson iteration.
    """
    if eccentricity == 0.0:
        return mean_anomaly_rad

    if eccentricity < 0.8:
        e_anomaly = mean_anomaly_rad
    else:
        e_anomaly = math.pi if mean_anomaly_rad != 0 else 0.0

    for _ in range(max_iter):
        f = e_anomaly - eccentricity * math.sin(e_anomaly) - mean_anomaly_rad
        f_prime = 1.0 - eccentricity * math.cos(e_anomaly)
        delta = f / f_prime
        e_anomaly -= delta
        if abs(delta) < tolerance:
            break

    return e_anomaly

def eccentric_to_true_anomaly(e_anomaly_rad: float, eccentricity: float) -> float:
    """
    Converts Eccentric Anomaly E to True Anomaly nu using half-angle tangent relation.
    """
    if eccentricity >= 1.0:
        return e_anomaly_rad
    beta = eccentricity / (1.0 + math.sqrt(1.0 - eccentricity**2))
    nu = e_anomaly_rad + 2.0 * math.atan((beta * math.sin(e_anomaly_rad)) / (1.0 - beta * math.cos(e_anomaly_rad)))
    return nu

def orbital_elements_to_cartesian(
    semi_major_axis_au: float,
    eccentricity: float,
    inclination_deg: float,
    ascending_node_deg: float,
    arg_periapsis_deg: float,
    true_anomaly_deg: float,
    central_mass_kg: float = M_SUN
) -> Dict[str, Any]:
    """
    Converts Keplerian orbital elements to 3D Cartesian state vectors [x, y, z] (AU)
    and [vx, vy, vz] (km/s).
    """
    a_m = semi_major_axis_au * AU_METERS
    e = eccentricity
    i_rad = math.radians(inclination_deg)
    omega_rad = math.radians(ascending_node_deg)
    w_rad = math.radians(arg_periapsis_deg)
    nu_rad = math.radians(true_anomaly_deg)

    mu = G_CONST * central_mass_kg
    p_m = a_m * (1.0 - e**2) if e < 1.0 else a_m

    r_m = p_m / (1.0 + e * math.cos(nu_rad)) if (1.0 + e * math.cos(nu_rad)) > 0 else a_m

    x_peri = r_m * math.cos(nu_rad)
    y_peri = r_m * math.sin(nu_rad)

    h = math.sqrt(mu * p_m) if p_m > 0 else 0.0
    vx_peri = -(mu / h) * math.sin(nu_rad) if h > 0 else 0.0
    vy_peri = (mu / h) * (e + math.cos(nu_rad)) if h > 0 else 0.0

    cos_w = math.cos(w_rad)
    sin_w = math.sin(w_rad)
    cos_o = math.cos(omega_rad)
    sin_o = math.sin(omega_rad)
    cos_i = math.cos(i_rad)
    sin_i = math.sin(i_rad)

    px = cos_o * cos_w - sin_o * sin_w * cos_i
    py = sin_o * cos_w + cos_o * sin_w * cos_i
    pz = sin_w * sin_i

    qx = -cos_o * sin_w - sin_o * cos_w * cos_i
    qy = -sin_o * sin_w + cos_o * cos_w * cos_i
    qz = cos_w * sin_i

    x_m = x_peri * px + y_peri * qx
    y_m = x_peri * py + y_peri * qy
    z_m = x_peri * pz + y_peri * qz

    vx_m_s = vx_peri * px + vy_peri * qx
    vy_m_s = vx_peri * py + vy_peri * qy
    vz_m_s = vx_peri * pz + vy_peri * qz

    return {
        "position_au": [x_m / AU_METERS, y_m / AU_METERS, z_m / AU_METERS],
        "velocity_km_s": [vx_m_s / 1000.0, vy_m_s / 1000.0, vz_m_s / 1000.0],
        "distance_au": r_m / AU_METERS,
        "orbital_speed_km_s": math.sqrt(vx_m_s**2 + vy_m_s**2 + vz_m_s**2) / 1000.0
    }

def calculate_hohmann_transfer(
    r1_au: float,
    r2_au: float,
    central_mass_kg: float = M_SUN
) -> Dict[str, Any]:
    """
    Computes Hohmann Transfer trajectory between two coplanar circular orbits.
    """
    if r1_au <= 0 or r2_au <= 0:
        raise ValueError("Orbital radii must be strictly positive (> 0 AU).")
    if math.isclose(r1_au, r2_au, rel_tol=1e-7):
        raise ValueError("Origin and target orbits cannot have identical radii.")

    r1 = r1_au * AU_METERS
    r2 = r2_au * AU_METERS
    mu = G_CONST * central_mass_kg

    a_transfer = (r1 + r2) / 2.0
    v1_circ = math.sqrt(mu / r1)
    v2_circ = math.sqrt(mu / r2)

    v1_trans = math.sqrt(mu * (2.0 / r1 - 1.0 / a_transfer))
    v2_trans = math.sqrt(mu * (2.0 / r2 - 1.0 / a_transfer))

    delta_v1 = abs(v1_trans - v1_circ)
    delta_v2 = abs(v2_circ - v2_trans)
    total_delta_v = delta_v1 + delta_v2

    transfer_time_sec = math.pi * math.sqrt((a_transfer**3) / mu)
    transfer_time_days = transfer_time_sec / DAY_SECONDS

    eccentricity_transfer = abs(r2 - r1) / (r1 + r2)

    return {
        "origin_radius_au": r1_au,
        "target_radius_au": r2_au,
        "transfer_semi_major_axis_au": a_transfer / AU_METERS,
        "transfer_eccentricity": eccentricity_transfer,
        "delta_v1_km_s": round(delta_v1 / 1000.0, 3),
        "delta_v2_km_s": round(delta_v2 / 1000.0, 3),
        "total_delta_v_km_s": round(total_delta_v / 1000.0, 3),
        "transfer_time_days": round(transfer_time_days, 1),
        "scientific_formulation": {
            "a_trans": "a_{trans} = (r_1 + r_2) / 2",
            "delta_v1": "\\Delta v_1 = |\\sqrt{\\mu(2/r_1 - 1/a_{trans})} - \\sqrt{\\mu/r_1}|",
            "delta_v2": "\\Delta v_2 = |\\sqrt{\\mu/r_2} - \\sqrt{\\mu(2/r_2 - 1/a_{trans})}|",
            "transfer_time": "T_{trans} = \\pi \\sqrt{a_{trans}^3 / \\mu}"
        }
    }

def calculate_hill_sphere(
    semi_major_axis_au: float,
    eccentricity: float,
    body_mass_kg: float,
    parent_mass_kg: float = M_SUN
) -> Dict[str, Any]:
    """
    Computes Hill Sphere radius where the body's gravity dominates over primary tidal forces.
    """
    if parent_mass_kg <= 0 or body_mass_kg <= 0 or semi_major_axis_au <= 0:
        raise ValueError("Masses and semi-major axis must be strictly positive.")

    a_m = semi_major_axis_au * AU_METERS
    mass_ratio = body_mass_kg / (3.0 * parent_mass_kg)
    r_hill_m = a_m * (1.0 - eccentricity) * (mass_ratio ** (1.0 / 3.0))

    return {
        "hill_radius_km": round(r_hill_m / 1000.0, 1),
        "hill_radius_au": round(r_hill_m / AU_METERS, 6),
        "semi_major_axis_au": semi_major_axis_au,
        "body_mass_kg": body_mass_kg,
        "parent_mass_kg": parent_mass_kg,
        "equation": "r_H \\approx a(1-e) \\left(\\frac{m}{3M}\\right)^{1/3}"
    }

def calculate_roche_limit(
    primary_radius_km: float,
    primary_density_g_cm3: float,
    secondary_density_g_cm3: float
) -> Dict[str, Any]:
    """
    Computes rigid and fluid Roche limits for tidal disruption.
    """
    if primary_radius_km <= 0 or primary_density_g_cm3 <= 0 or secondary_density_g_cm3 <= 0:
        raise ValueError("Radius and densities must be strictly positive.")

    density_ratio = primary_density_g_cm3 / secondary_density_g_cm3
    rigid_km = primary_radius_km * (2.0 * density_ratio) ** (1.0 / 3.0)
    fluid_km = 2.44 * primary_radius_km * (density_ratio ** (1.0 / 3.0))

    return {
        "primary_radius_km": primary_radius_km,
        "rigid_limit_km": round(rigid_km, 1),
        "fluid_limit_km": round(fluid_km, 1),
        "rigid_roche_limit_km": round(rigid_km, 1),
        "fluid_roche_limit_km": round(fluid_km, 1),
        "rigid_equation": "d_{\\text{rigid}} = R_M (2 \\rho_M / \\rho_m)^{1/3}",
        "fluid_equation": "d_{\\text{fluid}} \\approx 2.44 R_M (\\rho_M / \\rho_m)^{1/3}"
    }

def find_orbital_resonances(
    period_days_1: float,
    period_days_2: float,
    max_order: int = 8
) -> List[Dict[str, Any]]:
    """
    Finds near-integer mean-motion orbital resonance ratios p:q between two orbital periods.
    """
    if period_days_1 <= 0 or period_days_2 <= 0:
        raise ValueError("Orbital periods must be strictly positive.")

    p1, p2 = min(period_days_1, period_days_2), max(period_days_1, period_days_2)
    ratio = p2 / p1
    resonances = []

    for q in range(1, max_order + 1):
        for p in range(q + 1, max_order * 2):
            target_ratio = p / q
            discrepancy_pct = abs(ratio - target_ratio) / target_ratio * 100.0
            if discrepancy_pct < 2.5:
                resonances.append({
                    "ratio_str": f"{p}:{q}",
                    "ratio_value": round(target_ratio, 4),
                    "measured_ratio": round(ratio, 4),
                    "discrepancy_percent": round(discrepancy_pct, 2),
                    "resonance_order": p - q,
                    "description": f"Inner body completes {p} orbits for every {q} orbits of outer body"
                })

    resonances.sort(key=lambda x: x["discrepancy_percent"])
    return resonances

def calculate_lagrange_points(
    primary_mass_kg: float,
    secondary_mass_kg: float,
    separation_au: float
) -> Dict[str, Any]:
    """
    Computes coordinates for the 5 Lagrange Equilibrium Points (L1-L5).
    """
    if primary_mass_kg <= 0 or secondary_mass_kg <= 0 or separation_au <= 0:
        raise ValueError("Masses and separation must be strictly positive.")

    d_au = separation_au
    m1 = primary_mass_kg
    m2 = secondary_mass_kg
    mu = m2 / (m1 + m2)

    r_l1 = (mu / 3.0) ** (1.0 / 3.0)
    x_l1 = (1.0 - mu) - r_l1

    r_l2 = (mu / 3.0) ** (1.0 / 3.0)
    x_l2 = (1.0 - mu) + r_l2

    r_l3 = 7.0 * mu / 12.0
    x_l3 = -1.0 + r_l3

    x_l4 = 0.5 - mu
    y_l4 = math.sqrt(3.0) / 2.0
    x_l5 = 0.5 - mu
    y_l5 = -math.sqrt(3.0) / 2.0

    return {
        "separation_au": separation_au,
        "mass_ratio_mu": mu,
        "points": {
            "L1": {"x_au": round(x_l1 * d_au, 5), "y_au": 0.0, "stability": "Unstable (Saddle point)", "description": "Between Sun and planet, ideal for solar observation (e.g. SOHO, DSCOVR)"},
            "L2": {"x_au": round(x_l2 * d_au, 5), "y_au": 0.0, "stability": "Unstable (Saddle point)", "description": "Behind planet shielded from Sun, ideal for deep-space observatories (e.g. JWST, Gaia)"},
            "L3": {"x_au": round(x_l3 * d_au, 5), "y_au": 0.0, "stability": "Unstable", "description": "Directly behind Sun opposite planet"},
            "L4": {"x_au": round(x_l4 * d_au, 5), "y_au": round(y_l4 * d_au, 5), "stability": "Stable (Coriolis trap)", "description": "Leading 60 degrees ahead of planet (Trojan asteroids)"},
            "L5": {"x_au": round(x_l5 * d_au, 5), "y_au": round(y_l5 * d_au, 5), "stability": "Stable (Coriolis trap)", "description": "Trailing 60 degrees behind planet (Greek asteroids)"}
        }
    }
