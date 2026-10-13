"""
Astrophysical distance metrics and light propagation computation for NEBULA.
Implements spatial distances, light travel time, angular sizes, distance moduli, and apsidal extrema.
"""
import math
from typing import Dict, Any, List, Union
import numpy as np

from app.scientific.constants import (
    SPEED_OF_LIGHT,
    AU_METERS,
    PC_METERS,
    LY_METERS,
    DAY_SECONDS,
    JULIAN_YEAR_SECONDS
)

def calculate_euclidean_distance(
    pos1: Union[List[float], np.ndarray],
    pos2: Union[List[float], np.ndarray],
    input_unit: str = "au"
) -> Dict[str, Any]:
    """
    Computes Euclidean 3D spatial separation between two points in space.

    :param pos1: [x, y, z] coordinates of object 1
    :param pos2: [x, y, z] coordinates of object 2
    :param input_unit: Coordinate units ('m', 'km', 'au', 'pc', 'ly')
    """
    p1 = np.asarray(pos1, dtype=float)
    p2 = np.asarray(pos2, dtype=float)

    if p1.shape != (3,) or p2.shape != (3,):
        raise ValueError("Positions must be 3-dimensional Cartesian coordinates [x, y, z].")

    diff = p2 - p1
    raw_dist = float(np.linalg.norm(diff))

    # Convert to meters first
    unit_lower = input_unit.lower()
    if unit_lower == "m":
        dist_m = raw_dist
    elif unit_lower == "km":
        dist_m = raw_dist * 1000.0
    elif unit_lower == "au":
        dist_m = raw_dist * AU_METERS
    elif unit_lower == "pc":
        dist_m = raw_dist * PC_METERS
    elif unit_lower in ("ly", "lyr"):
        dist_m = raw_dist * LY_METERS
    else:
        raise ValueError(f"Unsupported distance unit: {input_unit}. Allowed: 'm', 'km', 'au', 'pc', 'ly'.")

    return {
        "distance_meters": float(dist_m),
        "distance_km": float(dist_m / 1000.0),
        "distance_au": float(dist_m / AU_METERS),
        "distance_light_years": float(dist_m / LY_METERS),
        "distance_parsecs": float(dist_m / PC_METERS),
        "delta_vector": [float(diff[0]), float(diff[1]), float(diff[2])],
        "input_unit": input_unit
    }

def calculate_light_travel_time(distance_m: float) -> Dict[str, Any]:
    """
    Computes time required for electromagnetic radiation (light) to traverse a given distance in vacuum.
    Formula: t = d / c

    :param distance_m: Distance in meters (> 0)
    """
    if distance_m <= 0:
        raise ValueError("Distance must be strictly positive (> 0 m).")

    time_sec = distance_m / SPEED_OF_LIGHT
    time_min = time_sec / 60.0
    time_hr = time_sec / 3600.0
    time_days = time_sec / DAY_SECONDS
    time_years = time_sec / JULIAN_YEAR_SECONDS

    return {
        "light_time_seconds": float(time_sec),
        "light_time_minutes": float(time_min),
        "light_time_hours": float(time_hr),
        "light_time_days": float(time_days),
        "light_time_years": float(time_years),
        "distance_meters": float(distance_m),
        "distance_au": float(distance_m / AU_METERS),
        "speed_of_light_m_s": SPEED_OF_LIGHT,
        "formula": "t = d / c"
    }

def calculate_angular_diameter(
    physical_diameter_m: float,
    distance_m: float
) -> Dict[str, Any]:
    """
    Computes apparent angular diameter of an astronomical object viewed from a given distance.
    Formula: theta = 2 * arctan(D / (2 * d))

    :param physical_diameter_m: Physical diameter of body in meters (> 0)
    :param distance_m: Observer distance in meters (> 0)
    """
    if physical_diameter_m <= 0:
        raise ValueError("Physical diameter must be strictly positive (> 0 m).")
    if distance_m <= 0:
        raise ValueError("Observer distance must be strictly positive (> 0 m).")

    theta_rad = 2.0 * math.atan(physical_diameter_m / (2.0 * distance_m))
    theta_deg = math.degrees(theta_rad)
    theta_arcmin = theta_deg * 60.0
    theta_arcsec = theta_deg * 3600.0

    return {
        "angular_diameter_rad": float(theta_rad),
        "angular_diameter_deg": float(theta_deg),
        "angular_diameter_arcmin": float(theta_arcmin),
        "angular_diameter_arcsec": float(theta_arcsec),
        "physical_diameter_m": float(physical_diameter_m),
        "distance_m": float(distance_m),
        "formula": "theta = 2 * arctan(D / (2d))"
    }

def calculate_distance_modulus(distance_pc: float) -> Dict[str, Any]:
    """
    Computes photometric distance modulus mu = m - M for an object at a given distance in parsecs.
    Formula: mu = 5 * log10(d_pc) - 5

    :param distance_pc: Distance in parsecs (> 0)
    """
    if distance_pc <= 0:
        raise ValueError("Distance must be strictly positive (> 0 pc).")

    mu = 5.0 * math.log10(distance_pc) - 5.0

    return {
        "distance_modulus_mag": float(mu),
        "distance_pc": float(distance_pc),
        "distance_ly": float(distance_pc * (PC_METERS / LY_METERS)),
        "formula": "mu = 5 * log10(d_pc) - 5"
    }

def calculate_distance_from_modulus(distance_modulus: float) -> Dict[str, Any]:
    """
    Inverts distance modulus mu = m - M to determine physical distance in parsecs.
    Formula: d_pc = 10^((mu + 5) / 5)
    """
    d_pc = 10.0 ** ((distance_modulus + 5.0) / 5.0)

    return {
        "distance_modulus": float(distance_modulus),
        "distance_pc": float(d_pc),
        "distance_ly": float(d_pc * (PC_METERS / LY_METERS)),
        "distance_meters": float(d_pc * PC_METERS),
        "formula": "d_pc = 10^((mu + 5) / 5)"
    }

def calculate_apsidal_distances(
    semi_major_axis_au: float,
    eccentricity: float
) -> Dict[str, Any]:
    """
    Computes periapsis and apoapsis distances for an eccentric Keplerian orbit.
    Formula: r_peri = a * (1 - e), r_apo = a * (1 + e)
    """
    if semi_major_axis_au <= 0:
        raise ValueError("Semi-major axis must be strictly positive (> 0 AU).")
    if eccentricity < 0 or eccentricity >= 1.0:
        raise ValueError("Eccentricity for bound orbits must be in the range [0, 1).")

    r_peri_au = semi_major_axis_au * (1.0 - eccentricity)
    r_apo_au = semi_major_axis_au * (1.0 + eccentricity)

    return {
        "periapsis_au": float(r_peri_au),
        "periapsis_km": float(r_peri_au * (AU_METERS / 1000.0)),
        "apoapsis_au": float(r_apo_au),
        "apoapsis_km": float(r_apo_au * (AU_METERS / 1000.0)),
        "semi_major_axis_au": float(semi_major_axis_au),
        "eccentricity": float(eccentricity),
        "difference_au": float(r_apo_au - r_peri_au)
    }
