"""
Simulation Session Manager for NEBULA.
Manages the lifecycle of N-body simulation jobs:
- Creation
- Execution
- Cancellation / Stop
- Result caching and retrieval
- Reproducibility verification
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import logging

from app.simulation.nbody_engine import (
    simulate_scenario,
    validate_simulation_parameters
)
from app.simulation.scenarios import get_scenario_by_id, SCENARIOS

logger = logging.getLogger(__name__)


class SimulationRecord:
    def __init__(
        self,
        sim_id: str,
        scenario_id: str,
        parameters: Dict[str, Any],
        status: str = "created"
    ):
        self.id = sim_id
        self.scenario_id = scenario_id
        self.parameters = parameters
        self.status = status
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.completed_at: Optional[str] = None
        self.results: Optional[Dict[str, Any]] = None
        self.error: Optional[str] = None

    def to_summary_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "scenario_id": self.scenario_id,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "parameters": self.parameters,
            "has_results": self.results is not None,
            "error": self.error
        }


class SimulationManager:
    """Singleton in-memory store for active and past simulations."""

    def __init__(self, max_cached_runs: int = 50):
        self._simulations: Dict[str, SimulationRecord] = {}
        self._max_cached_runs = max_cached_runs

    def create_simulation(
        self,
        scenario_id: str = "sun_earth",
        duration: Optional[float] = None,
        timestep: Optional[float] = None,
        num_steps: int = 150,
        integrator: str = "ias15",
        selected_bodies: Optional[List[str]] = None,
        custom_bodies: Optional[List[Dict[str, Any]]] = None,
        auto_run: bool = False
    ) -> Dict[str, Any]:
        """Creates a new simulation entry and optionally executes it immediately."""
        scenario = get_scenario_by_id(scenario_id)
        if not scenario:
            scenario_id = "sun_earth"
            scenario = SCENARIOS["sun_earth"]

        dur = duration if (duration and duration > 0) else scenario["default_time_years"]

        # Validate parameters
        is_valid, err_msg = validate_simulation_parameters(
            scenario_id=scenario_id,
            duration=dur,
            num_steps=num_steps,
            timestep=timestep,
            selected_body_ids=selected_bodies
        )
        if not is_valid:
            raise ValueError(err_msg)

        sim_id = str(uuid.uuid4())[:12]
        params = {
            "scenario_id": scenario_id,
            "scenario_name": scenario["name"],
            "duration": dur,
            "timestep": timestep,
            "num_steps": num_steps,
            "integrator": integrator,
            "selected_bodies": selected_bodies,
            "has_custom_bodies": custom_bodies is not None
        }

        record = SimulationRecord(
            sim_id=sim_id,
            scenario_id=scenario_id,
            parameters=params,
            status="created"
        )

        # Evict oldest if exceeding capacity
        if len(self._simulations) >= self._max_cached_runs:
            oldest_key = next(iter(self._simulations))
            del self._simulations[oldest_key]

        self._simulations[sim_id] = record

        if auto_run:
            self.run_simulation(
                sim_id=sim_id,
                custom_bodies=custom_bodies
            )

        return self.get_simulation(sim_id)

    def run_simulation(
        self,
        sim_id: str,
        custom_bodies: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Runs the simulation identified by sim_id."""
        record = self._simulations.get(sim_id)
        if not record:
            raise KeyError(f"Simulation '{sim_id}' not found.")

        if record.status == "completed" and record.results is not None:
            return record.to_summary_dict()

        record.status = "running"
        try:
            params = record.parameters
            result = simulate_scenario(
                scenario_id=record.scenario_id,
                integrator=params.get("integrator", "ias15"),
                total_time_years=params.get("duration"),
                num_steps=params.get("num_steps", 150),
                timestep_override=params.get("timestep"),
                selected_body_ids=params.get("selected_bodies"),
                custom_bodies=custom_bodies
            )
            record.results = result
            record.status = "completed"
            record.completed_at = datetime.now(timezone.utc).isoformat()
        except Exception as e:
            logger.exception(f"Simulation {sim_id} failed: {e}")
            record.status = "failed"
            record.error = str(e)
            raise

        return record.to_summary_dict()

    def stop_simulation(self, sim_id: str) -> Dict[str, Any]:
        """Stops/cancels a simulation run."""
        record = self._simulations.get(sim_id)
        if not record:
            raise KeyError(f"Simulation '{sim_id}' not found.")

        if record.status in ["created", "running"]:
            record.status = "stopped"
            record.completed_at = datetime.now(timezone.utc).isoformat()

        return record.to_summary_dict()

    def get_simulation(self, sim_id: str) -> Optional[Dict[str, Any]]:
        """Returns simulation status and parameters."""
        record = self._simulations.get(sim_id)
        if not record:
            return None
        return record.to_summary_dict()

    def get_simulation_results(self, sim_id: str) -> Optional[Dict[str, Any]]:
        """Returns the full computed results payload for the given simulation."""
        record = self._simulations.get(sim_id)
        if not record:
            return None
        if record.status != "completed" or record.results is None:
            return None
        return record.results

    def list_simulations(self) -> List[Dict[str, Any]]:
        """Returns all registered simulation jobs."""
        return [record.to_summary_dict() for record in reversed(list(self._simulations.values()))]


# Global simulation manager instance
simulation_manager = SimulationManager()
