import os
import time
import tempfile
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse, Response, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# Optional import: allow import-time survival when paddleocr is missing
try:
    from paddleocr import PaddleOCR  # type: ignore
except Exception as _e:  # pragma: no cover
    PaddleOCR = None  # type: ignore
    _paddle_import_error = _e

# Optional: image size detection
try:
    from PIL import Image as _PIL_Image  # type: ignore
except Exception:  # pragma: no cover
    _PIL_Image = None

# Optional: Prometheus metrics
try:  # pragma: no cover - thin wrapper around third-party
    from prometheus_client import (
        Counter,
        Histogram,
        Gauge,
        generate_latest,
        CONTENT_TYPE_LATEST,
    )
except Exception:  # pragma: no cover
    Counter = Histogram = Gauge = None  # type: ignore
    generate_latest = None  # type: ignore
    CONTENT_TYPE_LATEST = "text/plain; version=0.0.4; charset=utf-8"  # type: ignore

load_dotenv()

app = FastAPI()
app.mount("/ui", StaticFiles(directory="web/ui", html=True), name="ui")

def _bool_env(name: str, default: bool) -> bool:
    """Parse boolean-like env values."""
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "t", "yes", "y", "on"}


ocr_lang = os.getenv("OCR_LANG", "ch")
ocr_version = os.getenv("OCR_VERSION", "PP-OCRv4")
ocr_use_angle_cls = _bool_env("OCR_USE_ANGLE_CLS", True)
ocr_use_gpu = _bool_env("OCR_USE_GPU", True)
ocr_home = os.getenv("PADDLEOCR_HOME")

# Perf/Obs config
metrics_enabled = _bool_env("METRICS_ENABLED", True)
warmup_on_start = _bool_env("OCR_WARMUP_ON_START", True)
warmup_timeout_sec = int(os.getenv("OCR_WARMUP_TIMEOUT_SEC", "20"))
batch_max_files = int(os.getenv("OCR_BATCH_MAX_FILES", "8"))
max_image_size_mb = int(os.getenv("MAX_IMAGE_SIZE_MB", "10"))
max_batch_total_mb = int(os.getenv("MAX_BATCH_TOTAL_MB", "20"))

# Security / QoS
auth_token = os.getenv("AUTH_TOKEN")
rate_limit_per_min = int(os.getenv("RATE_LIMIT_PER_MINUTE", "0"))
_RATE_STATE = {"window": 0, "counts": {}}  # ip -> count
max_image_size_mb = int(os.getenv("MAX_IMAGE_SIZE_MB", "10"))
max_batch_total_mb = int(os.getenv("MAX_BATCH_TOTAL_MB", "20"))

# Allow overriding model cache directory for volume mounts.
if ocr_home:
    os.environ["PADDLEOCR_HOME"] = ocr_home

def _init_ocr() -> Optional[object]:
    """Initialize PaddleOCR with graceful CPU fallback.

    Returns None if PaddleOCR unavailable, allowing server to start
    and expose readiness indicating not-ready.
    """
    if PaddleOCR is None:  # pragma: no cover
        return None
    try:
        return PaddleOCR(
            lang=ocr_lang,
            use_angle_cls=ocr_use_angle_cls,
            use_gpu=ocr_use_gpu,
            ocr_version=ocr_version,
        )
    except Exception:
        # GPU init may fail on non-GPU hosts; try CPU fallback when requested GPU
        if ocr_use_gpu:
            try:
                return PaddleOCR(
                    lang=ocr_lang,
                    use_angle_cls=ocr_use_angle_cls,
                    use_gpu=False,
                    ocr_version=ocr_version,
                )
            except Exception:
                return None
        return None


ocr = _init_ocr()

# Prometheus metrics (guard when disabled or client missing)
if metrics_enabled and Counter and Histogram and Gauge:  # pragma: no cover
    HTTP_LATENCY = Histogram(
        "http_request_latency_seconds", "HTTP request latency", ["endpoint"]
    )
    OCR_INFER = Histogram("ocr_inference_seconds", "OCR inference duration (s)")
    OCR_IMG_MP = Histogram(
        "ocr_image_megapixels", "OCR input image size in megapixels"
    )
    OCR_REQS = Counter("ocr_requests_total", "Total OCR requests", ["status"])
    OCR_READY = Gauge("ocr_ready", "OCR engine ready (1/0)")
    OCR_READY.set(1.0 if ocr is not None else 0.0)
else:  # pragma: no cover
    HTTP_LATENCY = OCR_INFER = OCR_IMG_MP = OCR_REQS = OCR_READY = None


class OCRLine(BaseModel):
    text: str
    score: float


class OCRResponse(BaseModel):
    text: str
    lines: List[OCRLine]


@app.middleware("http")
async def _auth_rl_middleware(request: Request, call_next):  # type: ignore
    path = request.url.path or "/"
    # Allowlisted paths for auth and rate-limit
    auth_exempt = {"/", "/ui", "/healthz", "/readyz", "/docs", "/openapi.json", "/redoc"}
    rl_paths = {"/ocr", "/ocr/batch"}

    # Simple token auth (protect OCR + meta/metrics by default)
    if auth_token and path not in auth_exempt:
        # Only enforce on OCR/meta/metrics
        if path in rl_paths or path in {"/meta", "/metrics"}:
            tok = request.headers.get("authorization") or request.headers.get("Authorization") or request.headers.get("x-api-token") or request.headers.get("X-API-Token")
            ok = False
            if tok:
                parts = tok.split()
                if len(parts) == 2 and parts[0].lower() == "bearer":
                    ok = (parts[1] == auth_token)
                else:
                    ok = (tok == auth_token)
            if not ok:
                return JSONResponse({"detail": "Unauthorized"}, status_code=401)

    # Rate-limit OCR endpoints by IP
    if rate_limit_per_min > 0 and path in rl_paths:
        try:
            ip = request.client.host if request.client else "-"
            now_min = int(time.time() // 60)
            if _RATE_STATE["window"] != now_min:
                _RATE_STATE["window"] = now_min
                _RATE_STATE["counts"] = {}
            c = _RATE_STATE["counts"].get(ip, 0) + 1
            if c > rate_limit_per_min:
                return JSONResponse({"detail": "Too Many Requests"}, status_code=429)
            _RATE_STATE["counts"][ip] = c
        except Exception:
            pass

    return await call_next(request)


@app.middleware("http")
async def _timing_middleware(request, call_next):  # type: ignore
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = int((time.perf_counter() - start) * 1000)
    response.headers["X-Process-Time-ms"] = str(duration_ms)
    if HTTP_LATENCY is not None:  # pragma: no cover
        ep = request.url.path
        if ep not in {"/", "/ocr", "/ocr/batch", "/healthz", "/readyz", "/meta", "/metrics"}:
            ep = "other"
        HTTP_LATENCY.labels(ep).observe(duration_ms / 1000.0)
    return response


@app.get("/")
async def root():
    return RedirectResponse(url="/ui")


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/readyz")
async def readyz():
    ready = ocr is not None
    return JSONResponse(
        status_code=200 if ready else 503,
        content={
            "ready": ready,
            "ocr_available": ocr is not None,
        },
    )


@app.get("/meta")
async def meta():
    return {
        "lang": ocr_lang,
        "version": ocr_version,
        "use_angle_cls": ocr_use_angle_cls,
        "use_gpu_requested": ocr_use_gpu,
        "paddleocr_home": os.getenv("PADDLEOCR_HOME") or "",
        "metrics_enabled": metrics_enabled,
        "warmup_on_start": warmup_on_start,
        "batch_max_files": batch_max_files,
        "max_image_size_mb": max_image_size_mb,
        "max_batch_total_mb": max_batch_total_mb,
        "auth_enabled": bool(auth_token),
        "rate_limit_per_min": rate_limit_per_min,
    }


@app.get("/metrics")
async def metrics():  # pragma: no cover - text format
    if not metrics_enabled or generate_latest is None:
        raise HTTPException(status_code=404, detail="metrics disabled")
    data = generate_latest()  # type: ignore[arg-type]
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


def _mb_to_bytes(mb: int) -> int:
    return int(mb) * 1024 * 1024


async def _save_upload_to_temp(upload: UploadFile, per_file_limit_bytes: int) -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False)
    size = 0
    try:
        while True:
            chunk = await upload.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > per_file_limit_bytes:
                raise HTTPException(status_code=413, detail="file too large")
            tmp.write(chunk)
        tmp.flush()
        tmp.close()
        return tmp.name
    except Exception:
        try:
            tmp.close()
        except Exception:
            pass
        try:
            os.unlink(tmp.name)
        except Exception:
            pass
        raise


def _observed_img_megapixels(path: str) -> None:
    if OCR_IMG_MP is None or _PIL_Image is None:
        return
    try:
        with _PIL_Image.open(path) as im:  # type: ignore[attr-defined]
            w, h = im.size
        mp = max(1, w * h) / 1_000_000.0
        OCR_IMG_MP.observe(mp)
    except Exception:
        pass


@app.post("/ocr", response_model=OCRResponse)
async def ocr_api(file: UploadFile = File(...)):
    if ocr is None:
        raise HTTPException(status_code=503, detail="OCR engine not initialized")
    # Basic content-type sanity check (best-effort)
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Unsupported content-type; expected image/*")
    per_file_limit = _mb_to_bytes(max_image_size_mb)
    temp_path = await _save_upload_to_temp(file, per_file_limit)
    try:
        start = time.perf_counter()
        _observed_img_megapixels(temp_path)
        result = ocr.ocr(temp_path, cls=True)  # type: ignore[attr-defined]
        infer_s = time.perf_counter() - start
        if OCR_INFER is not None:
            OCR_INFER.observe(infer_s)

        lines: List[dict] = []
        if result and result[0]:
            for line in result[0]:
                text = line[1][0]
                score = float(line[1][1])
                lines.append({"text": text, "score": score})

        payload = OCRResponse(
            text="\n".join([l["text"] for l in lines]) if lines else "",
            lines=[OCRLine(**l) for l in lines],
        )
        if OCR_REQS is not None:
            OCR_REQS.labels("ok").inc()
        return JSONResponse(content=payload.model_dump())
    finally:
        try:
            os.unlink(temp_path)
        except OSError:
            pass


class OCRFileResult(BaseModel):
    filename: str
    text: str
    lines: List[OCRLine]


class OCRBatchResponse(BaseModel):
    results: List[OCRFileResult]


@app.post("/ocr/batch", response_model=OCRBatchResponse)
async def ocr_batch(files: List[UploadFile] = File(...)):
    if ocr is None:
        raise HTTPException(status_code=503, detail="OCR engine not initialized")
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    if len(files) > batch_max_files:
        raise HTTPException(
            status_code=413, detail=f"Too many files; max {batch_max_files}"
        )

    results: List[OCRFileResult] = []
    total_bytes = 0
    for f in files:
        if f.content_type and not f.content_type.startswith("image/"):
            # skip non-image but keep batch semantics
            results.append(OCRFileResult(filename=f.filename, text="", lines=[]))
            if OCR_REQS is not None:
                OCR_REQS.labels("skip").inc()
            continue
        per_file_limit = _mb_to_bytes(max_image_size_mb)
        temp_path = await _save_upload_to_temp(f, per_file_limit)
        total_bytes += os.path.getsize(temp_path)
        if total_bytes > _mb_to_bytes(max_batch_total_mb):
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            raise HTTPException(status_code=413, detail="batch payload too large")
        try:
            start = time.perf_counter()
            _observed_img_megapixels(temp_path)
            result = ocr.ocr(temp_path, cls=True)  # type: ignore[attr-defined]
            infer_s = time.perf_counter() - start
            if OCR_INFER is not None:
                OCR_INFER.observe(infer_s)

            lines: List[dict] = []
            if result and result[0]:
                for line in result[0]:
                    text = line[1][0]
                    score = float(line[1][1])
                    lines.append({"text": text, "score": score})
            results.append(
                OCRFileResult(
                    filename=f.filename,
                    text="\n".join([l["text"] for l in lines]) if lines else "",
                    lines=[OCRLine(**l) for l in lines],
                )
            )
            if OCR_REQS is not None:
                OCR_REQS.labels("ok").inc()
        finally:
            try:
                os.unlink(temp_path)
            except OSError:
                pass
    return JSONResponse(content=OCRBatchResponse(results=results).model_dump())


def _warmup_if_needed():  # pragma: no cover
    """Run a lightweight warmup with timeout protection."""
    import threading

    global ocr
    if not warmup_on_start or ocr is None:
        return

    def _do():
        try:
            import numpy as _np

            dummy = _np.zeros((10, 10, 3), dtype="uint8")
            ocr.ocr(dummy, cls=True)  # type: ignore[attr-defined]
            if OCR_READY is not None:
                OCR_READY.set(1.0)
        except Exception:
            if OCR_READY is not None:
                OCR_READY.set(0.0)

    t = threading.Thread(target=_do, daemon=True)
    t.start()
    t.join(timeout=float(max(1, warmup_timeout_sec)))
    # If still running after timeout, leave it to finish in background
    if t.is_alive() and OCR_READY is not None:
        OCR_READY.set(0.0)


# Attempt warmup at import time with timeout best-effort
try:  # pragma: no cover
    if warmup_on_start:
        _warmup_if_needed()
except Exception:
    pass

if __name__ == "__main__":
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "5000"))
    ssl_cert = os.getenv("SSL_CERTFILE")
    ssl_key = os.getenv("SSL_KEYFILE")
    kwargs = {"host": host, "port": port}
    if ssl_cert and ssl_key and os.path.exists(ssl_cert) and os.path.exists(ssl_key):
        kwargs.update({"ssl_certfile": ssl_cert, "ssl_keyfile": ssl_key})
    uvicorn.run(app, **kwargs)
