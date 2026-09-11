from typing import Any, Optional

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    code: str
    message: str


class ErrorWrapper(BaseModel):
    error: ErrorResponse


class FileValidationResponse(BaseModel):
    file_type: Optional[str] = None
    is_supported: bool
    is_readable: bool
    page_count: int
    status: str
    error_code: Optional[str] = None
    error_message: Optional[str] = None


class ValidationCheckResponse(BaseModel):
    name: Optional[str] = None
    formula: str

    # Different validators currently use "operands".
    # Keep the actual validation output structure.
    operands: dict[str, Any] = Field(default_factory=dict)

    calculated_value: Optional[float] = None
    reported_value: Optional[float] = None
    variance: Optional[float] = None
    status: str


class ValidationResponse(BaseModel):
    overall_status: str
    checks: list[ValidationCheckResponse] = Field(
        default_factory=list
    )


class ProcessingMetadataResponse(BaseModel):
    processing_time_seconds: Optional[float] = None
    extraction_method: Optional[str] = None
    ocr_used: Optional[bool] = None


class DocumentResponse(BaseModel):
    document_name: str
    document_type: str
    processing_status: str

    confidence: Optional[float] = None

    file_validation: FileValidationResponse

    extracted_data: Any

    validation: ValidationResponse

    processing_metadata: ProcessingMetadataResponse