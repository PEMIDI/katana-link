import pytest


@pytest.mark.anyio
async def test_create_short_url_creates_new_201(client):
    payload = {"long_link": "https://example.com/path?a=1"}
    r = await client.post("/short_url", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["long_link"] == payload["long_link"]
    assert data["short_link"].startswith("http://testserver/")
    # short code should be the last path segment
    short_code = data["short_link"].split("/")[-1]
    assert short_code  # non-empty


@pytest.mark.anyio
async def test_create_short_url_idempotent_200_same_link(client):
    payload = {"long_link": "https://example.com/idempotent"}

    r1 = await client.post("/short_url", json=payload)
    assert r1.status_code == 201
    link1 = r1.json()["short_link"]

    r2 = await client.post("/short_url", json=payload)
    assert r2.status_code == 200
    link2 = r2.json()["short_link"]

    assert link1 == link2
