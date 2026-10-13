from sqlalchemy import Column, String, Float, Integer, Text, DateTime, JSON, Boolean
from datetime import datetime
from app.db.database import Base

class AstronomicalObject(Base):
    __tablename__ = "astronomical_objects"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(128), nullable=False, index=True)
    category = Column(String(64), nullable=False, index=True) # Planet, Star, Exoplanet, Moon, Deep-Sky, Asteroid, Comet
    object_type = Column(String(64), nullable=True, index=True)
    description = Column(Text, nullable=True)
    parent_body_id = Column(String(64), nullable=True, index=True)
    parent_object = Column(String(64), nullable=True, index=True)
    
    # Normalized & Numeric Physical Fields
    mass = Column(Float, nullable=True)
    radius = Column(Float, nullable=True)
    gravity = Column(Float, nullable=True)
    distance_from_sun = Column(Float, nullable=True)
    orbital_period = Column(Float, nullable=True)
    rotation_period = Column(Float, nullable=True)
    orbital_velocity = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    orbital_parameters = Column(JSON, default=dict)
    discovery_information = Column(JSON, default=dict)
    source = Column(String(128), nullable=True)
    source_url = Column(String(256), nullable=True)
    units = Column(JSON, default=dict)
    metadata_json = Column(JSON, default=dict)
    
    # Physical Characteristics
    mass_kg = Column(Float, nullable=True)
    mass_earth_relative = Column(Float, nullable=True)
    radius_km = Column(Float, nullable=True)
    radius_earth_relative = Column(Float, nullable=True)
    mean_density_g_cm3 = Column(Float, nullable=True)
    surface_gravity_m_s2 = Column(Float, nullable=True)
    escape_velocity_km_s = Column(Float, nullable=True)
    surface_temperature_k = Column(Float, nullable=True)
    luminosity_solar = Column(Float, nullable=True)
    spectral_type = Column(String(32), nullable=True)
    apparent_magnitude = Column(Float, nullable=True)
    absolute_magnitude = Column(Float, nullable=True)
    
    # Orbital Parameters (Keplerian)
    semi_major_axis_au = Column(Float, nullable=True)
    eccentricity = Column(Float, nullable=True)
    orbital_inclination_deg = Column(Float, nullable=True)
    orbital_period_days = Column(Float, nullable=True)
    perihelion_au = Column(Float, nullable=True)
    aphelion_au = Column(Float, nullable=True)
    mean_orbital_velocity_km_s = Column(Float, nullable=True)
    ascending_node_deg = Column(Float, default=0.0)
    arg_periapsis_deg = Column(Float, default=0.0)
    mean_anomaly_epoch_deg = Column(Float, default=0.0)

    # Visual Appearance
    color_hex = Column(String(16), default="#94a3b8")
    texture_preset = Column(String(64), default="generic")
    has_rings = Column(Boolean, default=False)
    has_atmosphere = Column(Boolean, default=False)

    # Adaptive Content
    description_citizen = Column(Text, nullable=False)
    description_student = Column(Text, nullable=False)
    description_researcher = Column(Text, nullable=False)
    educational_facts = Column(JSON, default=list) # List of interesting facts for students/citizens
    research_notes = Column(JSON, default=dict) # Scientific notes, formulas, references
    
    data_source = Column(String(128), default="NASA Planetary Fact Sheet / JPL Horizons")
    data_confidence = Column(String(32), default="High")
    updated_at = Column(DateTime, default=datetime.utcnow)

AstronomicalObjectModel = AstronomicalObject

class SimulationRunRecord(Base):
    __tablename__ = "simulation_runs"

    id = Column(String(64), primary_key=True)
    scenario_id = Column(String(64), index=True)
    integrator = Column(String(32))
    timestep_days = Column(Float)
    total_time_days = Column(Float)
    num_particles = Column(Integer)
    max_energy_error = Column(Float)
    runtime_ms = Column(Float)
    steps_computed = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class EvaluationRecord(Base):
    __tablename__ = "evaluation_records"

    id = Column(String(64), primary_key=True)
    query = Column(String(256), nullable=False)
    target_object_id = Column(String(64), nullable=True)
    researcher_metrics = Column(JSON, nullable=False)
    student_metrics = Column(JSON, nullable=False)
    citizen_metrics = Column(JSON, nullable=False)
    computation_benchmark = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserBookmark(Base):
    __tablename__ = "user_bookmarks"

    id = Column(String(64), primary_key=True)
    object_id = Column(String(64), nullable=False)
    mode = Column(String(32), default="citizen")
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TelemetryRecord(Base):
    __tablename__ = "telemetry_records"

    id = Column(String(64), primary_key=True)
    event_type = Column(String(64), nullable=False, index=True)
    component = Column(String(64), nullable=True)
    duration_ms = Column(Float, nullable=True)
    success = Column(Boolean, nullable=True)
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)


class TaskExecutionRecord(Base):
    __tablename__ = "task_execution_records"

    id = Column(String(64), primary_key=True)
    task_id = Column(String(64), nullable=False, index=True)
    task_name = Column(String(128), nullable=False)
    category = Column(String(64), nullable=False)
    status = Column(String(32), default="pending")
    success = Column(Boolean, default=False)
    duration_ms = Column(Float, default=0.0)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    verification_details = Column(JSON, default=dict)

