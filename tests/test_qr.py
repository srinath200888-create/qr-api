import base64
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"


def test_generate_png():
    resp = client.post("/v1/generate", json={"text": "https://example.com"})
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/png"
    assert len(resp.content) > 100


def test_generate_svg():
    resp = client.post(
        "/v1/generate", json={"text": "hello", "format": "svg"}
    )
    assert resp.status_code == 200
    assert "image/svg+xml" in resp.headers["content-type"]


def test_generate_custom_colors():
    resp = client.post(
        "/v1/generate",
        json={
            "text": "test",
            "color": "#FF0000",
            "bg_color": "#000000",
        },
    )
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/png"


def test_generate_with_logo():
    small_img = base64.b64encode(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100).decode()
    resp = client.post(
        "/v1/generate",
        json={"text": "test", "logo": small_img},
    )
    assert resp.status_code == 200


def test_generate_invalid_color():
    resp = client.post(
        "/v1/generate",
        json={"text": "test", "color": "red"},
    )
    assert resp.status_code == 422


def test_generate_empty_text():
    resp = client.post(
        "/v1/generate",
        json={"text": ""},
    )
    assert resp.status_code == 422


def test_generate_bulk():
    resp = client.post(
        "/v1/generate/bulk",
        json={
            "items": [
                {"text": "first"},
                {"text": "second", "color": "#FF0000"},
            ]
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert len(data["data"]) == 2
    assert data["data"][0]["qr"] is not None
    assert data["data"][1]["qr"] is not None


def test_generate_bulk_too_many():
    resp = client.post(
        "/v1/generate/bulk",
        json={"items": [{"text": f"item-{i}"} for i in range(101)]},
    )
    assert resp.status_code == 422


def test_rate_limit():
    client.post("/v1/generate", json={"text": "test"})
