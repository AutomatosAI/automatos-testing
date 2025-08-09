import os
import requests

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
OPENAPI_PATH = os.getenv("OPENAPI_PATH", "/openapi.json")


def test_health_ok():
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert "status" in data


def test_openapi_available():
    r = requests.get(f"{BASE_URL}{OPENAPI_PATH}", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert "openapi" in data


