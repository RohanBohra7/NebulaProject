"""
Gravitational physics computation module for NEBULA.
Implements Newtonian universal gravitation, gravitational fields, potentials, and tidal accelerations.
"""
import math
from typing import Dict, Any, List, Union
import numpy as np
import astropy.units as u

from app.scientific.constants import G_CONST, G_EARTH_SURFACE

def calculate_gravitational_force(
    m1_kg: float,
    m2_kg: float,
    distance_m: float
) -> Dict[str, Any]:
    """
    Computes Newtonian gravitational attraction force between two point masses.
    Formula: F = G * (m1 * m2) / r^2

    :param m1_kg: Mass of first body in kilograms (> 0)
    :param m2_kg: Mass of second body in kilograms (> 0)
    :param distance_m: Center-to-center distance in meters (> 0)
    :return: Force in Newtons, kilonewtons, dynes, and input metadata.
    """
    if m1_kg <= 0 or m2_kg <= 0:
        raise ValueError("Masses must be strictly positive (> 0 kg).")
    if distance_m <= 0:
        raise ValueError("Distance between bodies must be strictly positive (> 0 m).")

    # Astropy Quantity verification
    m1_q = m1_kg * u.kg
    m2_q = m2_kg * u.kg
    r_q = distance_m * u.m

    force_n = G_CONST * (m1_kg * m2_kg) / (distance_m ** 2)
    force_kn = force_n / 1000.0
    force_dyn = force_n * 1e5

    return {
        "force_newtons": float(force_n),
        "force_kilonewtons": float(force_kn),
        "force_dynes": float(force_dyn),
        "m1_kg": float(m1_kg),
        "m2_kg": float(m2_kg),
        "distance_m": float(distance_m),
        "formula": "F = G * (m1 * m2) / r^2",
        "units": "N (kg m s^-2)"
    }

def calculate_gravitational_force_vector(
    m1_kg: float,
    m2_kg: float,
    pos1_m: Union[List[float], np.ndarray],
    pos2_m: Union[List[float], np.ndarray]
) -> Dict[str, Any]:
    """
    Computes the 3D gravitational force vector exerted on body 1 by body 2.
    Formula: F_vec = G * m1 * m2 * (pos2 - pos1) / ||pos2 - pos1||^3

    :param m1_kg: Mass of body 1 in kg
    :param m2_kg: Mass of body 2 in kg
    :param pos1_m: [x, y, z] coordinate of body 1 in meters
    :param pos2_m: [x, y, z] coordinate of body 2 in meters
    """
    if m1_kg <= 0 or m2_kg <= 0:
        raise ValueError("Masses must be strictly positive (> 0 kg).")

    p1 = np.asarray(pos1_m, dtype=float)
    p2 = np.asarray(pos2_m, dtype=float)

    if p1.shape != (3,) or p2.shape != (3,):
        raise ValueError("Positions must be 3-dimensional Cartesian coordinates [x, y, z].")

    r_vec = p2 - p1
    dist = float(np.linalg.norm(r_vec))

    if dist == 0.0:
        raise ValueError("Distance between bodies cannot be zero.")

    f_mag = G_CONST * (m1_kg * m2_kg) / (dist ** 2)
    f_vec = (G_CONST * m1_kg * m2_kg / (dist ** 3)) * r_vec

    return {
        "force_magnitude_n": f_mag,
        "force_vector_n": [float(f_vec[0]), float(f_vec[1]), float(f_vec[2])],
        "relative_vector_m": [float(r_vec[0]), float(r_vec[1]), float(r_vec[2])],
        "distance_m": dist,
        "formula": "F_12 = G * m1 * m2 * (r2 - r1) / ||r2 - r1||^3"
    }

def calculate_surface_gravity(
    mass_kg: float,
    radius_m: float
) -> Dict[str, Any]:
    """
    Computes local gravitational acceleration at the surface of a spherical body.
    Formula: g = G * M / R^2

    :param mass_kg: Body mass in kg (> 0)
    :param radius_m: Mean body radius in meters (> 0)
    :return: Acceleration in m/s^2 and relative Earth gees.
    """
    if mass_kg <= 0:
        raise ValueError("Body mass must be strictly positive (> 0 kg).")
    if radius_m <= 0:
        raise ValueError("Body radius must be strictly positive (> 0 m).")

    g_m_s2 = G_CONST * mass_kg / (radius_m ** 2)
    g_earth_ratio = g_m_s2 / G_EARTH_SURFACE

    return {
        "gravity_m_s2": float(g_m_s2),
        "gravity_earth_gees": float(g_earth_ratio),
        "mass_kg": float(mass_kg),
        "radius_m": float(radius_m),
        "formula": "g = G * M / R^2",
        "reference_standard_g": G_EARTH_SURFACE
    }

def calculate_gravitational_potential(
    mass_kg: float,
    distance_m: float,
    secondary_mass_kg: float = None
) -> Dict[str, Any]:
    """
    Computes gravitational potential Phi(r) and potential energy U(r).
    Formula: Phi = -G * M / r
    Formula: U = -G * M * m / r

    :param mass_kg: Primary mass in kg (> 0)
    :param distance_m: Radial distance in meters (> 0)
    :param secondary_mass_kg: Optional secondary mass in kg for potential energy U
    """
    if mass_kg <= 0:
        raise ValueError("Mass must be strictly positive (> 0 kg).")
    if distance_m <= 0:
        raise ValueError("Distance must be strictly positive (> 0 m).")

    potential_j_kg = -G_CONST * mass_kg / distance_m
    potential_energy_j = None

    if secondary_mass_kg is not None:
        if secondary_mass_kg <= 0:
            raise ValueError("Secondary mass must be strictly positive (> 0 kg).")
        potential_energy_j = -G_CONST * mass_kg * secondary_mass_kg / distance_m

    return {
        "potential_j_kg": float(potential_j_kg),
        "potential_energy_joules": float(potential_energy_j) if potential_energy_j is not None else None,
        "mass_kg": float(mass_kg),
        "distance_m": float(distance_m),
        "potential_formula": "Phi(r) = -G * M / r",
        "energy_formula": "U(r) = -G * M * m / r"
    }

def calculate_tidal_acceleration(
    primary_mass_kg: float,
    body_radius_m: float,
    distance_m: float
) -> Dict[str, Any]:
    """
    Computes differential tidal acceleration across a secondary body's diameter.
    Formula: a_tidal approx 2 * G * M_primary * R_secondary / r^3

    :param primary_mass_kg: Mass of tide-raising primary body (kg)
    :param body_radius_m: Radius of affected secondary body (m)
    :param distance_m: Orbital separation between centers (m)
    """
    if primary_mass_kg <= 0 or body_radius_m <= 0 or distance_m <= 0:
        raise ValueError("All parameters must be strictly positive (> 0).")

    a_tidal = (2.0 * G_CONST * primary_mass_kg * body_radius_m) / (distance_m ** 3)

    return {
        "tidal_acceleration_m_s2": float(a_tidal),
        "primary_mass_kg": float(primary_mass_kg),
        "body_radius_m": float(body_radius_m),
        "distance_m": float(distance_m),
        "formula": "a_tidal = 2 * G * M * R / r^3"
    }
