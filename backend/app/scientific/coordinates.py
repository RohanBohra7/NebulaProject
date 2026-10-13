"""
Astronomical coordinate transformations module for NEBULA.
Implements 3D Cartesian, spherical polar, ecliptic, and equatorial reference frames.
"""
import math
from typing import Dict, Any, List, Union
import numpy as np

from app.scientific.constants import EARTH_OBLIQUITY_J2000_DEG

def cartesian_to_spherical(
    x: float,
    y: float,
    z: float
) -> Dict[str, Any]:
    """
    Transforms 3D Cartesian coordinates (x, y, z) to spherical polar coordinates (r, theta, phi).
    r: radial distance >= 0
    theta: colatitude / inclination from positive Z-axis [0, pi]
    phi: azimuth in XY plane [-pi, pi]
    """
    r = math.sqrt(x**2 + y**2 + z**2)
    if r == 0.0:
        return {
            "radius": 0.0,
            "theta_rad": 0.0,
            "theta_deg": 0.0,
            "phi_rad": 0.0,
            "phi_deg": 0.0,
            "elevation_deg": 0.0
        }

    theta_rad = math.acos(max(-1.0, min(1.0, z / r)))
    phi_rad = math.atan2(y, x)

    # Elevation (latitude) above XY plane
    elevation_rad = (math.pi / 2.0) - theta_rad

    return {
        "radius": float(r),
        "theta_rad": float(theta_rad),
        "theta_deg": float(math.degrees(theta_rad)),
        "phi_rad": float(phi_rad),
        "phi_deg": float(math.degrees(phi_rad)),
        "elevation_deg": float(math.degrees(elevation_rad)),
        "cartesian_input": [float(x), float(y), float(z)]
    }

def spherical_to_cartesian(
    radius: float,
    theta_rad: float,
    phi_rad: float
) -> Dict[str, Any]:
    """
    Transforms spherical polar coordinates (r, theta, phi) to 3D Cartesian coordinates (x, y, z).
    """
    if radius < 0:
        raise ValueError("Radial distance must be non-negative (>= 0).")

    x = radius * math.sin(theta_rad) * math.cos(phi_rad)
    y = radius * math.sin(theta_rad) * math.sin(phi_rad)
    z = radius * math.cos(theta_rad)

    return {
        "x": float(x),
        "y": float(y),
        "z": float(z),
        "coordinates": [float(x), float(y), float(z)],
        "radius": float(radius),
        "theta_rad": float(theta_rad),
        "phi_rad": float(phi_rad)
    }

def ecliptic_to_equatorial(
    ecliptic_lon_deg: float,
    ecliptic_lat_deg: float,
    obliquity_deg: float = EARTH_OBLIQUITY_J2000_DEG
) -> Dict[str, Any]:
    """
    Converts heliocentric or geocentric Ecliptic coordinates (lambda, beta)
    to Equatorial coordinates (Right Ascension alpha, Declination delta)
    via standard J2000.0 Earth axial obliquity rotation.
    """
    lam_rad = math.radians(ecliptic_lon_deg)
    bet_rad = math.radians(ecliptic_lat_deg)
    eps_rad = math.radians(obliquity_deg)

    # Spherical trigonometry transformations
    sin_dec = math.sin(bet_rad) * math.cos(eps_rad) + math.cos(bet_rad) * math.sin(eps_rad) * math.sin(lam_rad)
    dec_rad = math.asin(max(-1.0, min(1.0, sin_dec)))

    y_ra = math.sin(lam_rad) * math.cos(eps_rad) - math.tan(bet_rad) * math.sin(eps_rad)
    x_ra = math.cos(lam_rad)
    ra_rad = math.atan2(y_ra, x_ra) % (2.0 * math.pi)

    ra_deg = math.degrees(ra_rad)
    dec_deg = math.degrees(dec_rad)

    # Convert RA to Hours:Minutes:Seconds
    ra_hours_float = ra_deg / 15.0
    ra_h = int(ra_hours_float)
    ra_m = int((ra_hours_float - ra_h) * 60)
    ra_s = ((ra_hours_float - ra_h) * 60 - ra_m) * 60

    return {
        "right_ascension_deg": float(ra_deg),
        "declination_deg": float(dec_deg),
        "right_ascension_hms": f"{ra_h:02d}h {ra_m:02d}m {ra_s:05.2f}s",
        "ecliptic_lon_deg": float(ecliptic_lon_deg),
        "ecliptic_lat_deg": float(ecliptic_lat_deg),
        "obliquity_deg": float(obliquity_deg)
    }

def equatorial_to_ecliptic(
    ra_deg: float,
    dec_deg: float,
    obliquity_deg: float = EARTH_OBLIQUITY_J2000_DEG
) -> Dict[str, Any]:
    """
    Converts Equatorial coordinates (Right Ascension alpha, Declination delta)
    to Ecliptic coordinates (Longitude lambda, Latitude beta).
    """
    ra_rad = math.radians(ra_deg)
    dec_rad = math.radians(dec_deg)
    eps_rad = math.radians(obliquity_deg)

    sin_beta = math.sin(dec_rad) * math.cos(eps_rad) - math.cos(dec_rad) * math.sin(eps_rad) * math.sin(ra_rad)
    beta_rad = math.asin(max(-1.0, min(1.0, sin_beta)))

    y_lam = math.sin(ra_rad) * math.cos(eps_rad) + math.tan(dec_rad) * math.sin(eps_rad)
    x_lam = math.cos(ra_rad)
    lam_rad = math.atan2(y_lam, x_lam) % (2.0 * math.pi)

    return {
        "ecliptic_lon_deg": float(math.degrees(lam_rad)),
        "ecliptic_lat_deg": float(math.degrees(beta_rad)),
        "right_ascension_deg": float(ra_deg),
        "declination_deg": float(dec_deg),
        "obliquity_deg": float(obliquity_deg)
    }
