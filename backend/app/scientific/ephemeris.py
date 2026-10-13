"""
High-fidelity orbital path and ephemerides generator for NEBULA 3D visualization.
Generates smooth 3D Keplerian ellipses and trajectory points in astronomical units.
"""
import math
from typing import List, Dict, Any
from app.scientific.orbital import orbital_elements_to_cartesian
from app.scientific.constants import AU_METERS, M_SUN

def generate_orbit_path_points(
    semi_major_axis_au: float,
    eccentricity: float,
    inclination_deg: float,
    ascending_node_deg: float = 0.0,
    arg_periapsis_deg: float = 0.0,
    num_samples: int = 120
) -> List[List[float]]:
    """
    Generates a closed 3D polygonal orbit path (array of [x, y, z] points in AU)
    for rendering in Three.js Line or Tube geometries.
    """
    if semi_major_axis_au <= 0.0:
        return [[0.0, 0.0, 0.0]]

    points = []
    # Sample true anomaly from 0 to 360 degrees
    for step in range(num_samples + 1):
        nu_deg = (step / num_samples) * 360.0
        coords = orbital_elements_to_cartesian(
            semi_major_axis_au=semi_major_axis_au,
            eccentricity=eccentricity,
            inclination_deg=inclination_deg,
            ascending_node_deg=ascending_node_deg,
            arg_periapsis_deg=arg_periapsis_deg,
            true_anomaly_deg=nu_deg
        )
        pos = coords["position_au"]
        points.append([round(pos[0], 5), round(pos[1], 5), round(pos[2], 5)])

    return points

def propagate_ephemeris(
    semi_major_axis_au: float,
    eccentricity: float,
    orbital_period_days: float,
    inclination_deg: float = 0.0,
    elapsed_time_days: float = 0.0
) -> Dict[str, Any]:
    """
    Computes body position at a specific elapsed time t (days) since epoch.
    """
    if orbital_period_days <= 0.0:
        return {"position_au": [0.0, 0.0, 0.0], "velocity_km_s": [0.0, 0.0, 0.0]}

    mean_motion_deg_per_day = 360.0 / orbital_period_days
    current_mean_anomaly_deg = (elapsed_time_days * mean_motion_deg_per_day) % 360.0
    
    return orbital_elements_to_cartesian(
        semi_major_axis_au=semi_major_axis_au,
        eccentricity=eccentricity,
        inclination_deg=inclination_deg,
        ascending_node_deg=0.0,
        arg_periapsis_deg=0.0,
        true_anomaly_deg=current_mean_anomaly_deg
    )
