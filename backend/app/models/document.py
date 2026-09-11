from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    document_name = Column(String(255), nullable=False, index=True)

    document_type = Column(String(50), nullable=False)

    processing_status = Column(String(30), nullable=False)

    result_json = Column(Text, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )