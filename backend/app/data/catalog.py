from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, Base, engine
from app.db.models import AstronomicalObject
from app.data.seed_data import ASTRONOMICAL_CATALOG
import logging

logger = logging.getLogger(__name__)

DEFAULT_UNITS_DICT = {
    "mass": "kg",
    "radius": "km",
    "gravity": "m/s²",
    "distance_from_sun": "AU",
    "orbital_period": "days",
    "rotation_period": "hours",
    "orbital_velocity": "km/s",
    "temperature": "K"
}

def init_catalog_db():
    """Initializes tables and seeds initial data into SQLite database."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        count = db.query(AstronomicalObject).count()
        if count == 0:
            logger.info("Seeding astronomical catalog into SQLite database...")
            for item in ASTRONOMICAL_CATALOG:
                obj = AstronomicalObject(
                    id=item["id"],
                    name=item["name"],
                    category=item["category"],
                    object_type=item.get("object_type", item["category"]),
                    description=item.get("description", item.get("description_citizen")),
                    parent_body_id=item.get("parent_body_id"),
                    parent_object=item.get("parent_object", item.get("parent_body_id")),
                    mass=item.get("mass", item.get("mass_kg")),
                    radius=item.get("radius", item.get("radius_km")),
                    gravity=item.get("gravity", item.get("surface_gravity_m_s2")),
                    distance_from_sun=item.get("distance_from_sun", item.get("semi_major_axis_au")),
                    orbital_period=item.get("orbital_period", item.get("orbital_period_days")),
                    rotation_period=item.get("rotation_period"),
                    orbital_velocity=item.get("orbital_velocity", item.get("mean_orbital_velocity_km_s")),
                    temperature=item.get("temperature", item.get("surface_temperature_k")),
                    orbital_parameters=item.get("orbital_parameters", {
                        "semi_major_axis_au": item.get("semi_major_axis_au"),
                        "eccentricity": item.get("eccentricity"),
                        "orbital_inclination_deg": item.get("orbital_inclination_deg"),
                        "perihelion_au": item.get("perihelion_au"),
                        "aphelion_au": item.get("aphelion_au")
                    }),
                    discovery_information=item.get("discovery_information", {}),
                    source=item.get("source", item.get("data_source", "NASA Planetary Fact Sheet / JPL Horizons")),
                    source_url=item.get("source_url", "https://nssdc.gsfc.nasa.gov/planetary/factsheet/"),
                    units=item.get("units", DEFAULT_UNITS_DICT),
                    metadata_json=item.get("metadata", item.get("research_notes", {})),
                    mass_kg=item.get("mass_kg", item.get("mass")),
                    mass_earth_relative=item.get("mass_earth_relative"),
                    radius_km=item.get("radius_km", item.get("radius")),
                    radius_earth_relative=item.get("radius_earth_relative"),
                    mean_density_g_cm3=item.get("mean_density_g_cm3"),
                    surface_gravity_m_s2=item.get("surface_gravity_m_s2", item.get("gravity")),
                    escape_velocity_km_s=item.get("escape_velocity_km_s"),
                    surface_temperature_k=item.get("surface_temperature_k", item.get("temperature")),
                    luminosity_solar=item.get("luminosity_solar"),
                    spectral_type=item.get("spectral_type"),
                    apparent_magnitude=item.get("apparent_magnitude"),
                    absolute_magnitude=item.get("absolute_magnitude"),
                    semi_major_axis_au=item.get("semi_major_axis_au", item.get("distance_from_sun")),
                    eccentricity=item.get("eccentricity"),
                    orbital_inclination_deg=item.get("orbital_inclination_deg"),
                    orbital_period_days=item.get("orbital_period_days", item.get("orbital_period")),
                    perihelion_au=item.get("perihelion_au"),
                    aphelion_au=item.get("aphelion_au"),
                    mean_orbital_velocity_km_s=item.get("mean_orbital_velocity_km_s", item.get("orbital_velocity")),
                    color_hex=item.get("color_hex", "#94a3b8"),
                    texture_preset=item.get("texture_preset", "generic"),
                    has_rings=item.get("has_rings", False),
                    has_atmosphere=item.get("has_atmosphere", False),
                    description_citizen=item.get("description_citizen", item.get("description", "")),
                    description_student=item.get("description_student", item.get("description", "")),
                    description_researcher=item.get("description_researcher", item.get("description", "")),
                    educational_facts=item.get("educational_facts", []),
                    research_notes=item.get("research_notes", {}),
                    data_source=item.get("data_source", item.get("source", "NASA Planetary Fact Sheet / JPL Horizons")),
                    data_confidence=item.get("data_confidence", "High")
                )
                db.add(obj)
            db.commit()
            logger.info(f"Successfully seeded {len(ASTRONOMICAL_CATALOG)} astronomical objects into SQLite.")
    finally:
        db.close()

def get_all_objects(db: Session, category: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
    query = db.query(AstronomicalObject)
    if category and category.lower() != "all":
        query = query.filter(
            (AstronomicalObject.category.ilike(category)) |
            (AstronomicalObject.object_type.ilike(category))
        )
    if search:
        query = query.filter(
            (AstronomicalObject.name.ilike(f"%{search}%")) |
            (AstronomicalObject.id.ilike(f"%{search}%"))
        )
    
    rows = query.all()
    if not rows and not search and (not category or category == "all"):
        return [enrich_catalog_item(item) for item in ASTRONOMICAL_CATALOG]
    
    return [object_to_dict(r) for r in rows]

def get_object_by_id(db: Session, object_id: str) -> Optional[Dict[str, Any]]:
    row = db.query(AstronomicalObject).filter(AstronomicalObject.id == object_id).first()
    if row:
        return object_to_dict(row)
    for item in ASTRONOMICAL_CATALOG:
        if item["id"] == object_id:
            return enrich_catalog_item(item)
    return None

def enrich_catalog_item(item: Dict[str, Any]) -> Dict[str, Any]:
    d = dict(item)
    d["object_type"] = d.get("object_type", d.get("category", "Generic"))
    d["category"] = d.get("category", d.get("object_type", "Generic"))
    d["description"] = d.get("description") or d.get("description_citizen") or d.get("description_student") or ""
    d["mass"] = d.get("mass", d.get("mass_kg"))
    d["radius"] = d.get("radius", d.get("radius_km"))
    d["gravity"] = d.get("gravity", d.get("surface_gravity_m_s2"))
    d["distance_from_sun"] = d.get("distance_from_sun", d.get("semi_major_axis_au"))
    d["orbital_period"] = d.get("orbital_period", d.get("orbital_period_days"))
    d["orbital_velocity"] = d.get("orbital_velocity", d.get("mean_orbital_velocity_km_s"))
    d["temperature"] = d.get("temperature", d.get("surface_temperature_k"))
    d["parent_object"] = d.get("parent_object", d.get("parent_body_id"))
    d["source"] = d.get("source", d.get("data_source", "NASA Planetary Fact Sheet / JPL Horizons"))
    d["source_url"] = d.get("source_url", "https://nssdc.gsfc.nasa.gov/planetary/factsheet/")
    d["units"] = d.get("units", DEFAULT_UNITS_DICT)
    d["metadata"] = d.get("metadata", d.get("research_notes", {}))
    if "orbital_parameters" not in d:
        d["orbital_parameters"] = {
            "semi_major_axis_au": d.get("semi_major_axis_au"),
            "eccentricity": d.get("eccentricity"),
            "orbital_inclination_deg": d.get("orbital_inclination_deg"),
            "perihelion_au": d.get("perihelion_au"),
            "aphelion_au": d.get("aphelion_au")
        }
    if "discovery_information" not in d:
        d["discovery_information"] = {}
    return d

def object_to_dict(obj: AstronomicalObject) -> Dict[str, Any]:
    obj_type = obj.object_type or obj.category
    desc = obj.description or obj.description_citizen
    return {
        "id": obj.id,
        "name": obj.name,
        "category": obj.category,
        "object_type": obj_type,
        "description": desc,
        "parent_body_id": obj.parent_body_id,
        "parent_object": obj.parent_object or obj.parent_body_id,
        "mass": obj.mass if obj.mass is not None else obj.mass_kg,
        "radius": obj.radius if obj.radius is not None else obj.radius_km,
        "gravity": obj.gravity if obj.gravity is not None else obj.surface_gravity_m_s2,
        "distance_from_sun": obj.distance_from_sun if obj.distance_from_sun is not None else obj.semi_major_axis_au,
        "orbital_period": obj.orbital_period if obj.orbital_period is not None else obj.orbital_period_days,
        "rotation_period": obj.rotation_period,
        "orbital_velocity": obj.orbital_velocity if obj.orbital_velocity is not None else obj.mean_orbital_velocity_km_s,
        "temperature": obj.temperature if obj.temperature is not None else obj.surface_temperature_k,
        "orbital_parameters": obj.orbital_parameters or {
            "semi_major_axis_au": obj.semi_major_axis_au,
            "eccentricity": obj.eccentricity,
            "orbital_inclination_deg": obj.orbital_inclination_deg,
            "perihelion_au": obj.perihelion_au,
            "aphelion_au": obj.aphelion_au
        },
        "discovery_information": obj.discovery_information or {},
        "source": obj.source or obj.data_source,
        "source_url": obj.source_url or "https://nssdc.gsfc.nasa.gov/planetary/factsheet/",
        "units": obj.units or DEFAULT_UNITS_DICT,
        "metadata": obj.metadata_json or obj.research_notes or {},
        "mass_kg": obj.mass_kg,
        "mass_earth_relative": obj.mass_earth_relative,
        "radius_km": obj.radius_km,
        "radius_earth_relative": obj.radius_earth_relative,
        "mean_density_g_cm3": obj.mean_density_g_cm3,
        "surface_gravity_m_s2": obj.surface_gravity_m_s2,
        "escape_velocity_km_s": obj.escape_velocity_km_s,
        "surface_temperature_k": obj.surface_temperature_k,
        "luminosity_solar": obj.luminosity_solar,
        "spectral_type": obj.spectral_type,
        "apparent_magnitude": obj.apparent_magnitude,
        "absolute_magnitude": obj.absolute_magnitude,
        "semi_major_axis_au": obj.semi_major_axis_au,
        "eccentricity": obj.eccentricity,
        "orbital_inclination_deg": obj.orbital_inclination_deg,
        "orbital_period_days": obj.orbital_period_days,
        "perihelion_au": obj.perihelion_au,
        "aphelion_au": obj.aphelion_au,
        "mean_orbital_velocity_km_s": obj.mean_orbital_velocity_km_s,
        "color_hex": obj.color_hex,
        "texture_preset": obj.texture_preset,
        "has_rings": obj.has_rings,
        "has_atmosphere": obj.has_atmosphere,
        "description_citizen": obj.description_citizen,
        "description_student": obj.description_student,
        "description_researcher": obj.description_researcher,
        "educational_facts": obj.educational_facts or [],
        "research_notes": obj.research_notes or {},
        "data_source": obj.data_source,
        "data_confidence": obj.data_confidence
    }
