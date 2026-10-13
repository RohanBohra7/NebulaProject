"""
Pre-configured scientific simulation scenarios for NEBULA.
Normalized in astronomical units:
  - Distance: Astronomical Units (AU)
  - Mass: Solar Masses (M_sun)
  - Time: Years (yr) or Days (d)
  - Velocity: AU/year (where circular speed at 1 AU is 2*pi ~ 6.283185 AU/yr)
  - Gravitational Constant: G = 4 * pi^2 ~ 39.4784176 AU^3 / (M_sun * yr^2)
  - For normalized dimensionless systems (e.g. Figure-8 Choreography), G = 1.0
"""
import math
from typing import Dict, Any, List, Optional

# G in units of AU^3 / (M_sun * year^2)
G_AU_MSUN_YEAR = 4.0 * (math.pi ** 2)  # ~39.47841760435743

SCENARIOS: Dict[str, Dict[str, Any]] = {
    "sun_earth": {
        "id": "sun_earth",
        "name": "Sun - Earth (Two-Body Keplerian Orbit)",
        "description": "Fundamental two-body gravitational interaction demonstrating circular/elliptical Keplerian orbit, angular momentum conservation, and orbital period of exactly 1.000 year.",
        "mode_focus": "Citizen / Student / Researcher",
        "default_time_years": 1.0,
        "default_dt_days": 1.0,
        "recommended_integrator": "whfast",
        "assumptions": [
            "Point-mass Newtonian universal gravitation.",
            "Isolated two-body system with zero external perturbations.",
            "Non-relativistic dynamics (Schwarzschild precession omitted).",
            "Initial velocity matches circular Keplerian velocity v = 2*pi AU/yr."
        ],
        "units": {
            "distance": "AU",
            "mass": "M_sun",
            "time": "years",
            "velocity": "AU/year"
        },
        "bodies": [
            {
                "id": "sun",
                "name": "Sun",
                "mass": 1.0,
                "radius_km": 696340.0,
                "radius_display": 1.6,
                "color": "#f59e0b",
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "vx": 0.0,
                "vy": 0.0,
                "vz": 0.0
            },
            {
                "id": "earth",
                "name": "Earth",
                "mass": 3.003489e-6,
                "radius_km": 6371.0,
                "radius_display": 0.9,
                "color": "#38bdf8",
                "x": 1.0,
                "y": 0.0,
                "z": 0.0,
                "vx": 0.0,
                "vy": 6.2831853,
                "vz": 0.0
            }
        ]
    },
    "earth_moon_sun": {
        "id": "earth_moon_sun",
        "name": "Sun - Earth - Moon (Hierarchical Three-Body System)",
        "description": "Hierarchical 3-body system demonstrating the Moon orbiting Earth while being perturbed by solar tidal gravitation, showing non-Keplerian orbital precession.",
        "mode_focus": "Student / Researcher",
        "default_time_years": 0.25,  # ~3 months (approx 3.3 lunar synodic orbits)
        "default_dt_days": 0.05,
        "recommended_integrator": "ias15",
        "assumptions": [
            "Hierarchical point-mass Newtonian gravity.",
            "Solar tidal field acts perturbatively on lunar geocentric orbit.",
            "No tidal dissipation or physical oblateness (J2 = 0).",
            "Adaptive IAS15 recommended due to high frequency ratio between Earth and Moon orbits (~13:1)."
        ],
        "units": {
            "distance": "AU",
            "mass": "M_sun",
            "time": "years",
            "velocity": "AU/year"
        },
        "bodies": [
            {
                "id": "sun",
                "name": "Sun",
                "mass": 1.0,
                "radius_km": 696340.0,
                "radius_display": 1.6,
                "color": "#f59e0b",
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "vx": 0.0,
                "vy": 0.0,
                "vz": 0.0
            },
            {
                "id": "earth",
                "name": "Earth",
                "mass": 3.003489e-6,
                "radius_km": 6371.0,
                "radius_display": 0.9,
                "color": "#38bdf8",
                "x": 1.0,
                "y": 0.0,
                "z": 0.0,
                "vx": 0.0,
                "vy": 6.2831853,
                "vz": 0.0
            },
            {
                "id": "moon",
                "name": "Moon",
                "mass": 3.6939e-8,
                "radius_km": 1737.4,
                "radius_display": 0.5,
                "color": "#cbd5e1",
                # Distance from Earth: 384,400 km ~ 0.00257 AU
                # Lunar circular orbital speed around Earth: ~1.022 km/s ~ 0.2156 AU/yr
                "x": 1.00257,
                "y": 0.0,
                "z": 0.0,
                "vx": 0.0,
                "vy": 6.4988,
                "vz": 0.0
            }
        ]
    },
    "solar_system_inner": {
        "id": "solar_system_inner",
        "name": "Inner Solar System (Sun + 4 Terrestrial Planets)",
        "description": "Multi-planet gravitational system showing the Sun and the four terrestrial worlds (Mercury, Venus, Earth, Mars) interacting gravitationally.",
        "mode_focus": "All Modes",
        "default_time_years": 2.0,
        "default_dt_days": 1.0,
        "recommended_integrator": "whfast",
        "assumptions": [
            "Point-mass Newtonian mechanics.",
            "Coplanar approximations with real semi-major axes and Keplerian orbital speeds.",
            "Planet-planet mutual gravitational perturbations included.",
            "Symplectic WHFast integrator recommended for long-term Keplerian phase-space volume preservation."
        ],
        "units": {
            "distance": "AU",
            "mass": "M_sun",
            "time": "years",
            "velocity": "AU/year"
        },
        "bodies": [
            {"id": "sun", "name": "Sun", "mass": 1.0, "radius_km": 696340.0, "radius_display": 1.5, "color": "#f59e0b", "x": 0.0, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 0.0, "vz": 0.0},
            {"id": "mercury", "name": "Mercury", "mass": 1.66e-7, "radius_km": 2439.7, "radius_display": 0.6, "color": "#9ca3af", "x": 0.387, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 10.08, "vz": 0.0},
            {"id": "venus", "name": "Venus", "mass": 2.45e-6, "radius_km": 6051.8, "radius_display": 0.8, "color": "#eab308", "x": 0.723, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 7.39, "vz": 0.0},
            {"id": "earth", "name": "Earth", "mass": 3.00e-6, "radius_km": 6371.0, "radius_display": 0.9, "color": "#38bdf8", "x": 1.000, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 6.283, "vz": 0.0},
            {"id": "mars", "name": "Mars", "mass": 3.23e-7, "radius_km": 3389.5, "radius_display": 0.7, "color": "#ef4444", "x": 1.524, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 5.09, "vz": 0.0}
        ]
    },
    "solar_system_full": {
        "id": "solar_system_full",
        "name": "Full Solar System (Sun + 8 Major Planets)",
        "description": "Complete 9-body simulation of the Sun and all 8 major planets from Mercury to Neptune, demonstrating gas giant perturbations and secular resonance.",
        "mode_focus": "Researcher / Student",
        "default_time_years": 12.0,  # ~1 Jupiter orbit
        "default_dt_days": 5.0,
        "recommended_integrator": "whfast",
        "assumptions": [
            "Point-mass Newtonian mechanics.",
            "Heliocentric Keplerian initial conditions across all 8 major planets.",
            "Jupiter and Saturn dominate non-central perturbations.",
            "Preserves phase-space volume via symplectic Wisdom-Holman mapping."
        ],
        "units": {
            "distance": "AU",
            "mass": "M_sun",
            "time": "years",
            "velocity": "AU/year"
        },
        "bodies": [
            {"id": "sun", "name": "Sun", "mass": 1.0, "radius_km": 696340.0, "radius_display": 1.6, "color": "#f59e0b", "x": 0.0, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 0.0, "vz": 0.0},
            {"id": "mercury", "name": "Mercury", "mass": 1.66e-7, "radius_km": 2439.7, "radius_display": 0.5, "color": "#9ca3af", "x": 0.387, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 10.08, "vz": 0.0},
            {"id": "venus", "name": "Venus", "mass": 2.45e-6, "radius_km": 6051.8, "radius_display": 0.7, "color": "#eab308", "x": 0.723, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 7.39, "vz": 0.0},
            {"id": "earth", "name": "Earth", "mass": 3.00e-6, "radius_km": 6371.0, "radius_display": 0.8, "color": "#38bdf8", "x": 1.000, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 6.283, "vz": 0.0},
            {"id": "mars", "name": "Mars", "mass": 3.23e-7, "radius_km": 3389.5, "radius_display": 0.6, "color": "#ef4444", "x": 1.524, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 5.09, "vz": 0.0},
            {"id": "jupiter", "name": "Jupiter", "mass": 9.548e-4, "radius_km": 69911.0, "radius_display": 1.3, "color": "#d97706", "x": 5.204, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 2.754, "vz": 0.0},
            {"id": "saturn", "name": "Saturn", "mass": 2.858e-4, "radius_km": 58232.0, "radius_display": 1.1, "color": "#fde047", "x": 9.582, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 2.030, "vz": 0.0},
            {"id": "uranus", "name": "Uranus", "mass": 4.366e-5, "radius_km": 25362.0, "radius_display": 0.9, "color": "#22d3ee", "x": 19.20, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 1.433, "vz": 0.0},
            {"id": "neptune", "name": "Neptune", "mass": 5.151e-5, "radius_km": 24622.0, "radius_display": 0.9, "color": "#3b82f6", "x": 30.05, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 1.144, "vz": 0.0}
        ]
    },
    "trappist_1_resonance": {
        "id": "trappist_1_resonance",
        "name": "TRAPPIST-1 Laplace Resonant Chain (7 Worlds)",
        "description": "Seven Earth-sized exoplanets orbiting an ultra-cool M-dwarf in a resonant chain (24:15:9:6:4:3:2 approximate frequency ratios).",
        "mode_focus": "Researcher",
        "default_time_years": 0.15,
        "default_dt_days": 0.02,
        "recommended_integrator": "whfast",
        "assumptions": [
            "Point-mass Newtonian mechanics.",
            "Ultra-compact resonant chain around M8V star.",
            "Three-body Laplace resonances maintain long-term dynamical packing stability."
        ],
        "units": {
            "distance": "AU",
            "mass": "M_sun",
            "time": "years",
            "velocity": "AU/year"
        },
        "bodies": [
            {"id": "trappist-1", "name": "TRAPPIST-1", "mass": 0.0898, "radius_km": 84100.0, "radius_display": 1.4, "color": "#dc2626", "x": 0.0, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 0.0, "vz": 0.0},
            {"id": "b", "name": "TRAPPIST-1b", "mass": 3.05e-6, "radius_km": 7111.0, "radius_display": 0.5, "color": "#94a3b8", "x": 0.0115, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 17.5, "vz": 0.0},
            {"id": "c", "name": "TRAPPIST-1c", "mass": 3.48e-6, "radius_km": 6976.0, "radius_display": 0.5, "color": "#facc15", "x": 0.0158, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 14.9, "vz": 0.0},
            {"id": "d", "name": "TRAPPIST-1d", "mass": 1.16e-6, "radius_km": 4995.0, "radius_display": 0.45, "color": "#fb923c", "x": 0.0223, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 12.6, "vz": 0.0},
            {"id": "e", "name": "TRAPPIST-1e", "mass": 2.08e-6, "radius_km": 5861.0, "radius_display": 0.5, "color": "#38bdf8", "x": 0.0293, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 11.0, "vz": 0.0},
            {"id": "f", "name": "TRAPPIST-1f", "mass": 3.12e-6, "radius_km": 6658.0, "radius_display": 0.5, "color": "#a855f7", "x": 0.0385, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 9.6, "vz": 0.0},
            {"id": "g", "name": "TRAPPIST-1g", "mass": 3.96e-6, "radius_km": 7320.0, "radius_display": 0.5, "color": "#06b6d4", "x": 0.0469, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 8.7, "vz": 0.0},
            {"id": "h", "name": "TRAPPIST-1h", "mass": 0.98e-6, "radius_km": 4924.0, "radius_display": 0.4, "color": "#ec4899", "x": 0.0619, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 7.6, "vz": 0.0}
        ]
    },
    "lagrange_trojans": {
        "id": "lagrange_trojans",
        "name": "Sun - Jupiter with L4/L5 Trojan Asteroids",
        "description": "Restricted 3-body system demonstrating the gravitational stability of equilateral Lagrange points L4 (leading) and L5 (trailing).",
        "mode_focus": "Student / Citizen",
        "default_time_years": 12.0,
        "default_dt_days": 5.0,
        "recommended_integrator": "whfast",
        "assumptions": [
            "Circular restricted three-body problem (CR3BP) approximation.",
            "Trojans treated as test particles with negligible mass perturbation on Jupiter.",
            "Demonstrates Jacobi energy constant conservation."
        ],
        "units": {
            "distance": "AU",
            "mass": "M_sun",
            "time": "years",
            "velocity": "AU/year"
        },
        "bodies": [
            {"id": "sun", "name": "Sun", "mass": 1.0, "radius_km": 696340.0, "radius_display": 1.6, "color": "#f59e0b", "x": 0.0, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 0.0, "vz": 0.0},
            {"id": "jupiter", "name": "Jupiter", "mass": 0.000954, "radius_km": 69911.0, "radius_display": 1.1, "color": "#d97706", "x": 5.204, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 2.754, "vz": 0.0},
            {"id": "trojan_l4", "name": "L4 Trojan Asteroid (Greek Camp)", "mass": 1e-12, "radius_km": 100.0, "radius_display": 0.5, "color": "#22c55e", "x": 2.602, "y": 4.507, "z": 0.0, "vx": -2.385, "vy": 1.377, "vz": 0.0},
            {"id": "trojan_l5", "name": "L5 Trojan Asteroid (Trojan Camp)", "mass": 1e-12, "radius_km": 100.0, "radius_display": 0.5, "color": "#a855f7", "x": 2.602, "y": -4.507, "z": 0.0, "vx": 2.385, "vy": 1.377, "vz": 0.0}
        ]
    },
    "figure_eight_choreography": {
        "id": "figure_eight_choreography",
        "name": "Figure-Eight Three-Body Choreography",
        "description": "The Chenciner-Montgomery periodic solution where three equal masses chase each other indefinitely along a figure-8 curve with zero angular momentum.",
        "mode_focus": "Citizen / Student / Researcher",
        "default_time_years": 2.0,
        "default_dt_days": 0.2,
        "recommended_integrator": "ias15",
        "assumptions": [
            "Dimensionless normalized gravitational units (G = 1, m = 1).",
            "Zero total angular momentum (L = 0).",
            "Requires high-precision non-symplectic IAS15 integrator to avoid breaking the delicate periodic orbit."
        ],
        "units": {
            "distance": "normalized",
            "mass": "normalized",
            "time": "normalized",
            "velocity": "normalized"
        },
        "bodies": [
            {"id": "star_1", "name": "Body A (Alpha)", "mass": 1.0, "radius_km": 50000.0, "radius_display": 1.0, "color": "#38bdf8", "x": 0.97000436, "y": -0.24308753, "z": 0.0, "vx": 0.46620531, "vy": 0.43236573, "vz": 0.0},
            {"id": "star_2", "name": "Body B (Beta)", "mass": 1.0, "radius_km": 50000.0, "radius_display": 1.0, "color": "#f43f5e", "x": -0.97000436, "y": 0.24308753, "z": 0.0, "vx": 0.46620531, "vy": 0.43236573, "vz": 0.0},
            {"id": "star_3", "name": "Body C (Gamma)", "mass": 1.0, "radius_km": 50000.0, "radius_display": 1.0, "color": "#fbbf24", "x": 0.0, "y": 0.0, "z": 0.0, "vx": -0.93241062, "vy": -0.86473146, "vz": 0.0}
        ]
    },
    "chaotic_three_body": {
        "id": "chaotic_three_body",
        "name": "Chaotic Three-Body Interaction (Pythagorean Problem)",
        "description": "Three stars placed at the vertices of a 3-4-5 right triangle at rest. Demonstrates sensitive dependence on initial conditions and eventual gravitational ejection.",
        "mode_focus": "Researcher / Student",
        "default_time_years": 1.5,
        "default_dt_days": 0.1,
        "recommended_integrator": "ias15",
        "assumptions": [
            "Dimensionless normalized units (G = 1).",
            "Bodies initialized from rest (v0 = 0).",
            "Displays extreme chaotic Lyapunov divergence and close triple-encounters."
        ],
        "units": {
            "distance": "normalized",
            "mass": "normalized",
            "time": "normalized",
            "velocity": "normalized"
        },
        "bodies": [
            {"id": "star_3m", "name": "Star 3 (Mass 3.0)", "mass": 3.0, "radius_km": 70000.0, "radius_display": 1.2, "color": "#38bdf8", "x": 1.0, "y": -1.0, "z": 0.0, "vx": 0.0, "vy": 0.0, "vz": 0.0},
            {"id": "star_4m", "name": "Star 4 (Mass 4.0)", "mass": 4.0, "radius_km": 80000.0, "radius_display": 1.3, "color": "#f59e0b", "x": -2.0, "y": -1.0, "z": 0.0, "vx": 0.0, "vy": 0.0, "vz": 0.0},
            {"id": "star_5m", "name": "Star 5 (Mass 5.0)", "mass": 5.0, "radius_km": 90000.0, "radius_display": 1.4, "color": "#ef4444", "x": 1.0, "y": 3.0, "z": 0.0, "vx": 0.0, "vy": 0.0, "vz": 0.0}
        ]
    },
    "binary_circumbinary": {
        "id": "binary_circumbinary",
        "name": "Binary Star System with Circumbinary Planet",
        "description": "Two central stars orbiting their common barycenter, with a stable circumbinary planet orbiting further out in the Keplerian regime.",
        "mode_focus": "All Modes",
        "default_time_years": 4.0,
        "default_dt_days": 0.5,
        "recommended_integrator": "ias15",
        "assumptions": [
            "Point-mass Newtonian mechanics.",
            "Stellar binary semi-major axis ~ 0.95 AU.",
            "Planet orbit semi-major axis ~ 3.2 AU satisfies Holman-Wiegert dynamical stability criterion (a_crit ~ 2.5 * a_binary)."
        ],
        "units": {
            "distance": "AU",
            "mass": "M_sun",
            "time": "years",
            "velocity": "AU/year"
        },
        "bodies": [
            {"id": "star_a", "name": "Primary Star A", "mass": 1.1, "radius_km": 720000.0, "radius_display": 1.3, "color": "#fbbf24", "x": -0.4, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": -4.0, "vz": 0.0},
            {"id": "star_b", "name": "Secondary Star B", "mass": 0.8, "radius_km": 600000.0, "radius_display": 1.1, "color": "#f97316", "x": 0.55, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 5.5, "vz": 0.0},
            {"id": "planet", "name": "Circumbinary Planet", "mass": 3e-6, "radius_km": 6371.0, "radius_display": 0.7, "color": "#38bdf8", "x": 3.2, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 4.8, "vz": 0.0}
        ]
    }
}


def get_all_scenarios() -> List[Dict[str, Any]]:
    """Returns headers for all available scientific simulation scenarios."""
    return [
        {
            "id": s["id"],
            "name": s["name"],
            "description": s["description"],
            "mode_focus": s["mode_focus"],
            "body_count": len(s["bodies"]),
            "default_time_years": s["default_time_years"],
            "recommended_integrator": s["recommended_integrator"],
            "assumptions": s.get("assumptions", []),
            "units": s.get("units", {})
        }
        for s in SCENARIOS.values()
    ]


def get_scenario_by_id(scenario_id: str) -> Optional[Dict[str, Any]]:
    """Returns full scenario configuration including bodies, initial conditions and metadata."""
    return SCENARIOS.get(scenario_id)
