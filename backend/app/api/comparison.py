from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.data.catalog import get_object_by_id
from app.schemas.celestial import CompareRequest, DetailedComparisonResponse

router = APIRouter(prefix="/compare", tags=["Object Comparison"])

@router.post("/", response_model=DetailedComparisonResponse)
def compare_astronomical_objects(req: CompareRequest, db: Session = Depends(get_db)):
    """
    Compares 2-6 astronomical objects side-by-side with calculated ratios,
    absolute/percentage differences, radar charts, and persona-tailored scientific insights.
    """
    if len(req.object_ids) < 2:
        raise HTTPException(status_code=400, detail="Provide at least 2 object IDs for comparison.")
    if len(req.object_ids) > 6:
        raise HTTPException(status_code=400, detail="Maximum 6 objects can be compared simultaneously.")

    objects = []
    for oid in req.object_ids:
        obj = get_object_by_id(db, oid)
        if obj:
            objects.append(obj)
        else:
            raise HTTPException(status_code=404, detail=f"Object '{oid}' not found.")

    primary = objects[0]
    ratios = []
    absolute_differences = []

    # Calculate ratios and deltas relative to primary object
    for obj in objects[1:]:
        mass_ratio = (obj["mass_kg"] / primary["mass_kg"]) if (obj.get("mass_kg") and primary.get("mass_kg")) else None
        radius_ratio = (obj["radius_km"] / primary["radius_km"]) if (obj.get("radius_km") and primary.get("radius_km")) else None
        gravity_ratio = (obj["surface_gravity_m_s2"] / primary["surface_gravity_m_s2"]) if (obj.get("surface_gravity_m_s2") and primary.get("surface_gravity_m_s2")) else None
        density_ratio = (obj["mean_density_g_cm3"] / primary["mean_density_g_cm3"]) if (obj.get("mean_density_g_cm3") and primary.get("mean_density_g_cm3")) else None
        period_ratio = (obj["orbital_period_days"] / primary["orbital_period_days"]) if (obj.get("orbital_period_days") and primary.get("orbital_period_days")) else None
        temp_ratio = (obj["surface_temperature_k"] / primary["surface_temperature_k"]) if (obj.get("surface_temperature_k") and primary.get("surface_temperature_k")) else None
        
        prim_dist = primary.get("semi_major_axis_au") if primary.get("semi_major_axis_au") is not None else primary.get("distance_from_sun")
        obj_dist = obj.get("semi_major_axis_au") if obj.get("semi_major_axis_au") is not None else obj.get("distance_from_sun")
        distance_ratio = (obj_dist / prim_dist) if (obj_dist and prim_dist and prim_dist != 0) else None

        prim_vel = primary.get("mean_orbital_velocity_km_s") if primary.get("mean_orbital_velocity_km_s") is not None else primary.get("orbital_velocity")
        obj_vel = obj.get("mean_orbital_velocity_km_s") if obj.get("mean_orbital_velocity_km_s") is not None else obj.get("orbital_velocity")
        velocity_ratio = (obj_vel / prim_vel) if (obj_vel and prim_vel and prim_vel != 0) else None

        ratios.append({
            "target_id": obj["id"],
            "target_name": obj["name"],
            "relative_to": primary["name"],
            "mass_ratio": round(mass_ratio, 4) if mass_ratio else None,
            "radius_ratio": round(radius_ratio, 4) if radius_ratio else None,
            "gravity_ratio": round(gravity_ratio, 4) if gravity_ratio else None,
            "density_ratio": round(density_ratio, 4) if density_ratio else None,
            "period_ratio": round(period_ratio, 4) if period_ratio else None,
            "temperature_ratio": round(temp_ratio, 4) if temp_ratio else None,
            "distance_ratio": round(distance_ratio, 4) if distance_ratio else None,
            "velocity_ratio": round(velocity_ratio, 4) if velocity_ratio else None,
        })

        # Absolute numerical and percentage differences
        def calc_delta(val_target, val_prim):
            if val_target is not None and val_prim is not None:
                delta = val_target - val_prim
                pct = (delta / val_prim * 100.0) if val_prim != 0 else None
                return round(delta, 3), round(pct, 1) if pct is not None else None
            return None, None

        m_delta, m_pct = calc_delta(obj.get("mass_earth_relative"), primary.get("mass_earth_relative"))
        r_delta, r_pct = calc_delta(obj.get("radius_km"), primary.get("radius_km"))
        g_delta, g_pct = calc_delta(obj.get("surface_gravity_m_s2"), primary.get("surface_gravity_m_s2"))
        d_delta, d_pct = calc_delta(obj.get("mean_density_g_cm3"), primary.get("mean_density_g_cm3"))
        t_delta, t_pct = calc_delta(obj.get("surface_temperature_k"), primary.get("surface_temperature_k"))
        dist_delta, dist_pct = calc_delta(obj_dist, prim_dist)
        v_delta, v_pct = calc_delta(obj_vel, prim_vel)

        absolute_differences.append({
            "target_name": obj["name"],
            "relative_to": primary["name"],
            "mass_diff_earth": m_delta,
            "mass_diff_percent": m_pct,
            "radius_diff_km": r_delta,
            "radius_diff_percent": r_pct,
            "gravity_diff_m_s2": g_delta,
            "gravity_diff_percent": g_pct,
            "density_diff_g_cm3": d_delta,
            "density_diff_percent": d_pct,
            "temperature_diff_k": t_delta,
            "temperature_diff_percent": t_pct,
            "distance_diff_au": dist_delta,
            "distance_diff_percent": dist_pct,
            "orbital_velocity_diff_km_s": v_delta,
            "orbital_velocity_diff_percent": v_pct,
        })

    # Prepare normalized radar chart metrics
    radar_data = []
    attributes = [
        "mass_earth_relative",
        "radius_earth_relative",
        "surface_gravity_m_s2",
        "mean_density_g_cm3",
        "surface_temperature_k",
        "semi_major_axis_au",
        "mean_orbital_velocity_km_s"
    ]
    attr_labels = {
        "mass_earth_relative": "Mass (Earth=1)",
        "radius_earth_relative": "Radius (Earth=1)",
        "surface_gravity_m_s2": "Gravity (m/s²)",
        "mean_density_g_cm3": "Density (g/cm³)",
        "surface_temperature_k": "Temperature (K)",
        "semi_major_axis_au": "Distance (AU)",
        "mean_orbital_velocity_km_s": "Orbital Velocity (km/s)"
    }

    for attr in attributes:
        entry = {"metric": attr_labels[attr]}
        for obj in objects:
            val = obj.get(attr)
            if val is None and attr == "semi_major_axis_au":
                val = obj.get("distance_from_sun")
            if val is None and attr == "mean_orbital_velocity_km_s":
                val = obj.get("orbital_velocity")
            entry[obj["name"]] = round(val, 2) if val is not None else 0.0
        radar_data.append(entry)

    # Generate persona-grounded comparative insights
    sec = objects[1] if len(objects) > 1 else primary
    insights = {
        "citizen": f"If you set foot on {sec['name']}, your weight would be about {round(sec.get('surface_gravity_m_s2', 9.8)/9.8, 2)}x your weight on Earth. Meanwhile, {primary['name']} and {sec['name']} have a radius ratio of {round((sec.get('radius_km', 1)/primary.get('radius_km', 1)), 2)}:1.",
        "student": f"According to Newton's Law of Universal Gravitation ($g = GM/R^2$), surface gravity scales linearly with mass but inversely with the square of radius. {primary['name']} has density {primary.get('mean_density_g_cm3')} g/cm³ compared to {sec.get('mean_density_g_cm3')} g/cm³ for {sec['name']}.",
        "researcher": f"Empirical dimensional comparison: M_ratio={round(sec.get('mass_kg', 1)/primary.get('mass_kg', 1), 4)}, R_ratio={round(sec.get('radius_km', 1)/primary.get('radius_km', 1), 4)}. The resulting gravitational surface potential ratio is phi_2/phi_1 = (M_2/M_1)*(R_1/R_2) = {round((sec.get('mass_kg', 1)/primary.get('mass_kg', 1))*(primary.get('radius_km', 1)/sec.get('radius_km', 1)), 4)}."
    }

    return DetailedComparisonResponse(
        compared_objects=objects,
        primary_reference=primary["name"],
        calculated_ratios=ratios,
        radar_chart_metrics=radar_data,
        absolute_differences=absolute_differences,
        comparative_insights=insights
    )
