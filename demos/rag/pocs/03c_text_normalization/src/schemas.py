"""Pydantic schemas for 03c text normalization POC."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, model_validator


class DocumentChunk(BaseModel):
    """Input chunk contract produced by 03b_chunk_documents."""

    chunk_id: str
    document_id: str
    source_file: str
    source_path: str
    title: str
    chunk_index: int = Field(ge=0)
    text: str
    character_count: int = Field(gt=0)

    @field_validator("chunk_id", "document_id", "source_file", "source_path", "title")
    @classmethod
    def validate_non_empty_identity_fields(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("identity fields cannot be empty")
        return value

    @field_validator("text")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text cannot be empty")
        return value

    @model_validator(mode="after")
    def validate_character_count(self) -> "DocumentChunk":
        if self.character_count != len(self.text):
            raise ValueError("character_count must equal len(text)")
        return self


class NormalizedChunk(DocumentChunk):
    """Output chunk contract with normalized retrieval text added."""

    normalized_text: str
    normalized_character_count: int = Field(gt=0)

    @field_validator("normalized_text")
    @classmethod
    def validate_non_empty_normalized_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("normalized_text cannot be empty")
        return value

    @model_validator(mode="after")
    def validate_normalized_character_count(self) -> "NormalizedChunk":
        if self.normalized_character_count != len(self.normalized_text):
            raise ValueError("normalized_character_count must equal len(normalized_text)")
        return self
