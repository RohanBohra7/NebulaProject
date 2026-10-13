"""
Data Grounding Engine for NEBULA AI Services.
Extracts empirical astronomical parameters and real-time scientific calculations
to ground all AI responses in factual truth and prevent hallucinations.
"""
from typing import Dict, Any, List, Optional, Tuple
from app.data.seed_data import ASTRONOMICAL_CATALOG
from app.scientific import (
    calculate_hohmann_transfer,
    calculate_hill_sphere,
    calculate_roche_limit,
    find_orbital_resonances
)

def find_referenced_objects(query: str, target_object_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Finds celestial objects mentioned in the query or explicitly specified by target_object_id.
    """
    found = []
    seen_ids = set()

    # If target_object_id is specified
    if target_object_id:
        for obj in ASTRONOMICAL_CATALOG:
            if obj["id"] == target_object_id:
                found.append(obj)
                seen_ids.add(obj["id"])
                break

    query_lower = query.lower()
    for obj in ASTRONOMICAL_CATALOG:
        if obj["id"] in seen_ids:
            continue
        # Check by ID or name tokens
        name_clean = obj["name"].lower().split("(")[0].strip()
        if obj["id"] in query_lower or name_clean in query_lower:
            found.append(obj)
            seen_ids.add(obj["id"])

    return found


def extract_grounding_context(query: str, target_object_id: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
    """
    Constructs a detailed scientific context block and metadata payload for grounding.
    """
    objects = find_referenced_objects(query, target_object_id)
    grounded_data_points = []
    context_lines = ["### GROUNDED ASTRONOMICAL DATA FOUNDATION:"]

    if objects:
        for obj in objects:
            context_lines.append(f"Celestial Object: {obj['name']} (Category: {obj['category']})")
            if obj.get("mass_kg"):
                context_lines.append(f"- Mass: {obj['mass_kg']} kg ({obj.get('mass_earth_relative')} Earth masses)")
                grounded_data_points.append({"property": "mass", "value": obj['mass_kg'], "unit": "kg"})
            if obj.get("radius_km"):
                context_lines.append(f"- Radius: {obj['radius_km']} km ({obj.get('radius_earth_relative')} Earth radii)")
                grounded_data_points.append({"property": "radius", "value": obj['radius_km'], "unit": "km"})
            if obj.get("semi_major_axis_au"):
                context_lines.append(f"- Semi-Major Axis (a): {obj['semi_major_axis_au']} AU")
                grounded_data_points.append({"property": "semi_major_axis", "value": obj['semi_major_axis_au'], "unit": "AU"})
            if obj.get("orbital_period_days"):
                context_lines.append(f"- Orbital Period: {obj['orbital_period_days']} Earth days")
                grounded_data_points.append({"property": "period", "value": obj['orbital_period_days'], "unit": "days"})
            if obj.get("eccentricity") is not None:
                context_lines.append(f"- Orbital Eccentricity (e): {obj['eccentricity']}")
            if obj.get("surface_gravity_m_s2"):
                context_lines.append(f"- Surface Gravity: {obj['surface_gravity_m_s2']} m/s²")
            if obj.get("escape_velocity_km_s"):
                context_lines.append(f"- Escape Velocity: {obj['escape_velocity_km_s']} km/s")
            if obj.get("surface_temperature_k"):
                context_lines.append(f"- Surface/Equilibrium Temperature: {obj['surface_temperature_k']} K")
            if obj.get("mean_density_g_cm3"):
                context_lines.append(f"- Mean Density: {obj['mean_density_g_cm3']} g/cm³")
            if obj.get("data_source"):
                context_lines.append(f"- Data Provenance: {obj['data_source']}")

            # Run dynamic physical calculations if suitable
            if obj.get("semi_major_axis_au") and obj.get("mass_kg") and obj["category"] in ["Planet", "Exoplanet"]:
                hill = calculate_hill_sphere(obj["semi_major_axis_au"], obj.get("eccentricity", 0.0), obj["mass_kg"])
                context_lines.append(f"- Calculated Hill Sphere Radius: {hill['hill_radius_km']} km ({hill['hill_radius_au']} AU)")
                grounded_data_points.append({"property": "hill_sphere_km", "value": hill["hill_radius_km"], "unit": "km"})

    # Check for Hohmann transfer queries between two objects (e.g., Earth to Mars)
    query_lower = query.lower()
    if ("transfer" in query_lower or "hohmann" in query_lower or "travel" in query_lower) and len(objects) >= 2:
        o1, o2 = objects[0], objects[1]
        if o1.get("semi_major_axis_au") and o2.get("semi_major_axis_au"):
            hohmann = calculate_hohmann_transfer(o1["semi_major_axis_au"], o2["semi_major_axis_au"])
            context_lines.append(f"\n### REAL-TIME HOHMANN TRANSFER TRAJECTORY ({o1['name']} -> {o2['name']}):")
            context_lines.append(f"- Delta-v Burn 1: {hohmann['delta_v1_km_s']} km/s")
            context_lines.append(f"- Delta-v Burn 2: {hohmann['delta_v2_km_s']} km/s")
            context_lines.append(f"- Total Delta-v: {hohmann['total_delta_v_km_s']} km/s")
            context_lines.append(f"- One-way Transfer Time: {hohmann['transfer_time_days']} Earth days")
            grounded_data_points.append({"property": "hohmann_total_dv", "value": hohmann["total_delta_v_km_s"], "unit": "km/s"})
            grounded_data_points.append({"property": "hohmann_transfer_days", "value": hohmann["transfer_time_days"], "unit": "days"})

    context_str = "\n".join(context_lines)
    metadata = {
        "grounded_objects": [o["name"] for o in objects],
        "grounded_points_count": len(grounded_data_points),
        "data_points": grounded_data_points,
        "is_grounded": len(grounded_data_points) > 0
    }

    return context_str, metadata
