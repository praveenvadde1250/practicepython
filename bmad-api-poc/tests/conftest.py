import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client() -> TestClient:
    # Fresh app + empty repository per test, so tests stay independent.
    return TestClient(create_app())
