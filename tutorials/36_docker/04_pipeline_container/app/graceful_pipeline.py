# ============================================================
# Topic   : Docker for Data Engineers
# File    : app/graceful_pipeline.py
# Covers  : Long-running pipeline with SIGTERM handling
# Prereqs : Docker Desktop installed and running
# Run     : docker run --rm -v ${PWD}/runtime_data/output:/data/output tutorial36-pipeline:signals-1.0.0
# ============================================================

from __future__ import annotations

import json
import logging
import os
import pathlib
import signal
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("graceful_pipeline")


class Pipeline:
    def __init__(self) -> None:
        self.shutdown_requested = False
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

    def _handle_signal(self, signum: int, frame: object) -> None:
        log.info("Shutdown signal %s received; finishing current batch before exit", signum)
        self.shutdown_requested = True

    def process_batch(self, batch_id: int) -> dict[str, int]:
        log.info("Processing batch %s", batch_id)
        time.sleep(1)
        return {"batch_id": batch_id, "rows_processed": 1000}

    def run(self) -> None:
        output_dir = pathlib.Path(os.getenv("OUTPUT_DIR", "/data/output"))
        output_dir.mkdir(parents=True, exist_ok=True)
        max_batches = int(os.getenv("MAX_BATCHES", "30"))
        results = []

        log.info("Pipeline starting")
        for batch_id in range(max_batches):
            results.append(self.process_batch(batch_id))
            if self.shutdown_requested:
                log.info("Graceful stop requested after batch %s", batch_id)
                break

        summary = {
            "total_batches": len(results),
            "total_rows": sum(row["rows_processed"] for row in results),
            "shutdown_requested": self.shutdown_requested,
        }
        summary_path = output_dir / "graceful_summary.json"
        summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        log.info("Pipeline complete; wrote %s", summary_path)
        log.info("Summary: %s", summary)


if __name__ == "__main__":
    Pipeline().run()
