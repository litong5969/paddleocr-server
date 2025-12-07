from fastapi.testclient import TestClient
import server


def test_auth_token_required_for_meta(monkeypatch):
    monkeypatch.setattr(server, "auth_token", "secret", raising=True)
    client = TestClient(server.app)
    # missing token
    r = client.get("/meta")
    assert r.status_code == 401
    # wrong token
    r = client.get("/meta", headers={"Authorization": "Bearer nope"})
    assert r.status_code == 401
    # correct token
    r = client.get("/meta", headers={"Authorization": "Bearer secret"})
    assert r.status_code == 200


class _FakeOCR:
    def ocr(self, path, cls=True):
        return (
            [
                [
                    [[0, 0], [1, 0], [1, 1], [0, 1]],
                    ["x", 0.9],
                ]
            ],
        )


def test_rate_limit_on_ocr(monkeypatch):
    monkeypatch.setattr(server, "ocr", _FakeOCR(), raising=True)
    monkeypatch.setattr(server, "rate_limit_per_min", 2, raising=True)
    # reset counters
    server._RATE_STATE["window"] = 0
    server._RATE_STATE["counts"] = {}
    client = TestClient(server.app)
    files = {"file": ("a.png", b"hi", "image/png")}
    # first two ok
    assert client.post("/ocr", files=files).status_code == 200
    assert client.post("/ocr", files=files).status_code == 200
    # third should be limited
    assert client.post("/ocr", files=files).status_code == 429
