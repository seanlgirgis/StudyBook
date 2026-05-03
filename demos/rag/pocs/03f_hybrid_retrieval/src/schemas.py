"""Pydantic schemas for 03f hybrid retrieval contracts.

This module defines data contracts only. Retrieval/search logic is intentionally
out of scope for this step.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class HybridRetrievalConfig(BaseModel):
    """Configuration contract for hybrid retrieval scoring and result limits."""

    word_weight: float = Field(default=0.65, ge=0.0, le=1.0)
    char_weight: float = Field(default=0.35, ge=0.0, le=1.0)
    top_k: int = Field(default=5, ge=1)

    @model_validator(mode="after")
    def validate_weight_sum(self) -> "HybridRetrievalConfig":
        if abs((self.word_weight + self.char_weight) - 1.0) > 1e-9:
            raise ValueError("word_weight + char_weight must equal 1.0")
        return self


class HybridSearchQuery(BaseModel):
    """Input query contract for hybrid search."""

    query: str

    @field_validator("query")
    @classmethod
    def validate_query_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("query cannot be empty")
        return value


class HybridSearchResult(BaseModel):
    """Ranked hybrid retrieval candidate contract."""

    rank: int = Field(ge=1)
    chunk_id: str
    hybrid_score: float = Field(ge=0.0)
    word_score: float = Field(ge=0.0)
    char_score: float = Field(ge=0.0)
    word_weight: float = Field(ge=0.0, le=1.0)
    char_weight: float = Field(ge=0.0, le=1.0)
    retrieval_sources: list[Literal["word", "char"]]
    source_file: str
    title: str
    section: str | None = None
    text: str
    normalized_text: str

    @field_validator("chunk_id", "source_file", "title")
    @classmethod
    def validate_non_empty_identity_fields(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("identity fields cannot be empty")
        return value

    @field_validator("text", "normalized_text")
    @classmethod
    def validate_non_empty_text_fields(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text fields cannot be empty")
        return value

    @field_validator("retrieval_sources")
    @classmethod
    def validate_retrieval_sources_not_empty(cls, value: list[Literal["word", "char"]]) -> list[Literal["word", "char"]]:
        if not value:
            raise ValueError("retrieval_sources cannot be empty")
        return value


class HybridSearchResponse(BaseModel):
    """Top-level hybrid retrieval response contract."""

    query: str
    normalized_query: str
    config: HybridRetrievalConfig
    results: list[HybridSearchResult]

    @field_validator("query", "normalized_query")
    @classmethod
    def validate_query_fields_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("query fields cannot be empty")
        return value
