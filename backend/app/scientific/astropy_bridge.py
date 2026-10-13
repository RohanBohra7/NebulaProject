"""
Astropy Bridge: Astronomical Units & Dimensional Conversion Engine for NEBULA.
Uses astropy.units and astropy.constants to compute normalized physical values,
alternative astrophysical coordinate representations, and validation checks.
"""
import math
from typing import Dict, Any, Optional, List
import astropy.units as u
from astropy.constants import G, M_sun, M_earth, M_jup, R_sun, R_earth, R_jup
from app.schemas.celestial import AstropyUnitsBreakdown, RelatedObjectSummary

# Constants in SI
M_SUN_KG = M_sun.value # ~1.9884e30
M_EARTH_KG = M_earth.value # ~5.9722e24
M_JUP_KG = M_jup.value # ~1.8981e27
R_SUN_KM = R_sun.value / 1000.0 # ~695700
R_EARTH_KM = R_earth.value / 1000.0 # ~6378.137
R_JUP_KM = R_jup.value / 1000.0 # ~71492.0
G_VAL = G.value # 6.6743e-11

def compute_astropy_units(obj: Dict[str, Any]) -> AstropyUnitsBreakdown:
    """
    Computes alternate astrophysical units for mass, radius, distance, and gravity
    using exact IAU/CODATA Astropy constants.
    """
    mass_kg = obj.get("mass_kg")
    radius_km = obj.get("radius_km")
    semi_major_axis_au = obj.get("semi_major_axis_au")
    surface_gravity_m_s2 = obj.get("surface_gravity_m_s2")
    surface_temperature_k = obj.get("surface_temperature_k")

    mass_solar = None
    mass_jupiter = None
    mass_earth = None
    if mass_kg and mass_kg > 0:
        mass_q = mass_kg * u.kg
        mass_solar = round(float((mass_q / M_sun).to_value(u.dimensionless_unscaled)), 6)
        mass_jupiter = round(float((mass_q / M_jup).to_value(u.dimensionless_unscaled)), 4)
        mass_earth = round(float((mass_q / M_earth).to_value(u.dimensionless_unscaled)), 4)

    radius_solar = None
    radius_jupiter = None
    radius_earth = None
    if radius_km and radius_km > 0:
        r_q = (radius_km * u.km).to(u.m)
        radius_solar = round(float((r_q / R_sun).to_value(u.dimensionless_unscaled)), 6)
        radius_jupiter = round(float((r_q / R_jup).to_value(u.dimensionless_unscaled)), 4)
        radius_earth = round(float((r_q / R_earth).to_value(u.dimensionless_unscaled)), 4)

    dist_au = semi_major_axis_au
    dist_pc = None
    dist_ly = None
    if semi_major_axis_au and semi_major_axis_au > 0:
        dist_q = semi_major_axis_au * u.AU
        dist_pc = round(float(dist_q.to(u.pc).value), 7)
        dist_ly = round(float(dist_q.to(u.lyr).value), 7)

    gravity_gees = None
    if surface_gravity_m_s2 is not None:
        gravity_gees = round(float(surface_gravity_m_s2 / 9.80665), 3)

    temp_celsius = None
    if surface_temperature_k is not None:
        temp_celsius = round(float(surface_temperature_k - 273.15), 1)

    return AstropyUnitsBreakdown(
        mass_solar=mass_solar,
        mass_jupiter=mass_jupiter,
        mass_earth=mass_earth,
        radius_solar=radius_solar,
        radius_jupiter=radius_jupiter,
        radius_earth=radius_earth,
        distance_au=dist_au,
        distance_parsec=dist_pc,
        distance_light_years=dist_ly,
        surface_gravity_gees=gravity_gees,
        temperature_celsius=temp_celsius
    )

def find_related_objects(obj_id: str, all_objects: List[Dict[str, Any]]) -> List[RelatedObjectSummary]:
    """
    Identifies related celestial bodies:
    - Moons of this body
    - Parent primary body
    - Planetary siblings orbiting the same star
    - Top matches in the same category
    """
    target = None
    for o in all_objects:
        if o["id"] == obj_id:
            target = o
            break

    if not target:
        return []

    related: List[RelatedObjectSummary] = []
    seen_ids = {obj_id}

    # 1. Moons of this object (parent_body_id == obj_id)
    for o in all_objects:
        if o.get("parent_body_id") == obj_id and o["id"] not in seen_ids:
            related.append(RelatedObjectSummary(
                id=o["id"],
                name=o["name"],
                category=o["category"],
                relationship="Moon / Satellite",
                color_hex=o.get("color_hex", "#94a3b8")
            ))
            seen_ids.add(o["id"])

    # 2. Parent primary body (if this is a moon or exoplanet)
    parent_id = target.get("parent_body_id")
    if parent_id:
        for o in all_objects:
            if o["id"] == parent_id and o["id"] not in seen_ids:
                rel_label = "Host Star" if o["category"] == "Star" else "Parent Body"
                related.append(RelatedObjectSummary(
                    id=o["id"],
                    name=o["name"],
                    category=o["category"],
                    relationship=rel_label,
                    color_hex=o.get("color_hex", "#94a3b8")
                ))
                seen_ids.add(o["id"])

    # 3. System siblings (orbiting same parent)
    if parent_id:
        for o in all_objects:
            if o.get("parent_body_id") == parent_id and o["id"] not in seen_ids:
                related.append(RelatedObjectSummary(
                    id=o["id"],
                    name=o["name"],
                    category=o["category"],
                    relationship="Orbital Sibling",
                    color_hex=o.get("color_hex", "#94a3b8")
                ))
                seen_ids.add(o["id"])

    # 4. Same category objects (up to 3)
    same_cat_count = 0
    for o in all_objects:
        if o["category"] == target["category"] and o["id"] not in seen_ids and same_cat_count < 3:
            related.append(RelatedObjectSummary(
                id=o["id"],
                name=o["name"],
                category=o["category"],
                relationship=f"Fellow {target['category']}",
                color_hex=o.get("color_hex", "#94a3b8")
            ))
            seen_ids.add(o["id"])
            same_cat_count += 1

    return related
