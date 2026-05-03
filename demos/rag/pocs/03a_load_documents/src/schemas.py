"""Pydantic contracts for 03a markdown document loading.

This module defines the structured schema used after reading raw markdown files
from disk. We use Pydantic here so document records are validated early:
- bad or empty fields fail fast
- downstream stages receive consistent typed data
- debugging is easier when data quality rules are explicit
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class SourceDocument(BaseModel):
    """Validated representation of one source markdown document.

    Field purpose:
    - document_id: stable identifier derived from file name stem
    - source_file: markdown file name (must end with .md)
    - source_path: repo-relative path for traceability/citations later
    - title: extracted heading or safe fallback title
    - text: full markdown text payload
    - character_count: character size of loaded text
    - line_count: line total for diagnostics and future chunking heuristics
    - synthetic: flag proving this dataset is synthetic demo content
    """

    document_id: str
    source_file: str
    source_path: str
    title: str
    text: str
    character_count: int = Field(gt=0)
    line_count: int = Field(gt=0)
    synthetic: bool

    @field_validator("document_id")
    @classmethod
    def validate_document_id(cls, value: str) -> str:
        # Plain-English rule: every record must have a non-empty stable id.
        if not value.strip():
            raise ValueError("document_id cannot be empty")
        return value

    @field_validator("source_file")
    @classmethod
    def validate_source_file(cls, value: str) -> str:
        # Plain-English rule: loaded source files in this POC are markdown only.
        if not value.lower().endswith(".md"):
            raise ValueError("source_file must end with .md")
        return value

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        # Plain-English rule: empty documents are invalid for retrieval preparation.
        if not value.strip():
            raise ValueError("text cannot be empty")
        return value
