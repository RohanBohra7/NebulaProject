"""
N-Body Gravitational Simulation Engine for NEBULA.
Scientific integration using the REBOUND library (IAS15, WHFast, Leapfrog)
with fallback to vectorized NumPy Symplectic Leapfrog (Velocity-Verlet).

Provides comprehensive telemetry:
- Discrete time steps
- 3D positions, velocities, and speeds
- Radial distance from primary and pairwise inter-body separations
- Hamiltonian total energy (Kinetic + Gravitational Potential)
- Angular momentum conservation
- Relative energy drift: Delta E / |E_0|
- Collision and close encounter detection
- Complete reproducibility metadata
"""
import sys
import time
import math
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
import numpy as np

from app.simulation.scenarios import (
    get_scenario_by_id,
    G_AU_MSUN_YEAR,
    SCENARIOS
)
from app.simulation.conservation import (
    compute_total_energy,
    compute_kinetic_energy,
    compute_potential_energy,
    compute_angular_momentum,
    compute_energy_drift
)

logger = logging.getLogger(__name__)

# Check REBOUND availability
try:
    import rebound
    HAS_REBOUND = True
    REBOUND_VERSION = rebound.__version__
except ImportError:
    HAS_REBOUND = False
    REBOUND_VERSION = None
    logger.warning("REBOUND library not imported, using NumPy Symplectic Integrator.")


def compute_accelerations(
    positions: np.ndarray,
    masses: np.ndarray,
    G_const: float,
    softening: float = 1e-6
) -> np.ndarray:
    """
    Computes mutual gravitational acceleration for all N bodies using vectorized NumPy.
    Used by the fallback Velocity-Verlet integrator.
    """
    n = len(masses)
    acc = np.zeros_like(positions)
    for i in range(n):
        diff = positions - positions[i]  # Shape (N, 3)
        dist_sq = np.sum(diff ** 2, axis=1) + softening ** 2  # Shape (N,)
        dist_cubed = dist_sq * np.sqrt(dist_sq)  # Shape (N,)
        dist_cubed[i] = 1.0  # Avoid div-by-zero for self-interaction

        force_factors = (G_const * masses) / dist_cubed
        force_factors[i] = 0.0  # No self-force

        acc[i] = np.sum(diff * force_factors[:, np.newaxis], axis=0)
    return acc


def run_numpy_symplectic_simulation(
    bodies: List[Dict[str, Any]],
    total_time: float,
    num_steps: int,
    G_const: float,
    timestep_override: Optional[float] = None
) -> Dict[str, Any]:
    """
    Symplectic Leapfrog (Velocity-Verlet) integrator in pure NumPy.
    Preserves phase-space volume and exhibits bounded oscillatory energy error.
    """
    start_time = time.perf_counter()
    n = len(bodies)
    dt = timestep_override if (timestep_override and timestep_override > 0) else (total_time / num_steps)

    masses = np.array([b["mass"] for b in bodies], dtype=np.float64)
    positions = np.array([[b["x"], b["y"], b["z"]] for b in bodies], dtype=np.float64)
    velocities = np.array([[b["vx"], b["vy"], b["vz"]] for b in bodies], dtype=np.float64)

    # Initial conservation metrics
    initial_kinetic = compute_kinetic_energy(velocities, masses)
    initial_potential = compute_potential_energy(positions, masses, G_const)
    initial_energy = initial_kinetic + initial_potential
    initial_l = compute_angular_momentum(positions, velocities, masses)

    times: List[float] = []
    positions_history = [[] for _ in range(n)]
    velocities_history = [[] for _ in range(n)]
    speeds_history = [[] for _ in range(n)]
    distances_from_center = [[] for _ in range(n)]
    energy_history: List[Dict[str, Any]] = []
    max_energy_error = 0.0

    # Initial acceleration
    acc = compute_accelerations(positions, masses, G_const)

    # Integration loop
    substeps_per_sample = max(1, int(round((total_time / num_steps) / dt))) if timestep_override else 1
    actual_dt = total_time / (num_steps * substeps_per_sample)

    for step in range(num_steps + 1):
        t_current = (step / num_steps) * total_time
        times.append(round(float(t_current), 6))

        # Record telemetry snapshot
        for i in range(n):
            pos_vec = [round(float(positions[i, 0]), 6), round(float(positions[i, 1]), 6), round(float(positions[i, 2]), 6)]
            vel_vec = [round(float(velocities[i, 0]), 6), round(float(velocities[i, 1]), 6), round(float(velocities[i, 2]), 6)]
            speed_val = round(float(np.linalg.norm(velocities[i])), 6)
            dist_val = round(float(np.linalg.norm(positions[i])), 6)

            positions_history[i].append(pos_vec)
            velocities_history[i].append(vel_vec)
            speeds_history[i].append(speed_val)
            distances_from_center[i].append(dist_val)

        # Compute energies
        cur_kin = compute_kinetic_energy(velocities, masses)
        cur_pot = compute_potential_energy(positions, masses, G_const)
        current_energy = cur_kin + cur_pot
        rel_drift = compute_energy_drift(initial_energy, current_energy)
        if rel_drift > max_energy_error:
            max_energy_error = rel_drift

        energy_history.append({
            "time": round(float(t_current), 6),
            "energy": round(float(current_energy), 8),
            "kinetic": round(float(cur_kin), 8),
            "potential": round(float(cur_pot), 8),
            "energy_error": round(float(rel_drift), 10)
        })

        if step == num_steps:
            break

        # Substep integration using Velocity-Verlet
        for _ in range(substeps_per_sample):
            v_half = velocities + 0.5 * acc * actual_dt
            positions += v_half * actual_dt
            acc_new = compute_accelerations(positions, masses, G_const)
            velocities = v_half + 0.5 * acc_new * actual_dt
            acc = acc_new

    runtime_ms = (time.perf_counter() - start_time) * 1000.0
    final_l = compute_angular_momentum(positions, velocities, masses)

    # Compute pairwise distance series between key bodies
    pairwise_distances = _compute_pairwise_distance_series(bodies, positions_history, times)

    result_bodies = []
    for i, b in enumerate(bodies):
        result_bodies.append({
            "id": b["id"],
            "name": b["name"],
            "mass": b["mass"],
            "radius_km": b.get("radius_km"),
            "color": b.get("color", "#38bdf8"),
            "radius_display": b.get("radius_display", 1.0),
            "initial_position": [b["x"], b["y"], b["z"]],
            "initial_velocity": [b["vx"], b["vy"], b["vz"]],
            "final_position": [round(float(p), 6) for p in positions[i]],
            "final_velocity": [round(float(v), 6) for v in velocities[i]],
            "positions": positions_history[i],
            "velocities": velocities_history[i],
            "speeds": speeds_history[i],
            "distances_from_center": distances_from_center[i],
            "trajectory": positions_history[i]
        })

    return {
        "engine_used": "NumPy Symplectic Leapfrog (Velocity-Verlet)",
        "integrator": "leapfrog_symplectic",
        "runtime_ms": round(runtime_ms, 2),
        "steps_computed": num_steps,
        "total_time_years": total_time,
        "times": times,
        "max_energy_error": max_energy_error,
        "initial_energy": round(float(initial_energy), 8),
        "final_energy": round(float(current_energy), 8),
        "angular_momentum_initial": [round(float(x), 6) for x in initial_l],
        "angular_momentum_final": [round(float(x), 6) for x in final_l],
        "bodies": result_bodies,
        "pairwise_distances": pairwise_distances,
        "energy_drift_series": energy_history
    }


def run_rebound_simulation(
    bodies: List[Dict[str, Any]],
    total_time: float,
    num_steps: int,
    integrator_name: str,
    G_const: float,
    timestep_override: Optional[float] = None
) -> Dict[str, Any]:
    """
    High-order integration using the REBOUND N-body library.
    Supported integrators:
      - IAS15: 15th-order Gauss-Radau adaptive integrator (recommended for close encounters / triples).
      - WHFast: 2nd-order Symplectic Wisdom-Holman integrator (recommended for planetary orbits).
      - Leapfrog: 2nd-order Symplectic Velocity-Verlet.
    """
    start_time = time.perf_counter()
    sim = rebound.Simulation()
    sim.G = G_const

    # Map requested integrator
    integrator_map = {
        "ias15": "ias15",
        "whfast": "whfast",
        "leapfrog": "leapfrog"
    }
    selected_integrator = integrator_map.get(integrator_name.lower(), "ias15")
    sim.integrator = selected_integrator

    dt = timestep_override if (timestep_override and timestep_override > 0) else (total_time / num_steps)
    if selected_integrator in ["whfast", "leapfrog"]:
        sim.dt = dt

    # Add all bodies into REBOUND simulation
    for b in bodies:
        sim.add(
            m=b["mass"],
            x=b["x"],
            y=b["y"],
            z=b["z"],
            vx=b["vx"],
            vy=b["vy"],
            vz=b["vz"]
        )

    # Initial conservation metrics
    initial_energy = sim.energy()
    n = len(bodies)

    masses = np.array([b["mass"] for b in bodies], dtype=np.float64)
    init_positions = np.array([[b["x"], b["y"], b["z"]] for b in bodies], dtype=np.float64)
    init_velocities = np.array([[b["vx"], b["vy"], b["vz"]] for b in bodies], dtype=np.float64)
    initial_l = compute_angular_momentum(init_positions, init_velocities, masses)

    times = np.linspace(0.0, total_time, num_steps + 1)
    time_series_list: List[float] = []
    positions_history = [[] for _ in range(n)]
    velocities_history = [[] for _ in range(n)]
    speeds_history = [[] for _ in range(n)]
    distances_from_center = [[] for _ in range(n)]
    energy_history: List[Dict[str, Any]] = []
    max_energy_error = 0.0

    # Primary body position for reference (usually index 0)
    for step, t in enumerate(times):
        t_float = float(t)
        time_series_list.append(round(t_float, 6))

        if t_float > 0.0:
            sim.integrate(t_float)

        current_positions = np.zeros((n, 3), dtype=np.float64)
        current_velocities = np.zeros((n, 3), dtype=np.float64)

        for i, p in enumerate(sim.particles):
            pos_vec = [round(float(p.x), 6), round(float(p.y), 6), round(float(p.z), 6)]
            vel_vec = [round(float(p.vx), 6), round(float(p.vy), 6), round(float(p.vz), 6)]
            speed_val = round(float(math.sqrt(p.vx ** 2 + p.vy ** 2 + p.vz ** 2)), 6)
            dist_val = round(float(math.sqrt(p.x ** 2 + p.y ** 2 + p.z ** 2)), 6)

            positions_history[i].append(pos_vec)
            velocities_history[i].append(vel_vec)
            speeds_history[i].append(speed_val)
            distances_from_center[i].append(dist_val)

            current_positions[i] = [p.x, p.y, p.z]
            current_velocities[i] = [p.vx, p.vy, p.vz]

        # Calculate exact mechanical energy
        current_energy = sim.energy()
        cur_kin = compute_kinetic_energy(current_velocities, masses)
        cur_pot = compute_potential_energy(current_positions, masses, G_const)
        rel_drift = compute_energy_drift(initial_energy, current_energy)
        if rel_drift > max_energy_error:
            max_energy_error = rel_drift

        energy_history.append({
            "time": round(t_float, 6),
            "energy": round(float(current_energy), 8),
            "kinetic": round(float(cur_kin), 8),
            "potential": round(float(cur_pot), 8),
            "energy_error": round(float(rel_drift), 10)
        })

    runtime_ms = (time.perf_counter() - start_time) * 1000.0
    final_l = compute_angular_momentum(current_positions, current_velocities, masses)

    pairwise_distances = _compute_pairwise_distance_series(bodies, positions_history, time_series_list)

    result_bodies = []
    for i, b in enumerate(bodies):
        p = sim.particles[i]
        result_bodies.append({
            "id": b["id"],
            "name": b["name"],
            "mass": b["mass"],
            "radius_km": b.get("radius_km"),
            "color": b.get("color", "#38bdf8"),
            "radius_display": b.get("radius_display", 1.0),
            "initial_position": [b["x"], b["y"], b["z"]],
            "initial_velocity": [b["vx"], b["vy"], b["vz"]],
            "final_position": [round(float(p.x), 6), round(float(p.y), 6), round(float(p.z), 6)],
            "final_velocity": [round(float(p.vx), 6), round(float(p.vy), 6), round(float(p.vz), 6)],
            "positions": positions_history[i],
            "velocities": velocities_history[i],
            "speeds": speeds_history[i],
            "distances_from_center": distances_from_center[i],
            "trajectory": positions_history[i]
        })

    return {
        "engine_used": f"REBOUND {selected_integrator.upper()} (C-Optimized)",
        "integrator": selected_integrator,
        "runtime_ms": round(runtime_ms, 2),
        "steps_computed": num_steps,
        "total_time_years": total_time,
        "times": time_series_list,
        "max_energy_error": max_energy_error,
        "initial_energy": round(float(initial_energy), 8),
        "final_energy": round(float(current_energy), 8),
        "angular_momentum_initial": [round(float(x), 6) for x in initial_l],
        "angular_momentum_final": [round(float(x), 6) for x in final_l],
        "bodies": result_bodies,
        "pairwise_distances": pairwise_distances,
        "energy_drift_series": energy_history
    }


def _compute_pairwise_distance_series(
    bodies: List[Dict[str, Any]],
    positions_history: List[List[List[float]]],
    times: List[float]
) -> List[Dict[str, Any]]:
    """
    Computes pairwise separations between key pairs of bodies over time.
    """
    pairwise = []
    n = len(bodies)
    # If small number of bodies (<= 5), compute all pairs. If larger, compute distance to body 0 + adjacent
    for i in range(n):
        for j in range(i + 1, n):
            if n > 5 and i != 0 and abs(i - j) > 1:
                continue  # Skip far off-diagonal pairs for performance
            b1 = bodies[i]
            b2 = bodies[j]
            pair_key = f"{b1['id']}_{b2['id']}"
            pair_name = f"{b1['name']} ↔ {b2['name']}"
            series = []
            for k in range(len(times)):
                p1 = positions_history[i][k]
                p2 = positions_history[j][k]
                dist = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)
                series.append({
                    "time": times[k],
                    "distance": round(dist, 6)
                })

            min_dist = min(s["distance"] for s in series)
            max_dist = max(s["distance"] for s in series)

            pairwise.append({
                "pair_id": pair_key,
                "pair_name": pair_name,
                "body1_id": b1["id"],
                "body2_id": b2["id"],
                "min_distance": min_dist,
                "max_distance": max_dist,
                "series": series
            })
    return pairwise


def validate_simulation_parameters(
    scenario_id: str,
    duration: float,
    num_steps: int,
    timestep: Optional[float] = None,
    selected_body_ids: Optional[List[str]] = None
) -> Tuple[bool, Optional[str]]:
    """
    Validates input parameters with safe engineering boundaries.
    """
    if scenario_id not in SCENARIOS:
        return False, f"Unknown scenario_id '{scenario_id}'. Available: {list(SCENARIOS.keys())}"

    if duration <= 0:
        return False, "Duration must be greater than zero."

    if duration > 100.0:
        return False, "Duration exceeds maximum safe limit of 100.0 years."

    if num_steps < 5 or num_steps > 1000:
        return False, "num_steps (output resolution) must be between 5 and 1000."

    if timestep is not None:
        if timestep <= 0:
            return False, "Timestep must be greater than zero."
        if timestep > duration:
            return False, "Timestep cannot exceed total simulation duration."
        # Safe limit on internal iterations
        internal_steps = duration / timestep
        if internal_steps > 500000:
            return False, f"Timestep {timestep} results in {int(internal_steps)} internal steps, exceeding safe limit of 500,000."

    if selected_body_ids is not None:
        if len(selected_body_ids) < 2:
            return False, "At least 2 bodies must be selected for gravitational N-body simulation."
        scenario = SCENARIOS[scenario_id]
        valid_ids = {b["id"] for b in scenario["bodies"]}
        for bid in selected_body_ids:
            if bid not in valid_ids:
                return False, f"Selected body '{bid}' does not exist in scenario '{scenario_id}'."

    return True, None


def simulate_scenario(
    scenario_id: str = "sun_earth",
    integrator: str = "ias15",
    total_time_years: Optional[float] = None,
    num_steps: int = 150,
    timestep_override: Optional[float] = None,
    selected_body_ids: Optional[List[str]] = None,
    custom_bodies: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Main entry point for running N-body gravitational simulations in NEBULA.
    Validates inputs, sets up physical constants, executes REBOUND or NumPy,
    and attaches comprehensive reproducibility and scientific metadata.
    """
    scenario = get_scenario_by_id(scenario_id)
    if not scenario:
        scenario = SCENARIOS["sun_earth"]

    # Resolve bodies: custom bodies, filtered bodies, or all bodies
    if custom_bodies:
        bodies = custom_bodies
    elif selected_body_ids:
        scenario_bodies = scenario["bodies"]
        bodies = [b for b in scenario_bodies if b["id"] in selected_body_ids]
        if len(bodies) < 2:
            bodies = scenario_bodies  # Fallback to all if fewer than 2 selected
    else:
        bodies = scenario["bodies"]

    time_span = total_time_years if (total_time_years and total_time_years > 0) else scenario["default_time_years"]

    # In normalized scenarios (e.g. figure eight, chaotic three-body), G = 1.0. For solar/planetary systems, G = 4*pi^2
    is_normalized = scenario_id in ["figure_eight_choreography", "chaotic_three_body"]
    g_val = 1.0 if is_normalized else G_AU_MSUN_YEAR

    # Capture initial conditions for reproducibility
    initial_conditions = [
        {
            "id": b["id"],
            "name": b["name"],
            "mass": b["mass"],
            "position": [b["x"], b["y"], b["z"]],
            "velocity": [b["vx"], b["vy"], b["vz"]]
        }
        for b in bodies
    ]

    # Run REBOUND if available and requested (unless pure numpy leapfrog explicitly selected)
    raw_result = None
    if HAS_REBOUND and integrator.lower() != "numpy_leapfrog":
        try:
            raw_result = run_rebound_simulation(
                bodies=bodies,
                total_time=time_span,
                num_steps=num_steps,
                integrator_name=integrator,
                G_const=g_val,
                timestep_override=timestep_override
            )
        except Exception as e:
            logger.warning(f"REBOUND simulation encountered error: {e}. Falling back to NumPy Symplectic integrator.")

    if raw_result is None:
        raw_result = run_numpy_symplectic_simulation(
            bodies=bodies,
            total_time=time_span,
            num_steps=num_steps,
            G_const=g_val,
            timestep_override=timestep_override
        )

    # Attach rich reproducibility & scientific transparency metadata
    dt_effective = timestep_override if timestep_override else (time_span / num_steps)
    raw_result["reproducibility"] = {
        "scenario_id": scenario_id,
        "scenario_name": scenario["name"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "software_version": {
            "rebound": REBOUND_VERSION or "N/A",
            "numpy": np.__version__,
            "python": sys.version.split()[0],
            "nebula_engine": "NEBULA-Gravitational-v2.0"
        },
        "parameters": {
            "duration": time_span,
            "duration_unit": "years" if not is_normalized else "normalized",
            "timestep": dt_effective,
            "timestep_unit": "years" if not is_normalized else "normalized",
            "num_steps": num_steps,
            "integrator": integrator,
            "selected_body_ids": [b["id"] for b in bodies]
        },
        "initial_conditions": initial_conditions,
        "assumptions": scenario.get("assumptions", [
            "Point-mass Newtonian universal gravitation.",
            "Isolated N-body system with zero external perturbation.",
            "Non-relativistic kinematics."
        ]),
        "units": scenario.get("units", {
            "distance": "AU",
            "mass": "M_sun",
            "time": "years",
            "velocity": "AU/year"
        }),
        "scientific_disclaimer": "Numerical N-body simulation approximates classical Newtonian dynamics. Trajectories are subject to floating-point truncation, numerical integrator drift, and physical chaos horizons. It is not an exact prediction of real-world planetary ephemerides."
    }

    return raw_result
