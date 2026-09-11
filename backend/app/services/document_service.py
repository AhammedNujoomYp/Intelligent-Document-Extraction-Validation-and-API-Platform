import time
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.services.document_validation_service import validate_document
from app.services.extraction_service import extract_document_text
from app.services.document_ai_service import extract_financial_data
from app.services.financial_validation_service import validate_invoice
from app.repositories.document_repository import save_document
from app.services.balance_sheet_validation_service import (
    validate_balance_sheet,
)
from app.services.profit_loss_validation_service import (
    validate_profit_loss,
)
from app.services.cash_flow_validation_service import validate_cash_flow



async def process_document(
    db: Session,
    file_bytes: bytes,
    filename: str,
    content_type: str,
    document_type: str,
):
    start_time = time.perf_counter()

    # ---------------------------------------------------------
    # 1. DOCUMENT VALIDATION
    # ---------------------------------------------------------
    file_validation = validate_document(
        filename=filename,
        content_type=content_type,
        file_bytes=file_bytes,
    )

    # ---------------------------------------------------------
    # 2. HANDLE INVALID DOCUMENT
    # ---------------------------------------------------------
    if file_validation["status"] == "FAIL":

        result = {
            "document_name": filename,
            "document_type": document_type,
            "processing_status": "FAILED",
            "file_validation": file_validation,
            "extracted_data": {},
            "validation": {
                "checks": [],
                "overall_status": "NOT_APPLICABLE",
                "issues": [],
            },
            "processing_metadata": {
                "processed_at": datetime.now(
                    timezone.utc
                ).isoformat(),
                "processing_time_ms": round(
                    (time.perf_counter() - start_time) * 1000,
                    2,
                ),
            },
        }

        # Store failed processing result
        save_document(
            db=db,
            document_name=filename,
            document_type=document_type,
            processing_status="FAILED",
            result=result,
        )

        return result

    # ---------------------------------------------------------
    # 3. TEXT EXTRACTION / OCR
    # ---------------------------------------------------------
    pages, ocr_used = extract_document_text(
        file_bytes=file_bytes,
        file_type=content_type,
    )

    # ---------------------------------------------------------
    # 4. AI FIELD & TABLE EXTRACTION
    # ---------------------------------------------------------
    extracted_data = extract_financial_data(
        document_type=document_type,
        pages=pages,
    )

    # ---------------------------------------------------------
    # 5. FINANCIAL CALCULATION VALIDATION
    # ---------------------------------------------------------
    if document_type == "invoice":
       validation = validate_invoice(extracted_data)

    elif document_type == "balance_sheet":
       validation = validate_balance_sheet(extracted_data)

    elif document_type == "profit_and_loss":
       validation = validate_profit_loss(extracted_data)

    elif document_type == "cash_flow_statement":
       validation = validate_cash_flow(extracted_data)

    else:
       raise ValueError(
        f"Unsupported document type for financial validation: {document_type}"
        )

    # ---------------------------------------------------------
    # 6. PROCESSING STATUS
    # ---------------------------------------------------------
    if validation["overall_status"] == "PASS":
        processing_status = "PASS"

    elif validation["overall_status"] == "FAIL":
        processing_status = "FAILED"

    else:
        processing_status = "FAILED"

    # ---------------------------------------------------------
    # 7. BUILD PROCESSING RESULT
    # ---------------------------------------------------------
    result = {
        "document_name": filename,
        "document_type": document_type,
        "processing_status": processing_status,
        "file_validation": file_validation,
        "extracted_data": extracted_data.model_dump(),
        "validation": validation,
        "processing_metadata": {
            "processed_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "processing_time_ms": round(
                (time.perf_counter() - start_time) * 1000,
                2,
            ),
            "page_count": len(pages),
            "ocr_used": ocr_used,
        },
    }

    # ---------------------------------------------------------
    # 8. STORE PROCESSING RESULT
    # ---------------------------------------------------------
    save_document(
        db=db,
        document_name=filename,
        document_type=document_type,
        processing_status=processing_status,
        result=result,
    )

    # ---------------------------------------------------------
    # 9. RETURN RESULT
    # ---------------------------------------------------------
    return result