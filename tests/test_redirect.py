import pytest
from unittest.mock import AsyncMock

from app.services import cache_service as cache_module


@pytest.mark.anyio
async def test_redirect_success_301(client, monkeypatch):
    # Mock increment_visits to avoid Redis interaction
    monkeypatch.setattr(cache_module.CacheService, "increment_visits", AsyncMock(return_value=None))

    # First create a short URL
    payload = {"long_link": "https://www.python.org/"}
    r = await client.post("/short_url", json=payload)
    assert r.status_code in (200, 201)
    short_link = r.json()["short_link"]
    short_code = short_link.rsplit("/", 1)[-1]

    # Then request redirect
    resp = await client.get(f"/{short_code}", follow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers["location"] == payload["long_link"]


@pytest.mark.anyio
async def test_redirect_invalid_short_code_404(client, monkeypatch):
    monkeypatch.setattr(cache_module.CacheService, "increment_visits", AsyncMock(return_value=None))

    resp = await client.get("/!!!", follow_redirects=False)
    assert resp.status_code == 404
