from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class EvaluateQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Prompt query to evaluate across personas")
    target_object_id: Optional[str] = None

class ModeEvaluationMetrics(BaseModel):
    flesch_kincaid_grade: float
    flesch_reading_ease: float
    technical_term_density_percent: float
    char_count: int
    word_count: int
    sentence_count: int
    grounding_score_percent: float
    response_sample: str

class ResearchEvaluationResultSchema(BaseModel):
    query: str
    target_object_id: Optional[str]
    researcher: ModeEvaluationMetrics
    student: ModeEvaluationMetrics
    citizen: ModeEvaluationMetrics
    comparative_insights: Dict[str, Any]
