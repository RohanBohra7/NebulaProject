from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Dict, Any, Literal, Union
from enum import Enum

class CelestialCategoryEnum(str, Enum):
    PLANET = "Planet"
    MOON = "Moon"
    STAR = "Star"
    EXOPLANET = "Exoplanet"
    ASTEROID = "Asteroid"
    COMET = "Comet"
    DEEP_SKY = "Deep-Sky"
    GENERIC = "Generic"

class SourceMetadata(BaseModel):
    source_name: str = Field(..., description="Name of astronomical data provider or catalog")
    source_url: Optional[str] = Field(None, description="Direct URL to source repository or documentation")
    retrieval_date: Optional[str] = Field("2026-10-06", description="ISO date of data acquisition or synchronization")
    is_demo_seed: bool = Field(True, description="Indicates whether this object is bundled for offline local demo")
    confidence_level: str = Field("High", description="Empirical confidence score (High, Moderate, Preliminary)")
    provenance_badge: str = Field("Verified Empirical (Local Primary)", description="Short display badge for UI")

class RawSourceData(BaseModel):
    source_id: str
    provider_name: str
    raw_payload: Dict[str, Any]
    ingested_at: Optional[str] = None

class AstropyUnitsBreakdown(BaseModel):
    mass_solar: Optional[float] = Field(None, description="Mass in Solar masses (M_sun)")
    mass_jupiter: Optional[float] = Field(None, description="Mass in Jupiter masses (M_jup)")
    mass_earth: Optional[float] = Field(None, description="Mass in Earth masses (M_earth)")
    radius_solar: Optional[float] = Field(None, description="Radius in Solar radii (R_sun)")
    radius_jupiter: Optional[float] = Field(None, description="Radius in Jupiter radii (R_jup)")
    radius_earth: Optional[float] = Field(None, description="Radius in Earth radii (R_earth)")
    distance_au: Optional[float] = Field(None, description="Semi-major axis in Astronomical Units (AU)")
    distance_parsec: Optional[float] = Field(None, description="Distance in parsecs (pc)")
    distance_light_years: Optional[float] = Field(None, description="Distance in light years (ly)")
    surface_gravity_gees: Optional[float] = Field(None, description="Surface gravity relative to standard Earth g (9.80665 m/s²)")
    temperature_celsius: Optional[float] = Field(None, description="Surface temperature in Celsius (°C)")

class RelatedObjectSummary(BaseModel):
    id: str
    name: str
    category: str
    relationship: str # "moon", "parent", "host_star", "sibling_planet", "same_category"
    color_hex: Optional[str] = "#94a3b8"

class OrbitalElements(BaseModel):
    semi_major_axis_au: Optional[float] = None
    eccentricity: Optional[float] = None
    orbital_inclination_deg: Optional[float] = None
    orbital_period_days: Optional[float] = None
    perihelion_au: Optional[float] = None
    aphelion_au: Optional[float] = None
    mean_orbital_velocity_km_s: Optional[float] = None
    ascending_node_deg: Optional[float] = 0.0
    arg_periapsis_deg: Optional[float] = 0.0
    mean_anomaly_epoch_deg: Optional[float] = 0.0

class PhysicalParameters(BaseModel):
    mass_kg: Optional[float] = None
    mass_earth_relative: Optional[float] = None
    radius_km: Optional[float] = None
    radius_earth_relative: Optional[float] = None
    mean_density_g_cm3: Optional[float] = None
    surface_gravity_m_s2: Optional[float] = None
    escape_velocity_km_s: Optional[float] = None
    surface_temperature_k: Optional[float] = None
    luminosity_solar: Optional[float] = None
    spectral_type: Optional[str] = None
    apparent_magnitude: Optional[float] = None
    absolute_magnitude: Optional[float] = None
    has_rings: Optional[bool] = False
    has_atmosphere: Optional[bool] = False

class MultiPersonaDescriptions(BaseModel):
    description_citizen: str
    description_student: str
    description_researcher: str
    educational_facts: Optional[List[str]] = []
    research_notes: Optional[Dict[str, Any]] = {}

# =====================================================================
# SPECIALIZED NORMALIZED OBJECT MODELS (PHASE 2 DATA MODEL SPEC)
# =====================================================================

DEFAULT_UNITS = {
    "mass": "kg",
    "radius": "km",
    "gravity": "m/s²",
    "distance_from_sun": "AU",
    "orbital_period": "days",
    "rotation_period": "hours",
    "orbital_velocity": "km/s",
    "temperature": "K"
}

class CelestialBase(BaseModel):
    """
    Common normalized foundation for all astronomical entities.
    Does not force orbital or host-dependent fields onto non-orbiting bodies.
    """
    id: str = Field(..., description="Unique slug identifier (e.g., 'earth', 'sun')")
    name: str = Field(..., description="Common astronomical name")
    object_type: str = Field(..., description="Classification: Planet, Moon, Star, Exoplanet, Asteroid, Comet, Generic")
    description: str = Field(..., description="Primary descriptive text")
    mass: Optional[float] = Field(None, description="Mass in kg")
    radius: Optional[float] = Field(None, description="Volumetric mean radius in km")
    gravity: Optional[float] = Field(None, description="Surface gravity in m/s²")
    temperature: Optional[float] = Field(None, description="Surface / effective temperature in K")
    source: Optional[str] = Field("NASA Planetary Fact Sheet / JPL Horizons", description="Data provider or catalog source")
    source_url: Optional[str] = Field(None, description="Direct URL to source repository or documentation")
    units: Dict[str, str] = Field(default_factory=lambda: dict(DEFAULT_UNITS), description="Documentation of field measurement units")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional scientific properties and telemetry")

class Star(CelestialBase):
    """
    Star model: central gravitational attractors.
    Does not force distance_from_sun or parent_object.
    """
    object_type: Literal["Star"] = "Star"
    spectral_type: Optional[str] = Field(None, description="Morgan-Keenan spectral classification (e.g., G2V, M1V)")
    luminosity: Optional[float] = Field(None, description="Luminosity in Solar units (L_sun)")
    rotation_period: Optional[float] = Field(None, description="Equatorial rotation period in hours")
    discovery_information: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Discovery metadata")

class Planet(CelestialBase):
    """
    Planet model: major bodies orbiting a central star.
    """
    object_type: Literal["Planet"] = "Planet"
    parent_object: Optional[str] = Field("sun", description="Host star identifier")
    distance_from_sun: Optional[float] = Field(None, description="Semi-major axis in Astronomical Units (AU)")
    orbital_period: Optional[float] = Field(None, description="Orbital period in days")
    rotation_period: Optional[float] = Field(None, description="Rotation period in hours")
    orbital_velocity: Optional[float] = Field(None, description="Mean heliocentric orbital velocity in km/s")
    orbital_parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Keplerian orbital parameters")
    discovery_information: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Historical discovery details")
    has_rings: Optional[bool] = Field(False, description="Presence of ring system")
    has_atmosphere: Optional[bool] = Field(False, description="Presence of atmospheric envelope")

class Moon(CelestialBase):
    """
    Moon model: natural satellites orbiting a parent planet.
    """
    object_type: Literal["Moon"] = "Moon"
    parent_object: str = Field(..., description="Host planet identifier (e.g. 'earth', 'jupiter', 'saturn')")
    orbital_period: Optional[float] = Field(None, description="Orbital period around parent body in days")
    rotation_period: Optional[float] = Field(None, description="Rotation period in hours (often synchronously locked)")
    orbital_velocity: Optional[float] = Field(None, description="Mean orbital velocity in km/s")
    distance_from_parent: Optional[float] = Field(None, description="Semi-major axis relative to host planet in km")
    orbital_parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    discovery_information: Optional[Dict[str, Any]] = Field(default_factory=dict)

class Exoplanet(CelestialBase):
    """
    Exoplanet model: planets orbiting stars outside the Solar System.
    """
    object_type: Literal["Exoplanet"] = "Exoplanet"
    parent_object: str = Field(..., description="Host star identifier (e.g., 'trappist-1', 'proxima-centauri')")
    distance_from_host_star: Optional[float] = Field(None, description="Semi-major axis in AU")
    orbital_period: Optional[float] = Field(None, description="Orbital period in days")
    orbital_velocity: Optional[float] = Field(None, description="Mean orbital velocity in km/s")
    orbital_parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    discovery_information: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Method (Transit, RV), year, facility")

class Asteroid(CelestialBase):
    """
    Asteroid model: minor planets in the Solar System.
    """
    object_type: Literal["Asteroid"] = "Asteroid"
    parent_object: Optional[str] = Field("sun", description="Host star identifier")
    distance_from_sun: Optional[float] = Field(None, description="Semi-major axis in AU")
    orbital_period: Optional[float] = Field(None, description="Orbital period in days")
    rotation_period: Optional[float] = Field(None, description="Rotation period in hours")
    orbital_velocity: Optional[float] = Field(None, description="Mean orbital velocity in km/s")
    orbital_parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    discovery_information: Optional[Dict[str, Any]] = Field(default_factory=dict)

class Comet(CelestialBase):
    """
    Comet model: small Solar System icy bodies with highly eccentric orbits.
    """
    object_type: Literal["Comet"] = "Comet"
    parent_object: Optional[str] = Field("sun", description="Host star identifier")
    distance_from_sun: Optional[float] = Field(None, description="Semi-major axis in AU")
    orbital_period: Optional[float] = Field(None, description="Orbital period in days or years")
    orbital_velocity: Optional[float] = Field(None, description="Mean orbital velocity in km/s")
    orbital_parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Perihelion AU, aphelion AU, eccentricity")
    discovery_information: Optional[Dict[str, Any]] = Field(default_factory=dict)

class GenericCelestialObject(CelestialBase):
    """
    Generic model: deep-sky objects, galaxies, and black holes.
    """
    object_type: str = Field("Generic", description="Generic or deep-sky category")
    orbital_parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    discovery_information: Optional[Dict[str, Any]] = Field(default_factory=dict)

def create_astronomical_object(data: Dict[str, Any]) -> Union[Planet, Moon, Star, Exoplanet, Asteroid, Comet, GenericCelestialObject]:
    """
    Factory function instantiating the appropriate specialized celestial model
    without forcing irrelevant properties.
    """
    obj_type = data.get("object_type") or data.get("category", "Generic")
    d = dict(data)
    d["object_type"] = obj_type
    if "description" not in d:
        d["description"] = d.get("description_citizen") or d.get("description_student") or d.get("description_researcher") or f"{d.get('name', '')} is a celestial body."
    if "mass" not in d and "mass_kg" in d:
        d["mass"] = d["mass_kg"]
    if "radius" not in d and "radius_km" in d:
        d["radius"] = d["radius_km"]
    if "gravity" not in d and "surface_gravity_m_s2" in d:
        d["gravity"] = d["surface_gravity_m_s2"]
    if "temperature" not in d and "surface_temperature_k" in d:
        d["temperature"] = d["surface_temperature_k"]
    if "distance_from_sun" not in d and "semi_major_axis_au" in d:
        d["distance_from_sun"] = d["semi_major_axis_au"]
    if "orbital_period" not in d and "orbital_period_days" in d:
        d["orbital_period"] = d["orbital_period_days"]
    if "orbital_velocity" not in d and "mean_orbital_velocity_km_s" in d:
        d["orbital_velocity"] = d["mean_orbital_velocity_km_s"]
    if "parent_object" not in d and "parent_body_id" in d:
        d["parent_object"] = d["parent_body_id"]
    if "source" not in d and "data_source" in d:
        d["source"] = d["data_source"]
    if "source_url" not in d and d.get("source_metadata"):
        d["source_url"] = d["source_metadata"].get("source_url")

    norm_type = obj_type.lower()
    if norm_type == "star":
        return Star(**d)
    elif norm_type == "planet":
        return Planet(**d)
    elif norm_type == "moon":
        if "parent_object" not in d or not d["parent_object"]:
            d["parent_object"] = "earth"
        return Moon(**d)
    elif norm_type == "exoplanet":
        if "parent_object" not in d or not d["parent_object"]:
            d["parent_object"] = "host_star"
        return Exoplanet(**d)
    elif norm_type == "asteroid":
        return Asteroid(**d)
    elif norm_type == "comet":
        return Comet(**d)
    else:
        return GenericCelestialObject(**d)

# =====================================================================
# UNIFIED NORMALIZED MODEL (Maintains full API backward compatibility)
# =====================================================================

class NormalizedCelestialBody(BaseModel):
    id: str = Field(..., description="Unique slug identifier (e.g., 'earth', 'trappist-1e')")
    name: str = Field(..., description="Common astronomical name")
    category: str = Field(..., description="Category: Planet, Moon, Star, Exoplanet, Asteroid, Comet, Deep-Sky")
    parent_body_id: Optional[str] = Field(None, description="ID of host body or star")

    # Phase 2 explicit fields
    object_type: Optional[str] = None
    description: Optional[str] = None
    mass: Optional[float] = None
    radius: Optional[float] = None
    gravity: Optional[float] = None
    distance_from_sun: Optional[float] = None
    orbital_period: Optional[float] = None
    rotation_period: Optional[float] = None
    orbital_velocity: Optional[float] = None
    temperature: Optional[float] = None
    parent_object: Optional[str] = None
    orbital_parameters: Optional[Dict[str, Any]] = None
    discovery_information: Optional[Dict[str, Any]] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    units: Optional[Dict[str, str]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    # Physical
    mass_kg: Optional[float] = None
    mass_earth_relative: Optional[float] = None
    radius_km: Optional[float] = None
    radius_earth_relative: Optional[float] = None
    mean_density_g_cm3: Optional[float] = None
    surface_gravity_m_s2: Optional[float] = None
    escape_velocity_km_s: Optional[float] = None
    surface_temperature_k: Optional[float] = None
    luminosity_solar: Optional[float] = None
    spectral_type: Optional[str] = None
    apparent_magnitude: Optional[float] = None
    absolute_magnitude: Optional[float] = None
    
    # Orbital
    semi_major_axis_au: Optional[float] = None
    eccentricity: Optional[float] = None
    orbital_inclination_deg: Optional[float] = None
    orbital_period_days: Optional[float] = None
    perihelion_au: Optional[float] = None
    aphelion_au: Optional[float] = None
    mean_orbital_velocity_km_s: Optional[float] = None
    ascending_node_deg: Optional[float] = 0.0
    arg_periapsis_deg: Optional[float] = 0.0
    mean_anomaly_epoch_deg: Optional[float] = 0.0
    
    # Visual
    color_hex: Optional[str] = "#94a3b8"
    texture_preset: Optional[str] = "generic"
    has_rings: Optional[bool] = False
    has_atmosphere: Optional[bool] = False
    
    # Adaptive content
    description_citizen: Optional[str] = None
    description_student: Optional[str] = None
    description_researcher: Optional[str] = None
    educational_facts: Optional[List[str]] = []
    research_notes: Optional[Dict[str, Any]] = {}
    
    # Source metadata
    source_metadata: Optional[SourceMetadata] = None
    data_source: Optional[str] = "NASA Planetary Fact Sheet / JPL Horizons"
    data_confidence: Optional[str] = "High"

    @model_validator(mode="before")
    @classmethod
    def sync_phase2_fields(cls, values: Any) -> Any:
        if not isinstance(values, dict):
            return values
        
        # Sync type & category
        obj_type = values.get("object_type") or values.get("category") or "Generic"
        values["object_type"] = obj_type
        values["category"] = obj_type

        # Sync descriptions
        desc = values.get("description") or values.get("description_citizen") or values.get("description_student") or values.get("description_researcher") or ""
        values["description"] = desc
        if not values.get("description_citizen"):
            values["description_citizen"] = desc
        if not values.get("description_student"):
            values["description_student"] = desc
        if not values.get("description_researcher"):
            values["description_researcher"] = desc

        # Sync physical fields
        m = values.get("mass") if values.get("mass") is not None else values.get("mass_kg")
        values["mass"] = m
        values["mass_kg"] = m

        r = values.get("radius") if values.get("radius") is not None else values.get("radius_km")
        values["radius"] = r
        values["radius_km"] = r

        g = values.get("gravity") if values.get("gravity") is not None else values.get("surface_gravity_m_s2")
        values["gravity"] = g
        values["surface_gravity_m_s2"] = g

        t = values.get("temperature") if values.get("temperature") is not None else values.get("surface_temperature_k")
        values["temperature"] = t
        values["surface_temperature_k"] = t

        dist = values.get("distance_from_sun") if values.get("distance_from_sun") is not None else values.get("semi_major_axis_au")
        values["distance_from_sun"] = dist
        values["semi_major_axis_au"] = dist

        p = values.get("orbital_period") if values.get("orbital_period") is not None else values.get("orbital_period_days")
        values["orbital_period"] = p
        values["orbital_period_days"] = p

        v = values.get("orbital_velocity") if values.get("orbital_velocity") is not None else values.get("mean_orbital_velocity_km_s")
        values["orbital_velocity"] = v
        values["mean_orbital_velocity_km_s"] = v

        parent = values.get("parent_object") if values.get("parent_object") is not None else values.get("parent_body_id")
        values["parent_object"] = parent
        values["parent_body_id"] = parent

        src = values.get("source") or values.get("data_source") or "NASA Planetary Fact Sheet / JPL Horizons"
        values["source"] = src
        values["data_source"] = src

        if not values.get("units"):
            values["units"] = dict(DEFAULT_UNITS)

        if not values.get("metadata"):
            values["metadata"] = values.get("research_notes") or {}

        if not values.get("orbital_parameters"):
            values["orbital_parameters"] = {
                "semi_major_axis_au": values.get("semi_major_axis_au"),
                "eccentricity": values.get("eccentricity"),
                "orbital_inclination_deg": values.get("orbital_inclination_deg"),
                "perihelion_au": values.get("perihelion_au"),
                "aphelion_au": values.get("aphelion_au")
            }

        return values

# API Response Models
class AstronomicalObjectBase(NormalizedCelestialBody):
    pass

class AstronomicalObjectSummary(BaseModel):
    id: str
    name: str
    category: str
    object_type: Optional[str] = None
    parent_body_id: Optional[str] = None
    parent_object: Optional[str] = None
    mass_earth_relative: Optional[float] = None
    radius_km: Optional[float] = None
    semi_major_axis_au: Optional[float] = None
    orbital_period_days: Optional[float] = None
    surface_temperature_k: Optional[float] = None
    color_hex: Optional[str] = "#94a3b8"
    description_citizen: Optional[str] = None
    description_student: Optional[str] = None
    description: Optional[str] = None
    data_source: Optional[str] = None
    source: Optional[str] = None

class AstronomicalObjectDetail(NormalizedCelestialBody):
    orbit_path_3d: Optional[List[List[float]]] = None
    astropy_units: Optional[AstropyUnitsBreakdown] = None
    related_objects: Optional[List[RelatedObjectSummary]] = None

class PaginatedCelestialResponse(BaseModel):
    items: List[AstronomicalObjectDetail]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

class SearchResultItem(BaseModel):
    id: str
    name: str
    category: str
    object_type: Optional[str] = None
    snippet: str
    match_field: str
    color_hex: Optional[str] = "#94a3b8"

class SearchResponse(BaseModel):
    query: str
    total_matches: int
    results: List[SearchResultItem]

class CompareRequest(BaseModel):
    object_ids: List[str] = Field(..., min_length=2, max_length=6)
    mode: Optional[str] = "researcher"

class CalculatedRatio(BaseModel):
    target_id: str
    target_name: str
    relative_to: str
    mass_ratio: Optional[float] = None
    radius_ratio: Optional[float] = None
    gravity_ratio: Optional[float] = None
    density_ratio: Optional[float] = None
    period_ratio: Optional[float] = None
    temperature_ratio: Optional[float] = None
    distance_ratio: Optional[float] = None
    velocity_ratio: Optional[float] = None

class DetailedComparisonResponse(BaseModel):
    compared_objects: List[AstronomicalObjectDetail]
    primary_reference: str
    calculated_ratios: List[CalculatedRatio]
    radar_chart_metrics: List[Dict[str, Any]]
    absolute_differences: List[Dict[str, Any]]
    comparative_insights: Optional[Dict[str, str]] = None
