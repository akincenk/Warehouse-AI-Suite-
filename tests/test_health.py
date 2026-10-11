def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_ping(client):
    assert client.get("/api/v1/ping").json() == {"pong": True}
