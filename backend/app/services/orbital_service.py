from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.data.catalog import get_object_by_id
from app.scientific.orbital_mechanics import (
    calculate_hohmann_transfer,
    calculate_hill_sphere,
    calculate_roche_limit,
    find_orbital_resonances,
    calculate_lagrange_points,
    M_SUN
)
from app.core.exceptions import ScientificCalculationError, AstronomicalObjectNotFoundError

class OrbitalService:
    @staticmethod
    def calculate_hohmann(
        db: Session,
        origin_id: Optional[str] = None,
        target_id: Optional[str] = None,
        r1_au: Optional[float] = None,
        r2_au: Optional[float] = None
    ) -> Dict[str, Any]:
        origin_name = "Origin Orbit"
        target_name = "Target Orbit"

        if origin_id:
            obj1 = get_object_by_id(db, origin_id)
            if not obj1:
                raise AstronomicalObjectNotFoundError(origin_id)
            if obj1.get("semi_major_axis_au"):
                r1_au = obj1["semi_major_axis_au"]
                origin_name = obj1["name"]

        if target_id:
            obj2 = get_object_by_id(db, target_id)
            if not obj2:
                raise AstronomicalObjectNotFoundError(target_id)
            if obj2.get("semi_major_axis_au"):
                r2_au = obj2["semi_major_axis_au"]
                target_name = obj2["name"]

        if not r1_au or not r2_au or r1_au <= 0 or r2_au <= 0:
            raise ScientificCalculationError("Semi-major axes must be strictly positive numerical values.")
        if r1_au == r2_au:
            raise ScientificCalculationError("Origin and target orbits cannot have the exact same radius.")

        res = calculate_hohmann_transfer(r1_au, r2_au)
        return {
            "origin_name": origin_name,
            "target_name": target_name,
            **res
        }

    @staticmethod
    def calculate_hill_sphere(
        db: Session,
        object_id: Optional[str] = None,
        semi_major_axis_au: Optional[float] = None,
        eccentricity: Optional[float] = 0.0,
        body_mass_kg: Optional[float] = None,
        parent_mass_kg: Optional[float] = M_SUN
    ) -> Dict[str, Any]:
        if object_id:
            obj = get_object_by_id(db, object_id)
            if obj:
                semi_major_axis_au = obj.get("semi_major_axis_au", semi_major_axis_au)
                eccentricity = obj.get("eccentricity", eccentricity)
                body_mass_kg = obj.get("mass_kg", body_mass_kg)

        if not semi_major_axis_au or not body_mass_kg or semi_major_axis_au <= 0 or body_mass_kg <= 0:
            raise ScientificCalculationError("Requires strictly positive semi_major_axis_au and body_mass_kg.")

        return calculate_hill_sphere(semi_major_axis_au, eccentricity or 0.0, body_mass_kg, parent_mass_kg or M_SUN)

    @staticmethod
    def calculate_roche_limit(primary_radius_km: float, primary_density: float, secondary_density: float) -> Dict[str, Any]:
        return calculate_roche_limit(primary_radius_km, primary_density, secondary_density)

    @staticmethod
    def calculate_resonances(period_1_days: float, period_2_days: float, max_order: int = 8) -> Dict[str, Any]:
        matches = find_orbital_resonances(period_1_days, period_2_days, max_order)
        return {
            "period_1_days": period_1_days,
            "period_2_days": period_2_days,
            "resonances_found": matches,
            "has_resonance": len(matches) > 0
        }

    @staticmethod
    def calculate_lagrange(primary_mass_kg: float, secondary_mass_kg: float, separation_au: float) -> Dict[str, Any]:
        return calculate_lagrange_points(primary_mass_kg, secondary_mass_kg, separation_au)

orbital_service = OrbitalService()
