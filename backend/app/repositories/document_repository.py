import json

from sqlalchemy.orm import Session

from app.models.document import Document


def save_document(
    db: Session,
    document_name: str,
    document_type: str,
    processing_status: str,
    result: dict,
):
    document = Document(
        document_name=document_name,
        document_type=document_type,
        processing_status=processing_status,
        result_json=json.dumps(result),
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_latest_document(
    db: Session,
    document_name: str,
):
    return (
        db.query(Document)
        .filter(Document.document_name == document_name)
        .order_by(Document.created_at.desc())
        .first()
    )


def get_documents(db: Session):
    return (
        db.query(Document)
        .order_by(Document.created_at.desc())
        .all()
    )