"""
Backward compatibility layer for app.computation.ephemeris.
Forwards to app.scientific.ephemeris.
"""
from app.scientific.ephemeris import (
    generate_orbit_path_points,
    propagate_ephemeris
)

__all__ = [
    "generate_orbit_path_points",
    "propagate_ephemeris"
]
