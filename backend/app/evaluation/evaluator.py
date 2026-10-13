"""
Evaluation Orchestrator for NEBULA.
Runs multi-persona comparative evaluations and computes comparative metrics.
"""
import uuid
import time
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.ai.service import ai_service
from app.evaluation.metrics import compute_text_readability, compute_grounding_score
from app.ai.grounding import extract_grounding_context
from app.db.models import EvaluationRecord

async def evaluate_query_across_modes(
    query: str,
    target_object_id: Optional[str] = None,
    db: Optional[Session] = None
) -> Dict[str, Any]:
    """
    Executes the query across Researcher, Student, and Citizen modes simultaneously.
    Computes quantitative cognitive load and scientific metrics side-by-side.
    """
    grounding_str, grounding_meta = extract_grounding_context(query, target_object_id)

    # Run all 3 personas
    t0 = time.perf_counter()
    res_researcher = await ai_service.chat(query, mode="researcher", target_object_id=target_object_id)
    t_res = (time.perf_counter() - t0) * 1000.0

    t0 = time.perf_counter()
    res_student = await ai_service.chat(query, mode="student", target_object_id=target_object_id)
    t_stu = (time.perf_counter() - t0) * 1000.0

    t0 = time.perf_counter()
    res_citizen = await ai_service.chat(query, mode="citizen", target_object_id=target_object_id)
    t_cit = (time.perf_counter() - t0) * 1000.0

    # Analyze texts
    read_res = compute_text_readability(res_researcher["response"])
    read_stu = compute_text_readability(res_student["response"])
    read_cit = compute_text_readability(res_citizen["response"])

    ground_res = compute_grounding_score(res_researcher["response"], grounding_meta["data_points"])
    ground_stu = compute_grounding_score(res_student["response"], grounding_meta["data_points"])
    ground_cit = compute_grounding_score(res_citizen["response"], grounding_meta["data_points"])

    researcher_metrics = {
        **read_res,
        **ground_res,
        "latency_ms": round(t_res, 1),
        "response_sample": res_researcher["response"]
    }

    student_metrics = {
        **read_stu,
        **ground_stu,
        "latency_ms": round(t_stu, 1),
        "response_sample": res_student["response"]
    }

    citizen_metrics = {
        **read_cit,
        **ground_cit,
        "latency_ms": round(t_cit, 1),
        "response_sample": res_citizen["response"]
    }

    eval_id = str(uuid.uuid4())[:8]

    # Comparative synthesis
    result = {
        "evaluation_id": eval_id,
        "query": query,
        "target_object_id": target_object_id,
        "grounding_summary": grounding_meta,
        "researcher": researcher_metrics,
        "student": student_metrics,
        "citizen": citizen_metrics,
        "comparative_insights": {
            "grade_level_contrast": f"Researcher grade {read_res['flesch_kincaid_grade']} vs Citizen grade {read_cit['flesch_kincaid_grade']} (Δ = {round(read_res['flesch_kincaid_grade'] - read_cit['flesch_kincaid_grade'], 1)} grades)",
            "technical_density_contrast": f"Researcher term density {read_res['technical_term_density_percent']}% vs Citizen {read_cit['technical_term_density_percent']}%",
            "reading_ease_contrast": f"Citizen reading ease {read_cit['flesch_reading_ease']} (accessible) vs Researcher {read_res['flesch_reading_ease']} (dense)",
            "math_density_contrast": f"Researcher math formulas: {read_res['math_expressions_count']} vs Student: {read_stu['math_expressions_count']} vs Citizen: {read_cit['math_expressions_count']}"
        }
    }

    # Store in database if session provided
    if db:
        try:
            record = EvaluationRecord(
                id=eval_id,
                query=query,
                target_object_id=target_object_id,
                researcher_metrics=researcher_metrics,
                student_metrics=student_metrics,
                citizen_metrics=citizen_metrics,
                computation_benchmark=result["comparative_insights"]
            )
            db.add(record)
            db.commit()
        except Exception:
            pass

    return result
