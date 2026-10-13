from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Union
import math
from app.db.database import get_db
from app.services.catalog_service import catalog_service
from app.scientific.ephemeris import generate_orbit_path_points, propagate_ephemeris
from app.schemas.celestial import (
    AstronomicalObjectDetail,
    PaginatedCelestialResponse,
    SearchResponse
)

router = APIRouter(prefix="/objects", tags=["Astronomical Objects"])

@router.get("/search", response_model=SearchResponse)
def search_objects_endpoint(
    q: str = Query(..., min_length=1, description="Search term for celestial objects"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Search celestial catalog by name, identifier, category, or spectral classification."""
    return catalog_service.search_objects(db, query=q, limit=limit)

@router.get("/type/{type_name}")
def get_objects_by_type_endpoint(
    type_name: str,
    db: Session = Depends(get_db)
):
    """Retrieve all celestial objects matching a specific category (e.g., Planet, Moon, Star, Exoplanet)."""
    results = catalog_service.get_objects_by_type(db, object_type=type_name)
    if not results:
        raise HTTPException(status_code=404, detail=f"No celestial objects found for category '{type_name}'.")
    return results

@router.get("/")
def list_objects(
    category: Optional[str] = Query(None, description="Filter by category (Planet, Star, Exoplanet, Moon, Deep-Sky, Asteroid, Comet)"),
    object_type: Optional[str] = Query(None, description="Alias for category filter"),
    search: Optional[str] = Query(None, description="Search by object name"),
    sort_by: Optional[str] = Query("distance", description="Sort field: distance, mass, radius, period, temperature, name"),
    sort_order: Optional[str] = Query("asc", description="Sort direction: asc or desc"),
    min_mass: Optional[float] = Query(None, description="Minimum Earth-relative mass"),
    max_mass: Optional[float] = Query(None, description="Maximum Earth-relative mass"),
    min_radius: Optional[float] = Query(None, description="Minimum radius in km"),
    max_radius: Optional[float] = Query(None, description="Maximum radius in km"),
    has_rings: Optional[bool] = Query(None, description="Filter by ring system presence"),
    has_atmosphere: Optional[bool] = Query(None, description="Filter by atmosphere presence"),
    page: Optional[int] = Query(None, ge=1, description="Page number for pagination"),
    page_size: Optional[int] = Query(None, ge=1, le=100, description="Items per page"),
    format: Optional[str] = Query(None, description="Response format: 'paginated' or 'list'"),
    db: Session = Depends(get_db)
):
    """
    Retrieve astronomical objects with filtering, sorting, and optional pagination.
    Returns a paginated envelope when 'page' or 'format=paginated' is specified;
    otherwise returns a direct list of objects for client flexibility.
    """
    is_paginated_requested = page is not None or page_size is not None or format == "paginated"
    current_page = page or 1
    current_page_size = page_size or 20

    items, total_count = catalog_service.list_objects(
        db,
        category=category,
        object_type=object_type,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        min_mass=min_mass,
        max_mass=max_mass,
        min_radius=min_radius,
        max_radius=max_radius,
        has_rings=has_rings,
        has_atmosphere=has_atmosphere,
        page=current_page if is_paginated_requested else None,
        page_size=current_page_size if is_paginated_requested else None
    )

    if is_paginated_requested:
        total_pages = math.ceil(total_count / current_page_size) if total_count > 0 else 1
        return {
            "items": items,
            "total": total_count,
            "page": current_page,
            "page_size": current_page_size,
            "total_pages": total_pages,
            "has_next": current_page < total_pages,
            "has_prev": current_page > 1
        }

    return items

@router.get("/{object_id}")
def get_object_details(object_id: str, db: Session = Depends(get_db)):
    """
    Retrieve full astronomical parameters, 3D orbit polyline, Astropy units,
    related objects, and source metadata for an object.
    """
    return catalog_service.get_object_by_id(db, object_id)

@router.get("/{object_id}/orbit-path")
def get_orbit_path(object_id: str, samples: int = 120, db: Session = Depends(get_db)):
    """Retrieve 3D polyline coordinate points for the object's Keplerian orbit."""
    return catalog_service.get_orbit_path(db, object_id, samples=samples)

@router.get("/{object_id}/ephemeris")
def get_ephemeris_propagation(object_id: str, elapsed_days: float = 0.0, db: Session = Depends(get_db)):
    """Propagate the object along its orbit at a given elapsed time in days."""
    return catalog_service.propagate(db, object_id, elapsed_days=elapsed_days)
