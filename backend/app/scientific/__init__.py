"""
NEBULA Scientific Computation Engine.
Unified export interface for astrophysical constants, gravitational physics,
Keplerian dynamics, distance metrics, coordinate frames, and Astropy unit tools.
"""
from app.scientific.constants import (
    G_CONST,
    G,
    SPEED_OF_LIGHT,
    C_CONST,
    M_SUN,
    M_EARTH,
    M_JUPITER,
    M_MOON,
    R_SUN,
    R_EARTH,
    R_EARTH_MEAN,
    R_JUPITER,
    R_MOON,
    AU_METERS,
    PC_METERS,
    LY_METERS,
    DAY_SECONDS,
    JULIAN_YEAR_DAYS,
    JULIAN_YEAR_SECONDS,
    G_EARTH_SURFACE,
    L_SUN,
    STEFAN_BOLTZMANN,
    EARTH_OBLIQUITY_J2000_DEG
)

from app.scientific.gravity import (
    calculate_gravitational_force,
    calculate_gravitational_force_vector,
    calculate_surface_gravity,
    calculate_gravitational_potential,
    calculate_tidal_acceleration
)

from app.scientific.orbital import (
    calculate_circular_velocity,
    calculate_vis_viva_velocity,
    calculate_escape_velocity,
    calculate_apsidal_velocities,
    calculate_orbital_period,
    calculate_synodic_period,
    calculate_orbital_parameters,
    solve_kepler,
    eccentric_to_true_anomaly,
    orbital_elements_to_cartesian,
    calculate_hohmann_transfer,
    calculate_hill_sphere,
    calculate_roche_limit,
    find_orbital_resonances,
    calculate_lagrange_points
)

from app.scientific.distances import (
    calculate_euclidean_distance,
    calculate_light_travel_time,
    calculate_angular_diameter,
    calculate_distance_modulus,
    calculate_distance_from_modulus,
    calculate_apsidal_distances
)

from app.scientific.coordinates import (
    cartesian_to_spherical,
    spherical_to_cartesian,
    ecliptic_to_equatorial,
    equatorial_to_ecliptic
)

from app.scientific.units import (
    convert_units,
    resolve_unit_string,
    get_supported_categories
)

from app.scientific.astropy_bridge import (
    compute_astropy_units,
    find_related_objects
)

from app.scientific.ephemeris import (
    generate_orbit_path_points,
    propagate_ephemeris
)

__all__ = [
    # Constants
    "G_CONST",
    "G",
    "SPEED_OF_LIGHT",
    "C_CONST",
    "M_SUN",
    "M_EARTH",
    "M_JUPITER",
    "M_MOON",
    "R_SUN",
    "R_EARTH",
    "R_EARTH_MEAN",
    "R_JUPITER",
    "R_MOON",
    "AU_METERS",
    "PC_METERS",
    "LY_METERS",
    "DAY_SECONDS",
    "JULIAN_YEAR_DAYS",
    "JULIAN_YEAR_SECONDS",
    "G_EARTH_SURFACE",
    "L_SUN",
    "STEFAN_BOLTZMANN",
    "EARTH_OBLIQUITY_J2000_DEG",

    # Gravity
    "calculate_gravitational_force",
    "calculate_gravitational_force_vector",
    "calculate_surface_gravity",
    "calculate_gravitational_potential",
    "calculate_tidal_acceleration",

    # Orbital
    "calculate_circular_velocity",
    "calculate_vis_viva_velocity",
    "calculate_escape_velocity",
    "calculate_apsidal_velocities",
    "calculate_orbital_period",
    "calculate_synodic_period",
    "calculate_orbital_parameters",
    "solve_kepler",
    "eccentric_to_true_anomaly",
    "orbital_elements_to_cartesian",
    "calculate_hohmann_transfer",
    "calculate_hill_sphere",
    "calculate_roche_limit",
    "find_orbital_resonances",
    "calculate_lagrange_points",

    # Distances
    "calculate_euclidean_distance",
    "calculate_light_travel_time",
    "calculate_angular_diameter",
    "calculate_distance_modulus",
    "calculate_distance_from_modulus",
    "calculate_apsidal_distances",

    # Coordinates
    "cartesian_to_spherical",
    "spherical_to_cartesian",
    "ecliptic_to_equatorial",
    "equatorial_to_ecliptic",

    # Units
    "convert_units",
    "resolve_unit_string",
    "get_supported_categories",

    # Astropy bridge & ephemeris
    "compute_astropy_units",
    "find_related_objects",
    "generate_orbit_path_points",
    "propagate_ephemeris",
]
