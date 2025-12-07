from fastapi.testclient import TestClient

import server


class _FakeOCR:
    def ocr(self, path, cls=True):  # noqa: ARG002
        # emulate PaddleOCR output structure: [[ [box], [text, score] ], ...]
        return [
            [
                [[0, 0], [1, 0], [1, 1], [0, 1]],
                ["hello", 0.98],
            ],
            [
                [[0, 0], [1, 0], [1, 1], [0, 1]],
                ["world", 0.99],
            ],
        ],


def test_health_and_meta():
    client = TestClient(server.app)
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
    assert "X-Process-Time-ms" in r.headers

    r = client.get("/meta")
    assert r.status_code == 200
    assert "lang" in r.json()


def test_ready_and_ocr_with_fake(monkeypatch):
    # Patch OCR engine with a fake to avoid heavyweight dependency
    monkeypatch.setattr(server, "ocr", _FakeOCR(), raising=True)
    client = TestClient(server.app)

    r = client.get("/readyz")
    assert r.status_code == 200
    assert r.json().get("ready") is True

    files = {"file": ("sample.png", b"fake-bytes", "image/png")}
    r = client.post("/ocr", files=files)
    assert r.status_code == 200
    data = r.json()
    assert data["text"] == "hello\nworld"
    assert len(data["lines"]) == 2
