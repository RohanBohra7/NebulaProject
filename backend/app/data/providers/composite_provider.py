from typing import List, Dict, Any, Optional
from app.data.providers.base import AstronomyDataProvider
from app.data.providers.local_provider import LocalDataProvider
from app.data.providers.nasa_provider import NASAProvider
from app.data.providers.simbad_provider import SIMBADProvider
from app.schemas.celestial import NormalizedCelestialBody

class CompositeDataProvider:
    """
    Unified manager and registry for all astronomical data providers.
    Coordinates local primary cache and external sources, ensuring zero duplication.
    """
    def __init__(self):
        self.local_provider = LocalDataProvider()
        self.nasa_provider = NASAProvider()
        self.simbad_provider = SIMBADProvider()
        self.providers: List[AstronomyDataProvider] = [
            self.local_provider,
            self.nasa_provider,
            self.simbad_provider
        ]

    async def get_all_objects(self) -> List[NormalizedCelestialBody]:
        # Always prioritize local verified catalog
        objects_dict: Dict[str, NormalizedCelestialBody] = {}
        
        # 1. Load local catalog
        local_objs = await self.local_provider.fetch_all_objects()
        for o in local_objs:
            objects_dict[o.id] = o

        # 2. Merge non-duplicate remote objects
        nasa_objs = await self.nasa_provider.fetch_all_objects()
        for o in nasa_objs:
            if o.id not in objects_dict:
                objects_dict[o.id] = o

        simbad_objs = await self.simbad_provider.fetch_all_objects()
        for o in simbad_objs:
            if o.id not in objects_dict:
                objects_dict[o.id] = o

        return list(objects_dict.values())

    async def get_object_by_id(self, object_id: str) -> Optional[NormalizedCelestialBody]:
        # Check local first
        obj = await self.local_provider.fetch_object_by_id(object_id)
        if obj:
            return obj
        
        # Check remote providers
        obj = await self.nasa_provider.fetch_object_by_id(object_id)
        if obj:
            return obj
            
        obj = await self.simbad_provider.fetch_object_by_id(object_id)
        return obj

    async def get_providers_status(self) -> List[Dict[str, Any]]:
        statuses = []
        for p in self.providers:
            st = await p.health_check()
            meta = p.get_source_metadata()
            statuses.append({
                **st,
                "provider_name": p.provider_name,
                "source_url": meta.source_url,
                "provenance_badge": meta.provenance_badge,
                "confidence_level": meta.confidence_level
            })
        return statuses

composite_provider = CompositeDataProvider()
