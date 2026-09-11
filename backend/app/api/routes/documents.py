import json
from typing import Literal

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.document_repository import (
    get_documents,
    get_latest_document,
)
from app.schemas.document import DocumentResponse
from app.services.document_service import process_document


router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
)


# ============================================================
# POST /api/v1/documents/process
# ============================================================

@router.post(
    "/process",
    response_model=DocumentResponse,
    summary="Process a financial document",
)
async def process_financial_document(
    file: UploadFile = File(...),
    document_type: Literal[
        "invoice",
        "balance_sheet",
        "profit_and_loss",
        "cash_flow_statement",
    ] = Form(...),
    db: Session = Depends(get_db),
):
    try:
        file_bytes = await file.read()

        result = await process_document(
            db=db,
            file_bytes=file_bytes,
            filename=file.filename,
            content_type=file.content_type,
            document_type=document_type,
        )

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "PROCESSING_ERROR",
                    "message": str(exc),
                }
            },
        )

    except Exception as exc:
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "INTERNAL_PROCESSING_ERROR",
                    "message": str(exc),
                }
            },
        )


# ============================================================
# GET /api/v1/documents
# ============================================================

@router.get(
    "",
    summary="List processed documents",
)
def list_documents(
    db: Session = Depends(get_db),
):
    documents = get_documents(db)

    return [
        {
            "document_name": document.document_name,
            "document_type": document.document_type,
            "processing_status": document.processing_status,
            "processed_at": document.updated_at,
        }
        for document in documents
    ]


# ============================================================
# GET /api/v1/documents/{document_name}
# ============================================================

@router.get(
    "/{document_name}",
    summary="Get latest document processing result",
)
def get_document(
    document_name: str,
    db: Session = Depends(get_db),
):
    document = get_latest_document(
        db=db,
        document_name=document_name,
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "DOCUMENT_NOT_FOUND",
                    "message": (
                        f"No processing result found for "
                        f"'{document_name}'."
                    ),
                }
            },
        )

    return json.loads(document.result_json)