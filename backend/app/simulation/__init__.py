"""
NEBULA N-Body and Orbital Simulation Engine.
Provides REBOUND integration (IAS15, WHFast, Leapfrog) with pure NumPy Symplectic fallback,
Hamiltonian energy conservation analytics, preconfigured astrophysical scenarios,
and lifecycle simulation management.
"""
from app.simulation.scenarios import (
    SCENARIOS,
    G_AU_MSUN_YEAR,
    get_all_scenarios,
    get_scenario_by_id
)
from app.simulation.conservation import (
    compute_total_energy,
    compute_kinetic_energy,
    compute_potential_energy,
    compute_angular_momentum,
    compute_center_of_mass,
    compute_energy_drift
)
from app.simulation.nbody_engine import (
    simulate_scenario,
    run_rebound_simulation,
    run_numpy_symplectic_simulation,
    validate_simulation_parameters,
    HAS_REBOUND
)
from app.simulation.manager import (
    simulation_manager,
    SimulationManager
)

__all__ = [
    "SCENARIOS",
    "G_AU_MSUN_YEAR",
    "get_all_scenarios",
    "get_scenario_by_id",
    "compute_total_energy",
    "compute_kinetic_energy",
    "compute_potential_energy",
    "compute_angular_momentum",
    "compute_center_of_mass",
    "compute_energy_drift",
    "simulate_scenario",
    "run_rebound_simulation",
    "run_numpy_symplectic_simulation",
    "validate_simulation_parameters",
    "HAS_REBOUND",
    "simulation_manager",
    "SimulationManager"
]
