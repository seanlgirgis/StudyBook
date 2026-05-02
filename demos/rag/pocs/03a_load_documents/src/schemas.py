from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class SourceDocument(BaseModel):
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
        if not value.strip():
            raise ValueError("document_id cannot be empty")
        return value

    @field_validator("source_file")
    @classmethod
    def validate_source_file(cls, value: str) -> str:
        if not value.lower().endswith(".md"):
            raise ValueError("source_file must end with .md")
        return value

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text cannot be empty")
        return value
