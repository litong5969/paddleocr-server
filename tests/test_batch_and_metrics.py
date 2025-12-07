from fastapi.testclient import TestClient

import server


class _FakeOCR:
    def ocr(self, path, cls=True):  # noqa: ARG002
        return (
            [
                [
                    [[0, 0], [1, 0], [1, 1], [0, 1]],
                    ["alpha", 0.90],
                ]
            ],
        )


def test_batch_and_metrics(monkeypatch):
    monkeypatch.setattr(server, "ocr", _FakeOCR(), raising=True)
    client = TestClient(server.app)

    # Batch with two images and one non-image
    files = [
        ("files", ("a.png", b"fake-a", "image/png")),
        ("files", ("b.jpg", b"fake-b", "image/jpeg")),
        ("files", ("c.txt", b"nope", "text/plain")),
    ]
    r = client.post("/ocr/batch", files=files)
    assert r.status_code == 200
    data = r.json()
    assert "results" in data and len(data["results"]) == 3
    assert data["results"][0]["filename"] == "a.png"
    assert data["results"][2]["text"] == ""  # skipped non-image

    # Metrics endpoint should exist (enabled by default)
    mr = client.get("/metrics")
    assert mr.status_code in (200, 404)  # 404 if metrics disabled in env
    if mr.status_code == 200:
        expo = mr.text
        # basic presence check for our custom metrics names
        assert "ocr_requests_total" in expo or "http_request_latency_seconds" in expo


def test_size_limits(monkeypatch):
    # Enforce tiny per-file and batch limits to trigger 413
    monkeypatch.setattr(server, "ocr", _FakeOCR(), raising=True)
    monkeypatch.setattr(server, "max_image_size_mb", 0, raising=True)
    client = TestClient(server.app)

    # Single file should trip 413 due to 0MB limit
    r = client.post("/ocr", files={"file": ("x.png", b"abc", "image/png")})
    assert r.status_code == 413

    # Batch total limit
    monkeypatch.setattr(server, "max_image_size_mb", 1, raising=True)  # allow small file
    monkeypatch.setattr(server, "max_batch_total_mb", 0, raising=True)
    files = [("files", ("a.png", b"abc", "image/png"))]
    r = client.post("/ocr/batch", files=files)
    assert r.status_code == 413
