"""
Backward compatibility layer for app.computation.orbital_mechanics.
Forwards to app.scientific.orbital and app.scientific.constants.
"""
from app.scientific.constants import (
    G_CONST,
    G,
    M_SUN,
    M_EARTH,
    R_SUN,
    R_EARTH,
    AU_METERS,
    DAY_SECONDS,
    SPEED_OF_LIGHT
)
from app.scientific.orbital import (
    solve_kepler,
    eccentric_to_true_anomaly,
    orbital_elements_to_cartesian,
    calculate_hohmann_transfer,
    calculate_hill_sphere,
    calculate_roche_limit,
    find_orbital_resonances,
    calculate_lagrange_points
)

__all__ = [
    "G_CONST",
    "G",
    "M_SUN",
    "M_EARTH",
    "R_SUN",
    "R_EARTH",
    "AU_METERS",
    "DAY_SECONDS",
    "SPEED_OF_LIGHT",
    "solve_kepler",
    "eccentric_to_true_anomaly",
    "orbital_elements_to_cartesian",
    "calculate_hohmann_transfer",
    "calculate_hill_sphere",
    "calculate_roche_limit",
    "find_orbital_resonances",
    "calculate_lagrange_points"
]
