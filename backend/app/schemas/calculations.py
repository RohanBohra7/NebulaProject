from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

M_SUN = 1.98847e30

class HohmannRequest(BaseModel):
    origin_id: Optional[str] = None
    target_id: Optional[str] = None
    r1_au: Optional[float] = None
    r2_au: Optional[float] = None

class HillSphereRequest(BaseModel):
    object_id: Optional[str] = None
    semi_major_axis_au: Optional[float] = None
    eccentricity: Optional[float] = 0.0
    body_mass_kg: Optional[float] = None
    parent_mass_kg: Optional[float] = M_SUN

class RocheLimitRequest(BaseModel):
    primary_radius_km: float = Field(..., gt=0, description="Primary body radius in km")
    primary_density_g_cm3: float = Field(..., gt=0, description="Primary body density in g/cm³")
    secondary_density_g_cm3: float = Field(..., gt=0, description="Secondary body density in g/cm³")

class ResonanceRequest(BaseModel):
    period_days_1: float = Field(..., gt=0, description="Orbital period of inner body in days")
    period_days_2: float = Field(..., gt=0, description="Orbital period of outer body in days")
    max_order: int = Field(8, gt=0, le=20, description="Maximum resonant harmonic order")

class LagrangeRequest(BaseModel):
    primary_mass_kg: float = Field(M_SUN, gt=0, description="Primary body mass in kg")
    secondary_mass_kg: float = Field(..., gt=0, description="Secondary body mass in kg")
    separation_au: float = Field(..., gt=0, description="Orbital separation in AU")
