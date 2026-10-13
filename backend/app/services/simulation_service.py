from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
import uuid
from app.simulation.scenarios import get_all_scenarios, get_scenario_by_id
from app.simulation.nbody_engine import simulate_scenario
from app.models.celestial import SimulationRunRecord
from app.core.exceptions import SimulationExecutionError

class SimulationService:
    @staticmethod
    def list_scenarios() -> List[Dict[str, Any]]:
        return get_all_scenarios()

    @staticmethod
    def get_scenario(scenario_id: str) -> Dict[str, Any]:
        scenario = get_scenario_by_id(scenario_id)
        if not scenario:
            raise SimulationExecutionError(f"Simulation scenario '{scenario_id}' not found.")
        return scenario

    @staticmethod
    def run_simulation(
        db: Optional[Session],
        scenario_id: str,
        integrator: str = "ias15",
        total_time_years: Optional[float] = None,
        num_steps: int = 150,
        custom_bodies: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        if num_steps < 10 or num_steps > 600:
            raise SimulationExecutionError("Number of simulation steps must be between 10 and 600.")

        result = simulate_scenario(
            scenario_id=scenario_id,
            integrator=integrator,
            total_time_years=total_time_years,
            num_steps=num_steps,
            custom_bodies=custom_bodies
        )

        if db:
            try:
                run_record = SimulationRunRecord(
                    id=str(uuid.uuid4())[:8],
                    scenario_id=scenario_id,
                    integrator=result.get("integrator"),
                    timestep_days=float(result.get("total_time_years", 1.0) * 365.25 / num_steps),
                    total_time_days=float(result.get("total_time_years", 1.0) * 365.25),
                    num_particles=len(result.get("bodies", [])),
                    max_energy_error=float(result.get("max_energy_error", 0.0)),
                    runtime_ms=float(result.get("runtime_ms", 0.0)),
                    steps_computed=num_steps
                )
                db.add(run_record)
                db.commit()
            except Exception:
                pass

        return result

simulation_service = SimulationService()
