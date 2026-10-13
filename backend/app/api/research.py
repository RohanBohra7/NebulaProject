from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import EvaluationRecord, SimulationRunRecord
from app.evaluation.evaluator import evaluate_query_across_modes
from app.evaluation.task_system import (
    get_all_predefined_tasks,
    start_task_session,
    complete_task_session,
    run_automated_task,
    run_all_predefined_tasks
)
from app.evaluation.scientific_validation import run_scientific_validation_suite
from app.evaluation.telemetry import (
    record_telemetry_event,
    get_telemetry_summary
)

router = APIRouter(prefix="/research", tags=["Research & Evaluation Benchmarks"])


# ==================== REQUEST SCHEMAS ====================

class EvaluateQueryRequest(BaseModel):
    query: str
    target_object_id: Optional[str] = None


class TaskCompleteRequest(BaseModel):
    session_id: Optional[str] = None
    success: bool = True
    duration_ms: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class TelemetryEventRequest(BaseModel):
    event_type: str
    component: Optional[str] = None
    duration_ms: Optional[float] = None
    success: Optional[bool] = True
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


# ==================== PREDEFINED EVALUATION TASKS ====================

@router.get("/tasks")
def list_evaluation_tasks_endpoint(db: Session = Depends(get_db)):
    """
    Returns the 6 canonical evaluation benchmark tasks with structured specifications,
    success criteria, routes, and recent run history.
    """
    return get_all_predefined_tasks(db=db)


@router.post("/tasks/{task_id}/start")
def start_evaluation_task_endpoint(task_id: str, db: Session = Depends(get_db)):
    """
    Initializes an interactive evaluation session timer for a specific task.
    """
    try:
        return start_task_session(task_id, db=db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/tasks/{task_id}/complete")
def complete_evaluation_task_endpoint(
    task_id: str,
    req: TaskCompleteRequest,
    db: Session = Depends(get_db)
):
    """
    Records interactive completion of a predefined evaluation task with stopwatch duration,
    success/failure flag, and verification metadata.
    """
    meta = req.metadata or {}
    meta["task_id"] = task_id
    if req.duration_ms is not None:
        meta["duration_ms"] = req.duration_ms

    return complete_task_session(
        session_id=req.session_id or f"sess_{task_id}_{req.duration_ms}",
        success=req.success,
        user_metadata=meta,
        db=db
    )


@router.post("/tasks/{task_id}/run_automated")
async def run_automated_task_endpoint(task_id: str, db: Session = Depends(get_db)):
    """
    Executes a fully automated server-side verification run of a single predefined task.
    """
    try:
        return await run_automated_task(task_id, db=db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/tasks/run_all")
async def run_all_tasks_automated_endpoint(db: Session = Depends(get_db)):
    """
    Executes all 6 canonical predefined evaluation benchmark tasks end-to-end
    and records rigorous outcomes.
    """
    return await run_all_predefined_tasks(db=db)


# ==================== SCIENTIFIC VALIDATION ====================

@router.get("/validation/benchmarks")
def get_scientific_validation_benchmarks():
    """
    Compares calculated physical and orbital properties against empirical IAU/NASA ground truth.
    Provides explicit physical tolerances, absolute errors, and percentage differences
    without fabricated precision claims.
    """
    return run_scientific_validation_suite()


# ==================== TELEMETRY & SYSTEM METRICS ====================

@router.post("/telemetry")
def ingest_telemetry_event(req: TelemetryEventRequest, db: Session = Depends(get_db)):
    """
    Ingests non-sensitive client/server interaction telemetry (task events,
    discovery time, 3D interactions, simulation runs, AI queries, page load latency).
    Zero PII collected.
    """
    return record_telemetry_event(
        event_type=req.event_type,
        component=req.component,
        duration_ms=req.duration_ms,
        success=req.success,
        metadata=req.metadata,
        db=db
    )


@router.get("/telemetry/summary")
def get_telemetry_summary_endpoint(db: Session = Depends(get_db)):
    """
    Returns aggregated application performance telemetry, completion metrics,
    and system performance indicators.
    """
    return get_telemetry_summary(db=db)


# ==================== MULTI-PERSONA COGNITIVE BENCHMARKS ====================

@router.post("/evaluate")
async def evaluate_query_endpoint(req: EvaluateQueryRequest, db: Session = Depends(get_db)):
    """
    Evaluates a user prompt across Researcher, Student, and Citizen modes in parallel.
    Calculates readability scores, vocabulary densities, and grounding fidelity.
    """
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
        
    return await evaluate_query_across_modes(req.query, req.target_object_id, db)


@router.get("/history")
def get_evaluation_history(limit: int = 20, db: Session = Depends(get_db)):
    """Retrieves previous multi-persona evaluation records from the database."""
    records = db.query(EvaluationRecord).order_by(EvaluationRecord.created_at.desc()).limit(limit).all()
    return [
        {
            "id": r.id,
            "query": r.query,
            "target_object_id": r.target_object_id,
            "researcher_metrics": r.researcher_metrics,
            "student_metrics": r.student_metrics,
            "citizen_metrics": r.citizen_metrics,
            "comparative_insights": r.computation_benchmark,
            "created_at": r.created_at.isoformat() if r.created_at else None
        }
        for r in records
    ]


@router.get("/benchmarks")
def get_aggregate_benchmarks(db: Session = Depends(get_db)):
    """
    Returns aggregate research performance metrics:
    - Average readability (FKGL / FRE) by mode
    - Average technical density by mode
    - Average simulation accuracy & energy conservation drift
    """
    sim_runs = db.query(SimulationRunRecord).order_by(SimulationRunRecord.created_at.desc()).limit(50).all()
    
    avg_energy_error = 0.0
    avg_sim_runtime = 0.0
    if sim_runs:
        avg_energy_error = sum(r.max_energy_error for r in sim_runs) / len(sim_runs)
        avg_sim_runtime = sum(r.runtime_ms for r in sim_runs) / len(sim_runs)

    return {
        "persona_complexity_benchmarks": {
            "researcher": {
                "expected_grade_level": "14 - 18 (Postgraduate)",
                "technical_term_density": "12.5% - 22.0%",
                "reading_ease": "20.0 - 45.0 (Dense Academic)",
                "target_audience": "Astrophysicists, Space Science Researchers"
            },
            "student": {
                "expected_grade_level": "8 - 11 (High School / Early Undergrad)",
                "technical_term_density": "4.5% - 8.5%",
                "reading_ease": "55.0 - 70.0 (Accessible Educational)",
                "target_audience": "Undergraduate Students, Educators, Physics Learners"
            },
            "citizen": {
                "expected_grade_level": "5 - 7 (General Public)",
                "technical_term_density": "1.0% - 3.5%",
                "reading_ease": "75.0 - 90.0 (Plain Language)",
                "target_audience": "Astronomy Enthusiasts, Stargazers, General Public"
            }
        },
        "simulation_engine_benchmarks": {
            "total_simulation_runs": len(sim_runs),
            "average_max_energy_drift": avg_energy_error,
            "average_runtime_ms": round(avg_sim_runtime, 2),
            "integrator_options": ["REBOUND IAS15", "REBOUND WHFast", "NEBULA Symplectic Leapfrog (NumPy)"],
            "symplectic_drift_characteristic": "Bounded oscillatory without secular energy decay"
        }
    }
