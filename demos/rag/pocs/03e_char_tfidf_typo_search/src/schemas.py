"""Pydantic schemas for 03e character TF-IDF typo search POC."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, model_validator


class NormalizedChunkRecord(BaseModel):
    """Validated normalized chunk record expected from 03c output."""

    chunk_id: str
    document_id: str
    source_file: str
    source_path: str
    title: str
    chunk_index: int = Field(ge=0)
    text: str
    character_count: int = Field(gt=0)
    normalized_text: str
    normalized_character_count: int = Field(gt=0)

    @field_validator("chunk_id", "document_id", "source_file", "source_path", "title")
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

    @model_validator(mode="after")
    def validate_character_counts(self) -> "NormalizedChunkRecord":
        if self.character_count != len(self.text):
            raise ValueError("character_count must equal len(text)")
        if self.normalized_character_count != len(self.normalized_text):
            raise ValueError("normalized_character_count must equal len(normalized_text)")
        return self
