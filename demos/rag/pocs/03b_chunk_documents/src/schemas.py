"""Pydantic schemas for 03b chunking POC."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, model_validator


class LoadedDocument(BaseModel):
    """Input contract for records produced by 03a_load_documents."""

    document_id: str
    source_file: str
    source_path: str
    title: str
    text: str
    character_count: int = Field(gt=0)

    @field_validator("document_id", "source_file", "source_path", "title", "text")
    @classmethod
    def validate_non_empty_strings(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("field cannot be empty")
        return value

    @model_validator(mode="after")
    def validate_character_count(self) -> "LoadedDocument":
        if self.character_count != len(self.text):
            raise ValueError("character_count must equal len(text)")
        return self


class DocumentChunk(BaseModel):
    """Chunk-level payload used by later retrieval stages."""

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
