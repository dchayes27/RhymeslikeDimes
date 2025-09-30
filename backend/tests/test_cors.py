import sys
from pathlib import Path

from fastapi.testclient import TestClient

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BACKEND_DIR))
sys.path.append(str(BACKEND_DIR / "app"))

from app.main import app

client = TestClient(app)


def _make_preflight_request(origin: str):
    return client.options(
        "/api/health",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )


def test_vercel_preview_origin_is_allowed():
    preview_origin = "https://feature-123--rhymeslikedimes.vercel.app"
    response = _make_preflight_request(preview_origin)

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == preview_origin


def test_production_origin_remains_whitelisted():
    production_origin = "https://rhymeslikedimes.vercel.app"
    response = _make_preflight_request(production_origin)

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == production_origin
