from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

try:
    from .service import (
        ServiceAnswerResult,
        ServiceExecutionResult,
        ServiceQueryRequest,
        execute_pipeline,
        retrieve_structured_answer,
    )
except ImportError:  # pragma: no cover
    from service import (
        ServiceAnswerResult,
        ServiceExecutionResult,
        ServiceQueryRequest,
        execute_pipeline,
        retrieve_structured_answer,
    )

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "poc": "04e"}


@router.post("/query", response_model=ServiceExecutionResult)
def submit_query(request: ServiceQueryRequest) -> ServiceExecutionResult:
    try:
        return execute_pipeline(request)
    except (ValidationError, ValueError) as exc:
        logger.warning("submit_query validation failure: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover
        logger.exception("submit_query internal failure")
        raise HTTPException(status_code=500, detail="Internal service error") from exc


@router.post("/answer", response_model=ServiceAnswerResult)
def get_structured_answer(request: ServiceQueryRequest) -> ServiceAnswerResult:
    try:
        return retrieve_structured_answer(request)
    except (ValidationError, ValueError) as exc:
        logger.warning("get_structured_answer validation failure: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover
        logger.exception("get_structured_answer internal failure")
        raise HTTPException(status_code=500, detail="Internal service error") from exc
