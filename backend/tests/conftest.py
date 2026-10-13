import pytest
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app
from app.data.catalog import init_catalog_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_catalog_db()

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
