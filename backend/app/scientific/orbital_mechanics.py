"""
Scientific orbital mechanics and astrophysical calculations engine for NEBULA.
Uses standard physical constants and Keplerian/Newtonian formulations.
"""
import math
from typing import Dict, Any, List, Tuple, Optional
import numpy as np

# Fundamental Astronomical Constants (SI Units)
G = 6.67430e-11           # Gravitational constant (m^3 kg^-1 s^-2)
G_CONST = G
M_SUN = 1.98847e30        # Solar mass (kg)
M_EARTH = 5.9722e24       # Earth mass (kg)
R_SUN = 6.9634e8          # Solar radius (m)
R_EARTH = 6.371e6         # Earth radius (m)
AU_METERS = 1.495978707e11 # 1 Astronomical Unit (m)
DAY_SECONDS = 86400.0     # Seconds in a day
SPEED_OF_LIGHT = 299792458.0 # m/s

def solve_kepler(mean_anomaly_rad: float, eccentricity: float, tolerance: float = 1e-12, max_iter: int = 100) -> float:
    """
    Solves Kepler's Equation M = E - e*sin(E) for Eccentric Anomaly E using Newton-Raphson iteration.
    """
    if eccentricity == 0.0:
        return mean_anomaly_rad
    
    # Initial guess
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
        # Parabolic/hyperbolic edge case
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

    mu = G * central_mass_kg
    p_m = a_m * (1.0 - e**2) if e < 1.0 else a_m

    # Orbital radius
    r_m = p_m / (1.0 + e * math.cos(nu_rad)) if (1.0 + e * math.cos(nu_rad)) > 0 else a_m

    # Perifocal coordinates (r in orbital plane)
    x_peri = r_m * math.cos(nu_rad)
    y_peri = r_m * math.sin(nu_rad)
    z_peri = 0.0

    # Perifocal velocity
    h = math.sqrt(mu * p_m) if p_m > 0 else 0.0
    vx_peri = -(mu / h) * math.sin(nu_rad) if h > 0 else 0.0
    vy_peri = (mu / h) * (e + math.cos(nu_rad)) if h > 0 else 0.0
    vz_peri = 0.0

    # Rotation matrix from perifocal to heliocentric ecliptic
    cos_w = math.cos(w_rad)
    sin_w = math.sin(w_rad)
    cos_o = math.cos(omega_rad)
    sin_o = math.sin(omega_rad)
    cos_i = math.cos(i_rad)
    sin_i = math.sin(i_rad)

    # Combined transformation elements
    px = cos_o * cos_w - sin_o * sin_w * cos_i
    py = sin_o * cos_w + cos_o * sin_w * cos_i
    pz = sin_w * sin_i

    qx = -cos_o * sin_w - sin_o * cos_w * cos_i
    qy = -sin_o * sin_w + cos_o * cos_w * cos_i
    qz = cos_w * sin_i

    # Position in meters
    x_m = x_peri * px + y_peri * qx
    y_m = x_peri * py + y_peri * qy
    z_m = x_peri * pz + y_peri * qz

    # Velocity in m/s
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
    Returns delta-v burns (km/s), transfer time (days), and transfer ellipse parameters.
    """
    r1 = r1_au * AU_METERS
    r2 = r2_au * AU_METERS
    mu = G * central_mass_kg

    # Semi-major axis of the transfer ellipse
    a_transfer = (r1 + r2) / 2.0
    
    # Velocity at circular orbits
    v1_circ = math.sqrt(mu / r1)
    v2_circ = math.sqrt(mu / r2)

    # Velocity on transfer ellipse at r1 and r2
    v1_trans = math.sqrt(mu * (2.0 / r1 - 1.0 / a_transfer))
    v2_trans = math.sqrt(mu * (2.0 / r2 - 1.0 / a_transfer))

    # Impulses
    delta_v1 = abs(v1_trans - v1_circ)
    delta_v2 = abs(v2_circ - v2_trans)
    total_delta_v = delta_v1 + delta_v2

    # Half-period of transfer ellipse
    transfer_time_sec = math.pi * math.sqrt((a_transfer**3) / mu)
    transfer_time_days = transfer_time_sec / DAY_SECONDS

    # Eccentricity of transfer orbit
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
    Computes Hill Sphere radius where the body's gravity dominates over the primary's tidal forces.
    Formula: r_H approx a * (1 - e) * (m / (3 * M))^(1/3)
    """
    if parent_mass_kg <= 0 or body_mass_kg <= 0 or semi_major_axis_au <= 0:
        return {"hill_radius_km": 0.0, "hill_radius_au": 0.0}

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
    if primary_density_g_cm3 <= 0 or secondary_density_g_cm3 <= 0:
        return {"rigid_limit_km": 0.0, "fluid_limit_km": 0.0}

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

def find_orbital_resonances(period_days_1: float, period_days_2: float, max_order: int = 8) -> List[Dict[str, Any]]:
    """
    Finds near-integer mean-motion orbital resonance ratios p:q between two orbital periods.
    """
    if period_days_1 <= 0 or period_days_2 <= 0:
        return []

    p1, p2 = min(period_days_1, period_days_2), max(period_days_1, period_days_2)
    ratio = p2 / p1
    resonances = []

    for q in range(1, max_order + 1):
        for p in range(q + 1, max_order * 2):
            target_ratio = p / q
            discrepancy_pct = abs(ratio - target_ratio) / target_ratio * 100.0
            if discrepancy_pct < 2.5: # Near resonance within 2.5%
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
    Computes coordinates for the 5 Lagrange Equilibrium Points (L1-L5)
    in the normalized rotating co-ordinate frame and physical AU units.
    """
    d_au = separation_au
    m1 = primary_mass_kg
    m2 = secondary_mass_kg
    mu = m2 / (m1 + m2) # Mass ratio

    # Normalized distance to barycenter: Primary at (-mu, 0), Secondary at (1-mu, 0)
    # L1: between primary and secondary
    r_l1 = (mu / 3.0) ** (1.0 / 3.0)
    x_l1 = (1.0 - mu) - r_l1

    # L2: beyond secondary
    r_l2 = (mu / 3.0) ** (1.0 / 3.0)
    x_l2 = (1.0 - mu) + r_l2

    # L3: opposite primary
    r_l3 = 7.0 * mu / 12.0
    x_l3 = -1.0 + r_l3

    # L4 and L5: equilateral triangles at (0.5 - mu, +/- sqrt(3)/2)
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
