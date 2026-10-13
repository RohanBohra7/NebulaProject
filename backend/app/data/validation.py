"""
Data Quality & Astropy Physical Validation Engine for NEBULA.
Performs dimensional checks, bounds validation, unit verification, and physical consistency verification.
"""
import math
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import astropy.units as u
from astropy.constants import G

G_SI = G.value # 6.6743e-11 m^3 / (kg s^2)

class FieldValidationIssue(BaseModel):
    field: str
    issue_type: str # "error" | "warning" | "info"
    message: str
    value: Optional[Any] = None

class ObjectValidationResult(BaseModel):
    object_id: str
    name: str
    category: str
    is_valid: bool
    issues: List[FieldValidationIssue]
    physical_consistency_score: float # 0 - 100

class DataQualityReport(BaseModel):
    total_objects_inspected: int
    objects_valid: int
    objects_with_warnings: int
    total_errors: int
    total_warnings: int
    quality_score_percent: float
    units_validated: List[str]
    object_results: List[ObjectValidationResult]
    duplicate_ids: List[str]
    unresolved_parent_ids: List[str]

SLUG_PATTERN = re.compile(r'^[a-z0-9_\-]+$')

VALID_SCIENTIFIC_UNITS = {
    "mass": ["kg", "g", "M_earth", "M_sun", "M_jup"],
    "radius": ["km", "m", "R_earth", "R_sun", "R_jup"],
    "gravity": ["m/s²", "m/s^2", "gees", "g"],
    "distance_from_sun": ["AU", "au", "km", "pc", "ly"],
    "orbital_period": ["days", "d", "years", "yr", "hours", "h"],
    "rotation_period": ["hours", "h", "days", "d"],
    "orbital_velocity": ["km/s", "m/s"],
    "temperature": ["K", "kelvin", "°C", "C"]
}

def validate_celestial_object(obj: Dict[str, Any]) -> ObjectValidationResult:
    issues: List[FieldValidationIssue] = []
    obj_id = str(obj.get("id", "")).strip()
    name = str(obj.get("name", "")).strip()
    category = str(obj.get("object_type") or obj.get("category", "Generic")).strip()
    description = obj.get("description") or obj.get("description_citizen") or obj.get("description_student")

    # 1. ID checks
    if not obj_id:
        issues.append(FieldValidationIssue(field="id", issue_type="error", message="Object ID cannot be empty."))
    elif not SLUG_PATTERN.match(obj_id):
        issues.append(FieldValidationIssue(
            field="id", issue_type="error",
            message=f"Object ID '{obj_id}' must be a lowercase URL-safe slug containing only letters, numbers, and hyphens.",
            value=obj_id
        ))

    # 2. Name check
    if not name:
        issues.append(FieldValidationIssue(field="name", issue_type="error", message="Object name cannot be empty."))

    # 3. Description check
    if not description:
        issues.append(FieldValidationIssue(field="description", issue_type="warning", message="Object description is missing."))

    # Helper to check float validity
    def check_number(val, field_name: str) -> Optional[float]:
        if val is None:
            return None
        if not isinstance(val, (int, float)):
            try:
                val = float(val)
            except (ValueError, TypeError):
                issues.append(FieldValidationIssue(
                    field=field_name, issue_type="error",
                    message=f"Field '{field_name}' must be a numeric value, got '{type(val).__name__}'.",
                    value=val
                ))
                return None
        if math.isnan(val) or math.isinf(val):
            issues.append(FieldValidationIssue(
                field=field_name, issue_type="error",
                message=f"Field '{field_name}' cannot be NaN or infinite.",
                value=val
            ))
            return None
        return float(val)

    # 4. Numeric bounds & Astropy unit validation
    mass_kg = check_number(obj.get("mass_kg") if obj.get("mass_kg") is not None else obj.get("mass"), "mass_kg")
    if mass_kg is not None:
        if mass_kg <= 0:
            issues.append(FieldValidationIssue(field="mass_kg", issue_type="error", message="Mass must be strictly positive.", value=mass_kg))
        else:
            try:
                _ = (mass_kg * u.kg).to(u.g)
            except Exception as e:
                issues.append(FieldValidationIssue(field="mass_kg", issue_type="error", message=f"Unit validation failed: {e}", value=mass_kg))

    radius_km = check_number(obj.get("radius_km") if obj.get("radius_km") is not None else obj.get("radius"), "radius_km")
    if radius_km is not None:
        if radius_km <= 0:
            issues.append(FieldValidationIssue(field="radius_km", issue_type="error", message="Radius must be strictly positive.", value=radius_km))
        else:
            try:
                _ = (radius_km * u.km).to(u.m)
            except Exception as e:
                issues.append(FieldValidationIssue(field="radius_km", issue_type="error", message=f"Unit validation failed: {e}", value=radius_km))

    gravity_val = check_number(obj.get("surface_gravity_m_s2") if obj.get("surface_gravity_m_s2") is not None else obj.get("gravity"), "surface_gravity_m_s2")
    if gravity_val is not None and gravity_val < 0:
        issues.append(FieldValidationIssue(field="surface_gravity_m_s2", issue_type="error", message="Surface gravity cannot be negative.", value=gravity_val))

    temp_k = check_number(obj.get("surface_temperature_k") if obj.get("surface_temperature_k") is not None else obj.get("temperature"), "surface_temperature_k")
    if temp_k is not None:
        if temp_k <= 0:
            issues.append(FieldValidationIssue(
                field="surface_temperature_k", issue_type="error",
                message="Surface temperature must be strictly positive (violates Third Law of Thermodynamics).",
                value=temp_k
            ))

    ecc = check_number(obj.get("eccentricity"), "eccentricity")
    if ecc is not None:
        if ecc < 0:
            issues.append(FieldValidationIssue(field="eccentricity", issue_type="error", message="Eccentricity cannot be negative.", value=ecc))
        elif ecc >= 1.0 and category in ["Planet", "Moon"]:
            issues.append(FieldValidationIssue(
                field="eccentricity", issue_type="warning",
                message=f"Eccentricity {ecc} indicates a parabolic/hyperbolic unbound orbit for a {category}.",
                value=ecc
            ))

    semi_major = check_number(obj.get("semi_major_axis_au") if obj.get("semi_major_axis_au") is not None else obj.get("distance_from_sun"), "semi_major_axis_au")
    if semi_major is not None:
        if semi_major < 0:
            issues.append(FieldValidationIssue(field="semi_major_axis_au", issue_type="error", message="Semi-major axis cannot be negative.", value=semi_major))
        elif semi_major == 0.0 and category in ["Planet", "Moon", "Exoplanet", "Asteroid", "Comet"]:
            issues.append(FieldValidationIssue(field="semi_major_axis_au", issue_type="error", message=f"{category} must have a positive non-zero semi-major axis.", value=semi_major))

    period_days = check_number(obj.get("orbital_period_days") if obj.get("orbital_period_days") is not None else obj.get("orbital_period"), "orbital_period_days")
    if period_days is not None:
        if period_days < 0:
            issues.append(FieldValidationIssue(field="orbital_period_days", issue_type="error", message="Orbital period cannot be negative.", value=period_days))
        elif period_days == 0.0 and category in ["Planet", "Moon", "Exoplanet", "Asteroid", "Comet"]:
            issues.append(FieldValidationIssue(field="orbital_period_days", issue_type="error", message=f"{category} must have a positive non-zero orbital period.", value=period_days))

    # 5. Units dictionary validation
    units_dict = obj.get("units")
    if units_dict is not None:
        if not isinstance(units_dict, dict):
            issues.append(FieldValidationIssue(field="units", issue_type="error", message="Units field must be a dictionary mapping field names to unit strings."))
        else:
            for u_field, u_unit in units_dict.items():
                if u_field in VALID_SCIENTIFIC_UNITS:
                    allowed = VALID_SCIENTIFIC_UNITS[u_field]
                    if u_unit not in allowed:
                        issues.append(FieldValidationIssue(
                            field=f"units.{u_field}", issue_type="warning",
                            message=f"Unit '{u_unit}' for '{u_field}' is non-standard. Expected one of: {allowed}.",
                            value=u_unit
                        ))

    # 6. Physical Consistency checks
    consistency_score = 100.0

    # Theoretical density check: rho = M / (4/3 * pi * R^3)
    if mass_kg and radius_km and mass_kg > 0 and radius_km > 0:
        vol_cm3 = (4.0 / 3.0) * math.pi * ((radius_km * 1e5) ** 3)
        theo_density_g_cm3 = (mass_kg * 1000.0) / vol_cm3
        stated_density = obj.get("mean_density_g_cm3")
        if stated_density and stated_density > 0:
            discrepancy = abs(theo_density_g_cm3 - stated_density) / stated_density * 100.0
            if discrepancy > 35.0:
                issues.append(FieldValidationIssue(
                    field="mean_density_g_cm3", issue_type="warning",
                    message=f"Discrepancy of {round(discrepancy, 1)}% between stated density ({stated_density} g/cm³) and spherical volume calculated density ({round(theo_density_g_cm3, 2)} g/cm³).",
                    value=stated_density
                ))
                consistency_score -= 10.0

        # Theoretical gravity check: g = G * M / R^2
        r_m = radius_km * 1000.0
        theo_g_m_s2 = (G_SI * mass_kg) / (r_m ** 2)
        stated_g = obj.get("surface_gravity_m_s2") if obj.get("surface_gravity_m_s2") is not None else obj.get("gravity")
        if stated_g and stated_g > 0:
            discrepancy_g = abs(theo_g_m_s2 - stated_g) / stated_g * 100.0
            if discrepancy_g > 25.0:
                issues.append(FieldValidationIssue(
                    field="surface_gravity_m_s2", issue_type="warning",
                    message=f"Discrepancy of {round(discrepancy_g, 1)}% between stated gravity ({stated_g} m/s²) and Newtonian calculated gravity ({round(theo_g_m_s2, 2)} m/s²).",
                    value=stated_g
                ))
                consistency_score -= 10.0

    has_errors = any(i.issue_type == "error" for i in issues)
    consistency_score = max(0.0, min(100.0, consistency_score))

    return ObjectValidationResult(
        object_id=obj_id,
        name=name,
        category=category,
        is_valid=not has_errors,
        issues=issues,
        physical_consistency_score=round(consistency_score, 1)
    )

def validate_catalog(objects: List[Dict[str, Any]]) -> DataQualityReport:
    """
    Validates entire astronomical dataset, detecting duplicate IDs,
    broken parent hierarchy links, and physical parameter issues.
    """
    seen_ids = set()
    duplicate_ids = []
    all_ids = set()

    for o in objects:
        oid = o.get("id")
        if oid:
            if oid in seen_ids:
                duplicate_ids.append(oid)
            seen_ids.add(oid)
            all_ids.add(oid)

    unresolved_parents = []
    for o in objects:
        parent_id = o.get("parent_object") or o.get("parent_body_id")
        if parent_id and parent_id not in all_ids:
            unresolved_parents.append(f"{o.get('id')} -> {parent_id}")

    results: List[ObjectValidationResult] = []
    total_errors = len(duplicate_ids)
    total_warnings = len(unresolved_parents)

    for o in objects:
        res = validate_celestial_object(o)
        for issue in res.issues:
            if issue.issue_type == "error":
                total_errors += 1
            elif issue.issue_type == "warning":
                total_warnings += 1
        results.append(res)

    valid_count = sum(1 for r in results if r.is_valid)
    warning_count = sum(1 for r in results if any(i.issue_type == "warning" for i in r.issues))
    
    total_objs = len(objects)
    score = ((valid_count / total_objs) * 100.0) if total_objs > 0 else 100.0
    if total_warnings > 0:
        score = max(0.0, score - (total_warnings * 0.5))

    return DataQualityReport(
        total_objects_inspected=total_objs,
        objects_valid=valid_count,
        objects_with_warnings=warning_count,
        total_errors=total_errors,
        total_warnings=total_warnings,
        quality_score_percent=round(score, 1),
        units_validated=["kg (mass)", "km (radius)", "AU (distance)", "days (orbital period)", "hours (rotation)", "K (temperature)", "m/s² (gravity)", "g/cm³ (density)"],
        object_results=results,
        duplicate_ids=duplicate_ids,
        unresolved_parent_ids=unresolved_parents
    )
