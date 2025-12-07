#!/usr/bin/env python3
import argparse
import asyncio
import statistics
import time
from pathlib import Path

import httpx


async def _post_ocr(client: httpx.AsyncClient, url: str, image_bytes: bytes):
    t0 = time.perf_counter()
    try:
        r = await client.post(url, files={"file": ("img.jpg", image_bytes, "image/jpeg")}, timeout=60)
        ok = r.status_code == 200
        return ok, time.perf_counter() - t0
    except Exception:
        return False, time.perf_counter() - t0


async def run(url: str, image_path: Path, concurrency: int, requests: int):
    data = image_path.read_bytes()
    sem = asyncio.Semaphore(concurrency)
    lat = []
    ok_cnt = 0

    async with httpx.AsyncClient() as client:
        async def one():
            nonlocal ok_cnt
            async with sem:
                ok, dt = await _post_ocr(client, url, data)
                lat.append(dt)
                if ok:
                    ok_cnt += 1

        tasks = [asyncio.create_task(one()) for _ in range(requests)]
        await asyncio.gather(*tasks)

    lat.sort()
    def pct(p):
        if not lat:
            return 0
        return lat[int(len(lat) * p / 100.0) - 1]

    print({
        "url": url,
        "concurrency": concurrency,
        "requests": requests,
        "ok": ok_cnt,
        "err": requests - ok_cnt,
        "p50": round(pct(50), 4),
        "p95": round(pct(95), 4),
        "p99": round(pct(99), 4),
        "avg": round(statistics.mean(lat) if lat else 0, 4),
    })


def main():
    ap = argparse.ArgumentParser(description="Simple OCR benchmark")
    ap.add_argument("--url", default="http://localhost:5215/ocr")
    ap.add_argument("--image", default=str(Path(__file__).resolve().parents[2] / "test.jpg"))
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--requests", type=int, default=16)
    args = ap.parse_args()

    asyncio.run(run(args.url, Path(args.image), args.concurrency, args.requests))


if __name__ == "__main__":
    main()
