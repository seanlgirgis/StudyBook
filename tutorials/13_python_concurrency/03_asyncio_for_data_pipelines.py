# ============================================================
# Topic   : Python Concurrency for Data Engineers
# File    : 03_asyncio_for_data_pipelines.py
# Covers  : asyncio event loop, coroutines, semaphores, async pipelines, TaskGroup
# Prereqs : pip install aiohttp aiofiles pyarrow pandas
# Run     : python 03_asyncio_for_data_pipelines.py
# ============================================================

from __future__ import annotations

import asyncio
import json
import os
import random
import time
from pathlib import Path
import datetime as dt


def default_output_dir() -> str:
    """Return platform-appropriate default output dir. Create if missing."""
    if os.name == "nt":
        base = Path("C:/tmp/studybook/concurrency/")
    else:
        base = Path("/tmp/studybook/concurrency/")
    base.mkdir(parents=True, exist_ok=True)
    return str(base)


async def async_http_get(url: str, session_id: int = 0) -> dict:
    """
    Simulate async HTTP GET. Uses asyncio.sleep(random 0.05–0.3s).
    10% chance of raising aiohttp.ClientError-like exception (simulated).
    Return:
      { url: str, status: 200, data: {"value": random_float, "ts": iso_string},
        latency_ms: float }
    """
    delay = random.uniform(0.05, 0.3)
    start = time.perf_counter()

    await asyncio.sleep(delay)

    # Simulate network error
    if random.random() < 0.1:
        raise Exception("Simulated network error")

    latency_ms = (time.perf_counter() - start) * 1000

    return {
        "url": url,
        "status": 200,
        "data": {
            "value": random.random(),
            "ts": dt.datetime.now(dt.UTC).isoformat(),
        },
        "latency_ms": latency_ms,
    }


async def fetch_all_urls(urls: list[str], max_concurrent: int = 10) -> list[dict]:
    """
    Use asyncio.Semaphore(max_concurrent) to cap concurrent requests.
    Use asyncio.gather(*tasks, return_exceptions=True).
    Replace exceptions with error dicts.
    Return results in original order.
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def bounded_fetch(url: str):
        async with semaphore:
            return await async_http_get(url)

    tasks = [bounded_fetch(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    final_results = []
    for url, result in zip(urls, results):
        if isinstance(result, Exception):
            final_results.append({
                "url": url,
                "status": "error",
                "error": str(result)
            })
        else:
            final_results.append(result)

    return final_results


async def read_file_async(path: str) -> str:
    """
    Read file using aiofiles. Fallback to thread executor if not installed.
    """
    try:
        import aiofiles
        async with aiofiles.open(path, mode="r") as f:
            return await f.read()
    except ImportError:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: Path(path).read_text())


async def write_file_async(path: str, content: str) -> None:
    """
    Write content to path using aiofiles (or executor fallback).
    """
    def ensure_dir():
        Path(path).parent.mkdir(parents=True, exist_ok=True)

    await asyncio.to_thread(ensure_dir)

    try:
        import aiofiles
        async with aiofiles.open(path, mode="w") as f:
            await f.write(content)
    except ImportError:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, lambda: Path(path).write_text(content))


async def pipeline_stage(items: list, processor, max_concurrent: int = 5) -> list:
    """
    Generic async pipeline stage.
    Applies async processor to each item with bounded concurrency.
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def worker(item):
        async with semaphore:
            return await processor(item)

    tasks = [worker(item) for item in items]
    return await asyncio.gather(*tasks)


async def run_etl_pipeline(source_urls: list[str], output_dir: str) -> dict:
    """
    Three-stage async pipeline:
      Stage 1: fetch
      Stage 2: transform
      Stage 3: write
    """
    t0 = time.perf_counter()

    # --- Stage 1 ---
    stage1_start = time.perf_counter()
    results = await fetch_all_urls(source_urls, max_concurrent=10)
    stage1_time = (time.perf_counter() - stage1_start) * 1000

    ok_results = [r for r in results if r.get("status") == 200]
    errors = [r for r in results if r.get("status") != 200]

    print(f"Stage 1 complete: {len(ok_results)}/{len(source_urls)} ok")

    # --- Stage 2 ---
    async def transform(item):
        return {
            "url": item["url"],
            "value": round(item["data"]["value"], 2),
            "ts": item["data"]["ts"],
            "processed_at": dt.datetime.now(dt.UTC).isoformat()
        }

    stage2_start = time.perf_counter()
    transformed = await pipeline_stage(ok_results, transform, max_concurrent=5)
    stage2_time = (time.perf_counter() - stage2_start) * 1000

    print(f"Stage 2 complete: {len(transformed)} transformed")

    # --- Stage 3 ---
    async def write_one(idx_item):
        i, item = idx_item
        path = Path(output_dir) / f"{i}.json"
        await write_file_async(str(path), json.dumps(item))

    stage3_start = time.perf_counter()
    await pipeline_stage(list(enumerate(transformed)), write_one, max_concurrent=5)
    stage3_time = (time.perf_counter() - stage3_start) * 1000

    print(f"Stage 3 complete: {len(transformed)} files written")

    total_ms = (time.perf_counter() - t0) * 1000

    return {
        "total_urls": len(source_urls),
        "fetched_ok": len(ok_results),
        "fetch_errors": len(errors),
        "files_written": len(transformed),
        "total_ms": total_ms,
        "stage1_ms": stage1_time,
        "stage2_ms": stage2_time,
        "stage3_ms": stage3_time,
    }


async def demonstrate_taskgroup() -> None:
    """
    Demonstrate asyncio.TaskGroup structured concurrency.
    """
    async def worker(i: int):
        delay = random.uniform(0.1, 0.5)
        await asyncio.sleep(delay)
        if random.random() < 0.2:
            raise RuntimeError(f"Task {i} failed")
        return f"Task {i} completed in {delay:.2f}s"

    start = time.perf_counter()

    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(worker(i)) for i in range(5)]
    except* Exception as eg:
        print("TaskGroup caught exception(s):")
        for e in eg.exceptions:
            print(f"  - {e}")
        tasks = []

    elapsed = time.perf_counter() - start

    for t in tasks:
        if not t.cancelled() and t.exception() is None:
            print(t.result())

    print(f"Total time: {elapsed:.2f}s")
    print(
        "TaskGroup ensures structured concurrency: if one task fails,\n"
        "all others are cancelled automatically."
    )


async def main_async():
    out = default_output_dir()
    urls = [f"http://sensors.internal/device/{i}/reading" for i in range(15)]

    print("\n=== ASYNC FETCH (15 URLs, max 10 concurrent) ===")
    results = await fetch_all_urls(urls, max_concurrent=10)
    ok = sum(1 for r in results if r.get("status") == 200)
    print(f"  OK: {ok}/15  Errors: {15 - ok}/15")

    print("\n=== ETL PIPELINE (fetch → transform → write) ===")
    stats = await run_etl_pipeline(urls[:10], out)
    print(
        f"  Fetched: {stats['fetched_ok']}  Errors: {stats['fetch_errors']}  "
        f"Written: {stats['files_written']}  Time: {stats['total_ms']:.0f}ms"
    )

    print("\n=== TASKGROUP (Python 3.11+) ===")
    await demonstrate_taskgroup()


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()