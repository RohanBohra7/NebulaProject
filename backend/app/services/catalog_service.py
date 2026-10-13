from typing import List, Optional, Dict, Any, Tuple
import math
from sqlalchemy.orm import Session
from app.data.catalog import get_all_objects, get_object_by_id
from app.scientific.ephemeris import generate_orbit_path_points, propagate_ephemeris
from app.scientific.astropy_bridge import compute_astropy_units, find_related_objects
from app.data.validation import validate_catalog, DataQualityReport
from app.core.exceptions import AstronomicalObjectNotFoundError
from app.schemas.celestial import (
    AstronomicalObjectDetail,
    AstronomicalObjectSummary,
    PaginatedCelestialResponse,
    SearchResponse,
    SearchResultItem,
    SourceMetadata
)

class CatalogService:
    @staticmethod
    def get_all_raw(db: Session) -> List[Dict[str, Any]]:
        return get_all_objects(db)

    @classmethod
    def list_objects(
        cls,
        db: Session,
        category: Optional[str] = None,
        object_type: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = "distance",
        sort_order: Optional[str] = "asc",
        min_mass: Optional[float] = None,
        max_mass: Optional[float] = None,
        min_radius: Optional[float] = None,
        max_radius: Optional[float] = None,
        has_rings: Optional[bool] = None,
        has_atmosphere: Optional[bool] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Retrieves, filters, sorts, and optionally paginates astronomical objects.
        """
        raw_objects = get_all_objects(db)
        cat_filter = (category or object_type or "").strip()

        filtered: List[Dict[str, Any]] = []
        for obj in raw_objects:
            # Category filter
            if cat_filter and cat_filter.lower() != "all":
                if obj["category"].lower() != cat_filter.lower():
                    continue

            # Search filter
            if search:
                s = search.lower().strip()
                matches_name = s in obj["name"].lower()
                matches_id = s in obj["id"].lower()
                matches_cat = s in obj["category"].lower()
                matches_desc = s in obj.get("description_citizen", "").lower()
                if not (matches_name or matches_id or matches_cat or matches_desc):
                    continue

            # Physical filters
            if min_mass is not None and (obj.get("mass_earth_relative") is None or obj["mass_earth_relative"] < min_mass):
                continue
            if max_mass is not None and (obj.get("mass_earth_relative") is None or obj["mass_earth_relative"] > max_mass):
                continue
            if min_radius is not None and (obj.get("radius_km") is None or obj["radius_km"] < min_radius):
                continue
            if max_radius is not None and (obj.get("radius_km") is None or obj["radius_km"] > max_radius):
                continue
            if has_rings is not None and obj.get("has_rings") != has_rings:
                continue
            if has_atmosphere is not None and obj.get("has_atmosphere") != has_atmosphere:
                continue

            filtered.append(obj)

        # Sorting
        reverse = (sort_order or "asc").lower() == "desc"
        sort_key = (sort_by or "distance").lower()

        if sort_key == "name":
            filtered.sort(key=lambda x: x["name"].lower(), reverse=reverse)
        elif sort_key == "mass":
            filtered.sort(key=lambda x: (x.get("mass_earth_relative") is not None, x.get("mass_earth_relative") or 0.0), reverse=reverse)
        elif sort_key == "radius":
            filtered.sort(key=lambda x: (x.get("radius_km") is not None, x.get("radius_km") or 0.0), reverse=reverse)
        elif sort_key == "period":
            filtered.sort(key=lambda x: (x.get("orbital_period_days") is not None, x.get("orbital_period_days") or 0.0), reverse=reverse)
        elif sort_key == "temperature":
            filtered.sort(key=lambda x: (x.get("surface_temperature_k") is not None, x.get("surface_temperature_k") or 0.0), reverse=reverse)
        else: # Default: distance / semi_major_axis
            filtered.sort(key=lambda x: (x.get("semi_major_axis_au") is not None, x.get("semi_major_axis_au") or 0.0), reverse=reverse)

        total_count = len(filtered)

        # Pagination if requested
        if page is not None and page_size is not None and page_size > 0:
            start_idx = max(0, (page - 1) * page_size)
            end_idx = start_idx + page_size
            paginated = filtered[start_idx:end_idx]
            return paginated, total_count

        return filtered, total_count

    @classmethod
    def get_object_by_id(cls, db: Session, object_id: str) -> Dict[str, Any]:
        obj = get_object_by_id(db, object_id)
        if not obj:
            raise AstronomicalObjectNotFoundError(object_id)

        all_objects = get_all_objects(db)

        # 1. Generate 3D orbit polyline points
        orbit_path = []
        if obj.get("semi_major_axis_au") and obj.get("eccentricity") is not None:
            orbit_path = generate_orbit_path_points(
                semi_major_axis_au=obj["semi_major_axis_au"],
                eccentricity=obj["eccentricity"],
                inclination_deg=obj.get("orbital_inclination_deg", 0.0),
                num_samples=120
            )

        # 2. Astropy unit conversions
        astropy_units = compute_astropy_units(obj)

        # 3. Related bodies
        related_objs = find_related_objects(object_id, all_objects)

        # 4. Source metadata
        source_meta = SourceMetadata(
            source_name=obj.get("data_source", "NASA Planetary Fact Sheet / JPL Horizons"),
            source_url="https://nssdc.gsfc.nasa.gov/planetary/factsheet/" if obj.get("category") in ["Planet", "Moon"] else "https://exoplanetarchive.ipac.caltech.edu/",
            retrieval_date="2026-10-06",
            is_demo_seed=True,
            confidence_level=obj.get("data_confidence", "High"),
            provenance_badge="Verified Local Primary"
        )

        return {
            **obj,
            "orbit_path_3d": orbit_path,
            "astropy_units": astropy_units.model_dump(),
            "related_objects": [r.model_dump() for r in related_objs],
            "source_metadata": source_meta.model_dump()
        }

    @classmethod
    def search_objects(cls, db: Session, query: str, limit: int = 10) -> SearchResponse:
        raw_objects = get_all_objects(db)
        q = query.lower().strip()
        matches: List[SearchResultItem] = []

        if not q:
            return SearchResponse(query=query, total_matches=0, results=[])

        for obj in raw_objects:
            match_field = None
            snippet = None

            if q in obj["name"].lower():
                match_field = "name"
                snippet = f"{obj['name']} ({obj['category']})"
            elif q in obj["id"].lower():
                match_field = "id"
                snippet = f"ID: {obj['id']}"
            elif q in obj["category"].lower():
                match_field = "category"
                snippet = f"Category: {obj['category']}"
            elif obj.get("spectral_type") and q in obj["spectral_type"].lower():
                match_field = "spectral_type"
                snippet = f"Spectral class {obj['spectral_type']}"
            elif q in obj.get("description_citizen", "").lower():
                match_field = "description"
                snippet = obj["description_citizen"][:120] + "..."

            if match_field:
                matches.append(SearchResultItem(
                    id=obj["id"],
                    name=obj["name"],
                    category=obj["category"],
                    snippet=snippet or f"{obj['name']} ({obj['category']})",
                    match_field=match_field,
                    color_hex=obj.get("color_hex", "#94a3b8")
                ))
                if len(matches) >= limit:
                    break

        return SearchResponse(
            query=query,
            total_matches=len(matches),
            results=matches
        )

    @classmethod
    def get_objects_by_type(cls, db: Session, object_type: str) -> List[Dict[str, Any]]:
        raw_objects = get_all_objects(db)
        target_type = object_type.lower().strip()
        matched = [
            o for o in raw_objects
            if (o.get("object_type", "").lower() == target_type) or (o.get("category", "").lower() == target_type)
        ]
        if not matched:
            # Check if partial match or plural (e.g. "planets" -> "planet")
            singular = target_type.rstrip('s')
            matched = [
                o for o in raw_objects
                if (o.get("object_type", "").lower() == singular) or (o.get("category", "").lower() == singular)
            ]
        return matched

    @classmethod
    def validate_catalog(cls, db: Session) -> DataQualityReport:
        objects = get_all_objects(db)
        return validate_catalog(objects)

    @classmethod
    def get_orbit_path(cls, db: Session, object_id: str, samples: int = 120) -> List[List[float]]:
        obj = get_object_by_id(db, object_id)
        if not obj:
            raise AstronomicalObjectNotFoundError(object_id)
        if not obj.get("semi_major_axis_au") or obj.get("eccentricity") is None:
            return [[0.0, 0.0, 0.0]]
        return generate_orbit_path_points(
            semi_major_axis_au=obj["semi_major_axis_au"],
            eccentricity=obj["eccentricity"],
            inclination_deg=obj.get("orbital_inclination_deg", 0.0),
            num_samples=samples
        )

    @classmethod
    def propagate(cls, db: Session, object_id: str, elapsed_days: float = 0.0) -> Dict[str, Any]:
        obj = get_object_by_id(db, object_id)
        if not obj:
            raise AstronomicalObjectNotFoundError(object_id)
        if not obj.get("semi_major_axis_au") or not obj.get("orbital_period_days"):
            return {
                "object_id": object_id,
                "elapsed_days": elapsed_days,
                "position_au": [0.0, 0.0, 0.0],
                "velocity_km_s": [0.0, 0.0, 0.0]
            }
        coords = propagate_ephemeris(
            semi_major_axis_au=obj["semi_major_axis_au"],
            eccentricity=obj.get("eccentricity", 0.0),
            orbital_period_days=obj["orbital_period_days"],
            inclination_deg=obj.get("orbital_inclination_deg", 0.0),
            elapsed_time_days=elapsed_days
        )
        return {
            "object_id": object_id,
            "elapsed_days": elapsed_days,
            **coords
        }

catalog_service = CatalogService()
