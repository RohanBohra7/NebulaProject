"""
REST API Router for N-Body and Orbital Simulation.
Exposes endpoints for:
- Preconfigured scientific scenarios
- Simulation creation, execution, stopping, and results retrieval
- Backward-compatible direct run endpoints
"""
import uuid
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import SimulationRunRecord
from app.schemas.simulation import (
    CreateSimulationRequest,
    RunSimulationRequest,
    SimulationSummaryResponse,
    SimulationFullResult
)
from app.simulation.scenarios import (
    get_all_scenarios,
    get_scenario_by_id,
    SCENARIOS
)
from app.simulation.nbody_engine import (
    simulate_scenario,
    validate_simulation_parameters
)
from app.simulation.manager import simulation_manager

router = APIRouter(tags=["N-Body Simulation"])


# ============================================================================
# Scenario Endpoints
# ============================================================================

@router.get("/simulations/scenarios", response_model=List[Dict[str, Any]])
@router.get("/simulation/scenarios", response_model=List[Dict[str, Any]])
def list_scenarios():
    """Returns all preconfigured scientific simulation scenarios."""
    return get_all_scenarios()


@router.get("/simulations/scenarios/{scenario_id}")
@router.get("/simulation/scenarios/{scenario_id}")
def get_scenario(scenario_id: str):
    """Returns detailed configuration, particle initial states, assumptions, and units for a scenario."""
    scenario = get_scenario_by_id(scenario_id)
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario '{scenario_id}' not found. Available: {list(SCENARIOS.keys())}"
        )
    return scenario


# ============================================================================
# Simulation Lifecycle Endpoints (POST, GET, /run, /stop, /results)
# ============================================================================

@router.post("/simulations", response_model=SimulationSummaryResponse, status_code=status.HTTP_201_CREATED)
def create_simulation_endpoint(req: CreateSimulationRequest, db: Session = Depends(get_db)):
    """
    Creates a new simulation specification.
    If `auto_run=True` (default), runs the integration immediately and stores results.
    """
    try:
        sim_summary = simulation_manager.create_simulation(
            scenario_id=req.scenario_id,
            duration=req.duration,
            timestep=req.timestep,
            num_steps=req.num_steps,
            integrator=req.integrator,
            selected_bodies=req.selected_bodies,
            custom_bodies=req.custom_bodies,
            auto_run=req.auto_run
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Simulation error: {str(e)}")

    # Log to DB if run completed
    _persist_simulation_run(sim_summary["id"], db)
    return sim_summary


@router.get("/simulations", response_model=List[SimulationSummaryResponse])
def list_simulations_endpoint():
    """Lists all registered simulation runs in session history."""
    return simulation_manager.list_simulations()


@router.get("/simulations/{sim_id}", response_model=SimulationSummaryResponse)
def get_simulation_endpoint(sim_id: str):
    """Retrieves metadata and lifecycle status for a specific simulation."""
    sim = simulation_manager.get_simulation(sim_id)
    if not sim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Simulation with ID '{sim_id}' not found."
        )
    return sim


@router.post("/simulations/{sim_id}/run", response_model=SimulationSummaryResponse)
def run_simulation_by_id_endpoint(sim_id: str, db: Session = Depends(get_db)):
    """Executes or resumes an existing simulation by ID."""
    try:
        sim_summary = simulation_manager.run_simulation(sim_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Simulation with ID '{sim_id}' not found."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Execution error: {str(e)}"
        )

    _persist_simulation_run(sim_id, db)
    return sim_summary


@router.post("/simulations/{sim_id}/stop", response_model=SimulationSummaryResponse)
def stop_simulation_endpoint(sim_id: str):
    """Stops/cancels a running simulation."""
    try:
        return simulation_manager.stop_simulation(sim_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Simulation with ID '{sim_id}' not found."
        )


@router.get("/simulations/{sim_id}/results", response_model=SimulationFullResult)
def get_simulation_results_endpoint(sim_id: str):
    """
    Retrieves full computed trajectories, positions, velocities, distances,
    energy conservation metrics, and reproducibility metadata.
    """
    sim = simulation_manager.get_simulation(sim_id)
    if not sim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Simulation with ID '{sim_id}' not found."
        )

    results = simulation_manager.get_simulation_results(sim_id)
    if not results:
        if sim["status"] == "created":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Simulation '{sim_id}' has not been executed yet. Call POST /simulations/{sim_id}/run first."
            )
        elif sim["status"] == "running":
            raise HTTPException(
                status_code=status.HTTP_202_ACCEPTED,
                detail=f"Simulation '{sim_id}' is currently running."
            )
        elif sim["status"] == "stopped":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Simulation '{sim_id}' was stopped before results were generated."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Simulation '{sim_id}' failed: {sim.get('error')}"
            )
    return results


# ============================================================================
# Direct / Backward-Compatible Simulation Execution
# ============================================================================

@router.post("/simulation/run")
def direct_run_simulation_endpoint(req: RunSimulationRequest, db: Session = Depends(get_db)):
    """
    Synchronous direct execution endpoint (backward compatible).
    Executes N-body gravitational integration and returns results directly.
    """
    duration = req.duration or req.total_time_years
    is_valid, err_msg = validate_simulation_parameters(
        scenario_id=req.scenario_id,
        duration=duration or 1.0,
        num_steps=req.num_steps,
        timestep=req.timestep,
        selected_body_ids=req.selected_bodies
    )
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err_msg)

    result = simulate_scenario(
        scenario_id=req.scenario_id,
        integrator=req.integrator,
        total_time_years=duration,
        num_steps=req.num_steps,
        timestep_override=req.timestep,
        selected_body_ids=req.selected_bodies,
        custom_bodies=req.custom_bodies
    )

    # Persist simulation run log
    try:
        run_record = SimulationRunRecord(
            id=str(uuid.uuid4())[:8],
            scenario_id=req.scenario_id,
            integrator=result.get("integrator"),
            timestep_days=float(result.get("total_time_years", 1.0) * 365.25 / req.num_steps),
            total_time_days=float(result.get("total_time_years", 1.0) * 365.25),
            num_particles=len(result.get("bodies", [])),
            max_energy_error=float(result.get("max_energy_error", 0.0)),
            runtime_ms=float(result.get("runtime_ms", 0.0)),
            steps_computed=req.num_steps
        )
        db.add(run_record)
        db.commit()
    except Exception:
        pass

    return result


def _persist_simulation_run(sim_id: str, db: Session):
    """Helper to persist successful simulation run records to SQLite."""
    try:
        results = simulation_manager.get_simulation_results(sim_id)
        sim = simulation_manager.get_simulation(sim_id)
        if not results or not sim:
            return

        run_record = SimulationRunRecord(
            id=sim_id,
            scenario_id=sim["scenario_id"],
            integrator=results.get("integrator"),
            timestep_days=float(results.get("total_time_years", 1.0) * 365.25 / results.get("steps_computed", 150)),
            total_time_days=float(results.get("total_time_years", 1.0) * 365.25),
            num_particles=len(results.get("bodies", [])),
            max_energy_error=float(results.get("max_energy_error", 0.0)),
            runtime_ms=float(results.get("runtime_ms", 0.0)),
            steps_computed=results.get("steps_computed", 150)
        )
        db.add(run_record)
        db.commit()
    except Exception:
        pass
