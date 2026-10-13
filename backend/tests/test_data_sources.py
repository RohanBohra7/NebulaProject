import pytest
import asyncio
from app.data.providers.local_provider import LocalDataProvider
from app.data.providers.nasa_provider import NASAProvider
from app.data.providers.simbad_provider import SIMBADProvider
from app.data.providers.composite_provider import CompositeDataProvider

def test_local_data_provider():
    async def _test():
        provider = LocalDataProvider()
        assert provider.provider_id == "local_curated"
        objects = await provider.fetch_all_objects()
        assert len(objects) >= 20
        earth = await provider.fetch_object_by_id("earth")
        assert earth is not None
        assert earth.name == "Earth"
        assert earth.source_metadata is not None
        assert earth.source_metadata.is_demo_seed is True
    asyncio.run(_test())

def test_nasa_provider_fallback():
    async def _test():
        provider = NASAProvider()
        assert provider.provider_id == "nasa_exoplanet_archive"
        objects = await provider.fetch_all_objects()
        assert len(objects) >= 1
        for o in objects:
            assert o.category == "Exoplanet"
    asyncio.run(_test())

def test_composite_provider():
    async def _test():
        composite = CompositeDataProvider()
        objects = await composite.get_all_objects()
        assert len(objects) >= 20
        ids = [o.id for o in objects]
        assert len(ids) == len(set(ids))
    asyncio.run(_test())

def test_data_status_endpoint(client):
    res = client.get("/api/v1/data/status")
    assert res.status_code == 200
    data = res.json()
    assert "sources" in data
    assert len(data["sources"]) >= 3
    assert data["offline_ready"] is True
