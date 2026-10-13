from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.schemas.celestial import NormalizedCelestialBody, SourceMetadata

class AstronomyDataProvider(ABC):
    """
    Abstract base class for all astronomical data providers.
    Ensures provider-agnostic access with strict offline guarantees.
    """
    @property
    @abstractmethod
    def provider_id(self) -> str:
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    def get_source_metadata(self) -> SourceMetadata:
        pass

    @abstractmethod
    async def fetch_all_objects(self) -> List[NormalizedCelestialBody]:
        pass

    @abstractmethod
    async def fetch_object_by_id(self, object_id: str) -> Optional[NormalizedCelestialBody]:
        pass

    async def search_objects(self, query: str, limit: int = 10) -> List[NormalizedCelestialBody]:
        """Search objects by name, slug, or category."""
        objs = await self.fetch_all_objects()
        q = query.lower().strip()
        if not q:
            return objs[:limit]
        matched = [
            o for o in objs
            if q in o.name.lower() or q in o.id.lower() or (o.category and q in o.category.lower())
        ]
        return matched[:limit]

    async def filter_by_type(self, object_type: str) -> List[NormalizedCelestialBody]:
        """Filter celestial objects by object type or category."""
        objs = await self.fetch_all_objects()
        target = object_type.lower().strip()
        return [
            o for o in objs
            if (o.object_type and o.object_type.lower() == target) or (o.category and o.category.lower() == target)
        ]

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        pass
