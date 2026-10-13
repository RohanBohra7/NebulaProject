"""
Pydantic Schemas for NEBULA N-Body Simulation Engine.
Strict typing for simulation specifications, lifecycle responses,
detailed trajectory telemetry, pairwise distances, and reproducibility.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class CustomBodyInput(BaseModel):
    id: Optional[str] = None
    name: str
    mass: float = Field(..., ge=0, description="Mass in solar masses (M_sun)")
    x: float = Field(..., description="Initial X position in AU")
    y: float = Field(..., description="Initial Y position in AU")
    z: float = Field(0.0, description="Initial Z position in AU")
    vx: float = Field(0.0, description="Initial Vx velocity in AU/year")
    vy: float = Field(0.0, description="Initial Vy velocity in AU/year")
    vz: float = Field(0.0, description="Initial Vz velocity in AU/year")
    color: Optional[str] = "#38bdf8"
    radius_km: Optional[float] = None
    radius_display: Optional[float] = 1.0


class CreateSimulationRequest(BaseModel):
    scenario_id: str = Field("sun_earth", description="Identifier of the scenario")
    duration: Optional[float] = Field(None, gt=0, le=100.0, description="Simulation duration in years")
    timestep: Optional[float] = Field(None, gt=0, description="Timestep in years")
    num_steps: int = Field(150, ge=5, le=1000, description="Number of output sampling steps")
    integrator: str = Field("ias15", description="Integrator: ias15, whfast, or leapfrog")
    selected_bodies: Optional[List[str]] = Field(None, description="Subset of body IDs to simulate")
    custom_bodies: Optional[List[Dict[str, Any]]] = Field(None, description="Optional custom initial bodies")
    auto_run: bool = Field(True, description="Whether to execute the simulation immediately upon creation")


class RunSimulationRequest(BaseModel):
    scenario_id: str = Field("sun_earth", description="Identifier of scenario")
    integrator: str = Field("ias15", description="Integrator algorithm: ias15, whfast, or leapfrog")
    total_time_years: Optional[float] = Field(None, gt=0, le=100.0, description="Duration in Earth years")
    duration: Optional[float] = Field(None, gt=0, le=100.0, description="Alias for total_time_years")
    timestep: Optional[float] = Field(None, gt=0, description="Timestep in years")
    num_steps: int = Field(150, ge=5, le=1000, description="Sample steps to record")
    selected_bodies: Optional[List[str]] = None
    custom_bodies: Optional[List[Dict[str, Any]]] = None


class SimulationSummaryResponse(BaseModel):
    id: str
    scenario_id: str
    status: str = Field(..., description="'created', 'running', 'completed', 'stopped', or 'failed'")
    created_at: str
    completed_at: Optional[str] = None
    parameters: Dict[str, Any]
    has_results: bool
    error: Optional[str] = None


class SimulationBodyOutput(BaseModel):
    id: str
    name: str
    mass: float
    radius_km: Optional[float] = None
    color: str
    radius_display: float
    initial_position: List[float]
    initial_velocity: List[float]
    final_position: List[float]
    final_velocity: List[float]
    positions: List[List[float]]
    velocities: List[List[float]]
    speeds: List[float]
    distances_from_center: List[float]
    trajectory: List[List[float]]


class EnergyDriftPoint(BaseModel):
    time: float
    energy: float
    kinetic: float
    potential: float
    energy_error: float


class PairwiseDistancePoint(BaseModel):
    pair_id: str
    pair_name: str
    body1_id: str
    body2_id: str
    min_distance: float
    max_distance: float
    series: List[Dict[str, Any]]


class SimulationFullResult(BaseModel):
    engine_used: str
    integrator: str
    runtime_ms: float
    steps_computed: int
    total_time_years: float
    times: List[float]
    max_energy_error: float
    initial_energy: float
    final_energy: float
    angular_momentum_initial: List[float]
    angular_momentum_final: List[float]
    bodies: List[SimulationBodyOutput]
    pairwise_distances: List[PairwiseDistancePoint]
    energy_drift_series: List[EnergyDriftPoint]
    reproducibility: Dict[str, Any]

# Aliases for backward compatibility
SimulationResultSchema = SimulationFullResult
ParticleState = SimulationBodyOutput

