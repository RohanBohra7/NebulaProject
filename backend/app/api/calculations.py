"""
REST API endpoints for NEBULA Scientific Computation Engine.
Provides validated, high-precision astronomical calculations for gravity,
orbital mechanics, trajectories, distance metrics, coordinate systems, and Astropy unit conversions.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Dict, Any, List, Union
from sqlalchemy.orm import Session
import math

from app.db.database import get_db
from app.data.catalog import get_object_by_id
from app.scientific import (
    # Constants
    G_CONST,
    M_SUN,
    M_EARTH,
    AU_METERS,
    PC_METERS,
    LY_METERS,
    SPEED_OF_LIGHT,
    # Gravity
    calculate_gravitational_force,
    calculate_gravitational_force_vector,
    calculate_surface_gravity,
    calculate_gravitational_potential,
    calculate_tidal_acceleration,
    # Orbital
    calculate_circular_velocity,
    calculate_vis_viva_velocity,
    calculate_escape_velocity,
    calculate_apsidal_velocities,
    calculate_orbital_period,
    calculate_synodic_period,
    calculate_orbital_parameters,
    calculate_hohmann_transfer,
    calculate_hill_sphere,
    calculate_roche_limit,
    find_orbital_resonances,
    calculate_lagrange_points,
    # Distances
    calculate_euclidean_distance,
    calculate_light_travel_time,
    calculate_angular_diameter,
    calculate_distance_modulus,
    calculate_distance_from_modulus,
    calculate_apsidal_distances,
    # Coordinates
    cartesian_to_spherical,
    spherical_to_cartesian,
    ecliptic_to_equatorial,
    equatorial_to_ecliptic,
    # Units
    convert_units,
    get_supported_categories
)

router = APIRouter(prefix="/calculate", tags=["Scientific Calculations"])

# ==================== REQUEST SCHEMAS ====================

# --- Gravity Schemas ---
class GravitationalForceRequest(BaseModel):
    m1_kg: Optional[float] = Field(None, gt=0, description="Mass of first body in kg (> 0)")
    m2_kg: Optional[float] = Field(None, gt=0, description="Mass of second body in kg (> 0)")
    distance_m: Optional[float] = Field(None, gt=0, description="Center-to-center distance in meters (> 0)")
    distance_au: Optional[float] = Field(None, gt=0, description="Center-to-center distance in AU (> 0)")
    distance_km: Optional[float] = Field(None, gt=0, description="Center-to-center distance in km (> 0)")
    object1_id: Optional[str] = Field(None, description="Catalog ID for first body (e.g. 'earth')")
    object2_id: Optional[str] = Field(None, description="Catalog ID for second body (e.g. 'moon', 'sun')")
    pos1_m: Optional[List[float]] = Field(None, description="Optional 3D position [x, y, z] in meters of body 1")
    pos2_m: Optional[List[float]] = Field(None, description="Optional 3D position [x, y, z] in meters of body 2")

class SurfaceGravityRequest(BaseModel):
    mass_kg: Optional[float] = Field(None, gt=0, description="Body mass in kg (> 0)")
    radius_m: Optional[float] = Field(None, gt=0, description="Body radius in meters (> 0)")
    radius_km: Optional[float] = Field(None, gt=0, description="Body radius in kilometers (> 0)")
    object_id: Optional[str] = Field(None, description="Catalog ID (e.g. 'jupiter')")

class GravitationalPotentialRequest(BaseModel):
    mass_kg: Optional[float] = Field(None, gt=0, description="Primary mass in kg (> 0)")
    distance_m: Optional[float] = Field(None, gt=0, description="Distance in meters (> 0)")
    distance_au: Optional[float] = Field(None, gt=0, description="Distance in AU (> 0)")
    secondary_mass_kg: Optional[float] = Field(None, gt=0, description="Optional secondary mass for potential energy U")
    object_id: Optional[str] = Field(None, description="Catalog ID (e.g. 'sun')")

# --- Orbital Schemas ---
class OrbitalVelocityRequest(BaseModel):
    central_mass_kg: Optional[float] = Field(M_SUN, gt=0, description="Central mass in kg (defaults to 1 M_sun)")
    distance_m: Optional[float] = Field(None, gt=0, description="Orbital radius or current distance in meters (> 0)")
    distance_au: Optional[float] = Field(None, gt=0, description="Orbital radius in AU (> 0)")
    semi_major_axis_au: Optional[float] = Field(None, gt=0, description="Semi-major axis in AU for eccentric orbit (> 0)")
    eccentricity: Optional[float] = Field(0.0, ge=0.0, lt=1.0, description="Eccentricity [0, 1)")
    body_radius_m: Optional[float] = Field(None, gt=0, description="Body radius for surface escape velocity")
    object_id: Optional[str] = Field(None, description="Catalog ID (e.g. 'earth')")

class OrbitalPeriodRequest(BaseModel):
    semi_major_axis_au: Optional[float] = Field(None, gt=0, description="Semi-major axis in AU (> 0)")
    semi_major_axis_m: Optional[float] = Field(None, gt=0, description="Semi-major axis in meters (> 0)")
    central_mass_kg: Optional[float] = Field(M_SUN, gt=0, description="Central mass in kg (defaults to 1 M_sun)")
    secondary_mass_kg: Optional[float] = Field(0.0, ge=0, description="Secondary body mass in kg")
    period1_days: Optional[float] = Field(None, gt=0, description="Period of body 1 for synodic calculation")
    period2_days: Optional[float] = Field(None, gt=0, description="Period of body 2 for synodic calculation")
    object_id: Optional[str] = Field(None, description="Catalog ID")

class OrbitalParametersRequest(BaseModel):
    semi_major_axis_au: Optional[float] = Field(None, gt=0, description="Semi-major axis in AU (> 0)")
    semi_major_axis_m: Optional[float] = Field(None, gt=0, description="Semi-major axis in meters (> 0)")
    eccentricity: float = Field(..., ge=0.0, description="Eccentricity (>= 0)")
    central_mass_kg: Optional[float] = Field(M_SUN, gt=0, description="Central mass in kg")
    object_id: Optional[str] = Field(None, description="Catalog ID")

# --- Distance Schemas ---
class DistanceCalculationRequest(BaseModel):
    calculation_type: str = Field("euclidean", description="'euclidean', 'light_travel', 'angular_diameter', or 'distance_modulus'")
    pos1: Optional[List[float]] = Field(None, description="[x, y, z] coordinate 1")
    pos2: Optional[List[float]] = Field(None, description="[x, y, z] coordinate 2")
    input_unit: Optional[str] = Field("au", description="'m', 'km', 'au', 'pc', 'ly'")
    distance_m: Optional[float] = Field(None, gt=0)
    distance_au: Optional[float] = Field(None, gt=0)
    physical_diameter_m: Optional[float] = Field(None, gt=0)
    distance_pc: Optional[float] = Field(None, gt=0)
    distance_modulus: Optional[float] = None

# --- Coordinate Schemas ---
class CoordinatesRequest(BaseModel):
    conversion_type: str = Field(
        ...,
        description="'cartesian_to_spherical', 'spherical_to_cartesian', 'ecliptic_to_equatorial', or 'equatorial_to_ecliptic'"
    )
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    radius: Optional[float] = Field(None, ge=0)
    theta_rad: Optional[float] = None
    phi_rad: Optional[float] = None
    ecliptic_lon_deg: Optional[float] = None
    ecliptic_lat_deg: Optional[float] = None
    ra_deg: Optional[float] = None
    dec_deg: Optional[float] = None
    obliquity_deg: Optional[float] = 23.43929111

# --- Unit Conversion Schema ---
class UnitConversionRequest(BaseModel):
    value: float = Field(..., description="Numerical value to convert")
    from_unit: str = Field(..., description="Source unit string (e.g. 'kg', 'M_sun', 'AU', 'km', 'c', 'K')")
    to_unit: str = Field(..., description="Target unit string (e.g. 'M_earth', 'm', 'ly', 'deg_C')")

# --- Legacy & Specific Trajectory Schemas ---
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
    primary_radius_km: float = Field(..., gt=0)
    primary_density_g_cm3: float = Field(..., gt=0)
    secondary_density_g_cm3: float = Field(..., gt=0)

class ResonanceRequest(BaseModel):
    period_days_1: float = Field(..., gt=0)
    period_days_2: float = Field(..., gt=0)
    max_order: int = 8

class LagrangeRequest(BaseModel):
    primary_mass_kg: float = M_SUN
    secondary_mass_kg: float
    separation_au: float


# ==================== GRAVITATIONAL ENDPOINTS ====================

@router.post("/gravity/force")
def gravity_force(req: GravitationalForceRequest, db: Session = Depends(get_db)):
    """
    Computes Newtonian gravitational attraction force between two celestial bodies.
    Supports catalog object lookup or direct physical quantities.
    """
    m1 = req.m1_kg
    m2 = req.m2_kg
    name1 = "Body 1"
    name2 = "Body 2"

    if req.object1_id:
        obj1 = get_object_by_id(db, req.object1_id)
        if obj1 and obj1.get("mass_kg"):
            m1 = obj1["mass_kg"]
            name1 = obj1["name"]
    if req.object2_id:
        obj2 = get_object_by_id(db, req.object2_id)
        if obj2 and obj2.get("mass_kg"):
            m2 = obj2["mass_kg"]
            name2 = obj2["name"]

    if not m1 or not m2 or m1 <= 0 or m2 <= 0:
        raise HTTPException(status_code=400, detail="Requires positive masses for both bodies (> 0 kg).")

    # If 3D vectors provided, compute vector force
    if req.pos1_m is not None and req.pos2_m is not None:
        try:
            res_vec = calculate_gravitational_force_vector(m1, m2, req.pos1_m, req.pos2_m)
            return {"name1": name1, "name2": name2, **res_vec}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # Determine scalar distance in meters
    dist_m = req.distance_m
    if dist_m is None and req.distance_au is not None:
        dist_m = req.distance_au * AU_METERS
    elif dist_m is None and req.distance_km is not None:
        dist_m = req.distance_km * 1000.0

    if not dist_m or dist_m <= 0:
        raise HTTPException(
            status_code=400,
            detail="Requires positive distance between bodies (> 0 m, km, or AU) or 3D position vectors."
        )

    try:
        res = calculate_gravitational_force(m1, m2, dist_m)
        return {"name1": name1, "name2": name2, **res}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/gravity/surface")
def surface_gravity(req: SurfaceGravityRequest, db: Session = Depends(get_db)):
    """
    Computes local surface gravitational acceleration (m/s^2 and Earth gees) for a celestial body.
    """
    mass = req.mass_kg
    radius = req.radius_m
    name = "Target Body"

    if req.radius_km is not None and radius is None:
        radius = req.radius_km * 1000.0

    if req.object_id:
        obj = get_object_by_id(db, req.object_id)
        if obj:
            mass = obj.get("mass_kg", mass)
            r_km = obj.get("radius_km")
            if r_km and radius is None:
                radius = r_km * 1000.0
            name = obj.get("name", name)

    if not mass or not radius or mass <= 0 or radius <= 0:
        raise HTTPException(status_code=400, detail="Requires strictly positive mass_kg and radius_m (> 0).")

    try:
        res = calculate_surface_gravity(mass, radius)
        return {"name": name, **res}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/gravity/potential")
def gravitational_potential(req: GravitationalPotentialRequest, db: Session = Depends(get_db)):
    """
    Computes gravitational potential Phi(r) and potential energy U(r) at distance r.
    """
    mass = req.mass_kg
    dist_m = req.distance_m

    if dist_m is None and req.distance_au is not None:
        dist_m = req.distance_au * AU_METERS

    if req.object_id:
        obj = get_object_by_id(db, req.object_id)
        if obj and obj.get("mass_kg"):
            mass = obj["mass_kg"]

    if not mass or not dist_m or mass <= 0 or dist_m <= 0:
        raise HTTPException(status_code=400, detail="Requires positive mass_kg and distance_m (> 0).")

    try:
        return calculate_gravitational_potential(mass, dist_m, req.secondary_mass_kg)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== ORBITAL VELOCITY & PERIOD ENDPOINTS ====================

@router.post("/orbital-velocity")
def orbital_velocity(req: OrbitalVelocityRequest, db: Session = Depends(get_db)):
    """
    Computes orbital velocity metrics: circular velocity, vis-viva velocity, escape velocity, and apsidal extrema.
    """
    central_m = req.central_mass_kg or M_SUN
    r_m = req.distance_m
    name = "Target"

    if r_m is None and req.distance_au is not None:
        r_m = req.distance_au * AU_METERS

    a_m = None
    if req.semi_major_axis_au is not None:
        a_m = req.semi_major_axis_au * AU_METERS

    if req.object_id:
        obj = get_object_by_id(db, req.object_id)
        if obj:
            name = obj.get("name", name)
            if obj.get("semi_major_axis_au") and a_m is None:
                a_m = obj["semi_major_axis_au"] * AU_METERS
            if r_m is None and a_m is not None:
                r_m = a_m

    results: Dict[str, Any] = {"name": name, "central_mass_kg": central_m}

    # 1. Circular velocity
    if r_m and r_m > 0:
        results["circular_velocity"] = calculate_circular_velocity(central_m, r_m)

    # 2. Escape velocity
    if r_m and r_m > 0:
        results["escape_velocity"] = calculate_escape_velocity(central_m, r_m)

    # 3. Vis-viva instantaneous velocity
    if r_m and a_m and r_m > 0 and a_m > 0:
        try:
            results["vis_viva_velocity"] = calculate_vis_viva_velocity(central_m, r_m, a_m)
        except ValueError as err:
            results["vis_viva_velocity"] = {"error": str(err)}

    # 4. Apsidal velocities if semi-major axis and eccentricity provided
    if a_m and a_m > 0 and req.eccentricity is not None and 0 <= req.eccentricity < 1.0:
        results["apsidal_velocities"] = calculate_apsidal_velocities(central_m, a_m, req.eccentricity)

    if len(results) <= 2:
        raise HTTPException(status_code=400, detail="Requires positive distance_m/au or semi_major_axis_au.")

    return results

@router.post("/orbital-period")
def orbital_period(req: OrbitalPeriodRequest, db: Session = Depends(get_db)):
    """
    Computes Keplerian orbital period (Kepler's Third Law) and/or synodic period between two bodies.
    """
    # Synodic period calculation if two periods provided
    if req.period1_days and req.period2_days:
        try:
            return calculate_synodic_period(req.period1_days, req.period2_days)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # Keplerian orbital period
    a_m = req.semi_major_axis_m
    if a_m is None and req.semi_major_axis_au is not None:
        a_m = req.semi_major_axis_au * AU_METERS

    central_m = req.central_mass_kg or M_SUN
    secondary_m = req.secondary_mass_kg or 0.0

    if req.object_id:
        obj = get_object_by_id(db, req.object_id)
        if obj:
            if obj.get("semi_major_axis_au") and a_m is None:
                a_m = obj["semi_major_axis_au"] * AU_METERS
            if obj.get("mass_kg") and secondary_m == 0.0:
                secondary_m = obj["mass_kg"]

    if not a_m or a_m <= 0:
        raise HTTPException(
            status_code=400,
            detail="Requires positive semi_major_axis_au/m (> 0) or period1_days and period2_days for synodic period."
        )

    try:
        return calculate_orbital_period(a_m, central_m, secondary_m)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/orbital-parameters")
def orbital_parameters(req: OrbitalParametersRequest, db: Session = Depends(get_db)):
    """
    Computes complete Keplerian orbit geometry: semi-minor axis, semi-latus rectum,
    periapsis/apoapsis, specific orbital energy, and angular momentum.
    """
    a_m = req.semi_major_axis_m
    if a_m is None and req.semi_major_axis_au is not None:
        a_m = req.semi_major_axis_au * AU_METERS

    if req.object_id:
        obj = get_object_by_id(db, req.object_id)
        if obj and obj.get("semi_major_axis_au") and a_m is None:
            a_m = obj["semi_major_axis_au"] * AU_METERS

    if not a_m or a_m <= 0:
        raise HTTPException(status_code=400, detail="Requires positive semi_major_axis_au or semi_major_axis_m (> 0).")

    try:
        return calculate_orbital_parameters(a_m, req.eccentricity, req.central_mass_kg or M_SUN)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== DISTANCE METRICS ENDPOINTS ====================

@router.post("/distance")
def distance_calculations(req: DistanceCalculationRequest):
    """
    Computes spatial distance metrics: 3D Euclidean separation, light travel time,
    apparent angular diameter, and photometric distance modulus.
    """
    calc = req.calculation_type.lower()

    if calc == "euclidean":
        if not req.pos1 or not req.pos2:
            raise HTTPException(status_code=400, detail="Euclidean distance requires both pos1 and pos2 coordinate arrays.")
        try:
            return calculate_euclidean_distance(req.pos1, req.pos2, req.input_unit or "au")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    elif calc == "light_travel":
        dist_m = req.distance_m
        if dist_m is None and req.distance_au is not None:
            dist_m = req.distance_au * AU_METERS
        if not dist_m or dist_m <= 0:
            raise HTTPException(status_code=400, detail="Requires strictly positive distance_m or distance_au (> 0).")
        try:
            return calculate_light_travel_time(dist_m)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    elif calc == "angular_diameter":
        dist_m = req.distance_m
        if dist_m is None and req.distance_au is not None:
            dist_m = req.distance_au * AU_METERS
        if not req.physical_diameter_m or not dist_m or req.physical_diameter_m <= 0 or dist_m <= 0:
            raise HTTPException(status_code=400, detail="Requires positive physical_diameter_m and distance_m/au.")
        try:
            return calculate_angular_diameter(req.physical_diameter_m, dist_m)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    elif calc == "distance_modulus":
        if req.distance_pc is not None and req.distance_pc > 0:
            return calculate_distance_modulus(req.distance_pc)
        elif req.distance_modulus is not None:
            return calculate_distance_from_modulus(req.distance_modulus)
        else:
            raise HTTPException(status_code=400, detail="Requires positive distance_pc or numerical distance_modulus.")

    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported calculation_type '{req.calculation_type}'. Choose from 'euclidean', 'light_travel', 'angular_diameter', 'distance_modulus'."
        )


# ==================== COORDINATE TRANSFORMATIONS ====================

@router.post("/coordinates")
def coordinate_transforms(req: CoordinatesRequest):
    """
    Transforms coordinates across Cartesian, spherical, ecliptic, and equatorial reference frames.
    """
    ctype = req.conversion_type.lower()

    if ctype == "cartesian_to_spherical":
        if req.x is None or req.y is None or req.z is None:
            raise HTTPException(status_code=400, detail="Requires x, y, and z coordinates.")
        return cartesian_to_spherical(req.x, req.y, req.z)

    elif ctype == "spherical_to_cartesian":
        if req.radius is None or req.theta_rad is None or req.phi_rad is None:
            raise HTTPException(status_code=400, detail="Requires radius, theta_rad, and phi_rad.")
        try:
            return spherical_to_cartesian(req.radius, req.theta_rad, req.phi_rad)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    elif ctype == "ecliptic_to_equatorial":
        if req.ecliptic_lon_deg is None or req.ecliptic_lat_deg is None:
            raise HTTPException(status_code=400, detail="Requires ecliptic_lon_deg and ecliptic_lat_deg.")
        return ecliptic_to_equatorial(req.ecliptic_lon_deg, req.ecliptic_lat_deg, req.obliquity_deg or 23.43929111)

    elif ctype == "equatorial_to_ecliptic":
        if req.ra_deg is None or req.dec_deg is None:
            raise HTTPException(status_code=400, detail="Requires ra_deg and dec_deg.")
        return equatorial_to_ecliptic(req.ra_deg, req.dec_deg, req.obliquity_deg or 23.43929111)

    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported conversion_type '{req.conversion_type}'. Choose from 'cartesian_to_spherical', 'spherical_to_cartesian', 'ecliptic_to_equatorial', 'equatorial_to_ecliptic'."
        )


# ==================== ASTROPY UNIT CONVERSIONS ====================

@router.post("/unit-conversion")
def convert_physical_units(req: UnitConversionRequest):
    """
    Converts a physical magnitude between dimensional units using Astropy.
    Verifies physical dimension compatibility (e.g. mass, length, velocity, time, temperature).
    """
    try:
        return convert_units(req.value, req.from_unit, req.to_unit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/units/categories")
def unit_categories():
    """Returns catalog of supported dimensional unit categories."""
    return get_supported_categories()


# ==================== MISSION PLANNING & LEGACY CALCULATIONS ====================

@router.post("/hohmann")
def hohmann_transfer(req: HohmannRequest, db: Session = Depends(get_db)):
    """Computes Hohmann transfer orbit between two celestial bodies or two orbital radii."""
    r1 = req.r1_au
    r2 = req.r2_au
    origin_name = "Origin Orbit"
    target_name = "Target Orbit"

    if req.origin_id:
        obj1 = get_object_by_id(db, req.origin_id)
        if obj1 and obj1.get("semi_major_axis_au"):
            r1 = obj1["semi_major_axis_au"]
            origin_name = obj1["name"]
    if req.target_id:
        obj2 = get_object_by_id(db, req.target_id)
        if obj2 and obj2.get("semi_major_axis_au"):
            r2 = obj2["semi_major_axis_au"]
            target_name = obj2["name"]

    if not r1 or not r2 or r1 <= 0 or r2 <= 0:
        raise HTTPException(status_code=400, detail="Invalid radii. Semi-major axes must be strictly positive.")
    if math.isclose(r1, r2, rel_tol=1e-7):
        raise HTTPException(status_code=400, detail="Origin and target orbits cannot have the exact same radius.")

    try:
        res = calculate_hohmann_transfer(r1, r2)
        return {
            "origin_name": origin_name,
            "target_name": target_name,
            **res
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/hill-sphere")
def hill_sphere(req: HillSphereRequest, db: Session = Depends(get_db)):
    """Computes Hill sphere radius for a body orbiting a primary mass."""
    a = req.semi_major_axis_au
    e = req.eccentricity or 0.0
    m = req.body_mass_kg
    m_parent = req.parent_mass_kg or M_SUN

    if req.object_id:
        obj = get_object_by_id(db, req.object_id)
        if obj:
            a = obj.get("semi_major_axis_au", a)
            e = obj.get("eccentricity", e)
            m = obj.get("mass_kg", m)

    if not a or not m or a <= 0 or m <= 0:
        raise HTTPException(status_code=400, detail="Requires positive semi_major_axis_au and body_mass_kg.")

    try:
        return calculate_hill_sphere(a, e, m, m_parent)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/roche-limit")
def roche_limit(req: RocheLimitRequest):
    """Computes rigid and fluid Roche limits for tidal disruption."""
    try:
        return calculate_roche_limit(req.primary_radius_km, req.primary_density_g_cm3, req.secondary_density_g_cm3)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/resonance")
def orbital_resonance(req: ResonanceRequest):
    """Detects near-integer mean-motion orbital resonances between two orbital periods."""
    try:
        matches = find_orbital_resonances(req.period_days_1, req.period_days_2, req.max_order)
        return {
            "period_1_days": req.period_days_1,
            "period_2_days": req.period_days_2,
            "resonances_found": matches,
            "has_resonance": len(matches) > 0
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/lagrange-points")
def lagrange_points(req: LagrangeRequest):
    """Computes spatial coordinates and stability for Lagrange equilibrium points L1-L5."""
    try:
        return calculate_lagrange_points(req.primary_mass_kg, req.secondary_mass_kg, req.separation_au)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
