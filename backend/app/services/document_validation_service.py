from io import BytesIO

import pymupdf

from app.core.config import settings


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
}


def validate_document(
    filename: str,
    content_type: str,
    file_bytes: bytes,
) -> dict:

    extension = ""

    if "." in filename:
        extension = "." + filename.rsplit(".", 1)[1].lower()

    # File type validation
    if extension not in SUPPORTED_EXTENSIONS:
        return {
            "file_type": content_type,
            "is_supported": False,
            "is_readable": False,
            "page_count": 0,
            "status": "FAIL",
            "error_code": "UNSUPPORTED_FILE_TYPE",
            "error_message": (
                "Only PDF / JPG / PNG documents are supported."
            ),
        }

    # Empty file
    if not file_bytes:
        return {
            "file_type": content_type,
            "is_supported": True,
            "is_readable": False,
            "page_count": 0,
            "status": "FAIL",
            "error_code": "EMPTY_FILE",
            "error_message": "The uploaded file is empty.",
        }

    # File size
    max_size = settings.max_file_size_mb * 1024 * 1024

    if len(file_bytes) > max_size:
        return {
            "file_type": content_type,
            "is_supported": True,
            "is_readable": False,
            "page_count": 0,
            "status": "FAIL",
            "error_code": "FILE_TOO_LARGE",
            "error_message": (
                f"File exceeds the maximum size of "
                f"{settings.max_file_size_mb} MB."
            ),
        }

    # PDF validation
    if extension == ".pdf":

        try:
            pdf = pymupdf.open(
                stream=BytesIO(file_bytes),
                filetype="pdf"
                )

            page_count = len(pdf)

            pdf.close()

            if page_count == 0:
                return {
                    "file_type": content_type,
                    "is_supported": True,
                    "is_readable": False,
                    "page_count": 0,
                    "status": "FAIL",
                    "error_code": "UNREADABLE_DOCUMENT",
                    "error_message": "PDF contains no pages.",
                }

            if page_count > settings.max_pages:
                return {
                    "file_type": content_type,
                    "is_supported": True,
                    "is_readable": True,
                    "page_count": page_count,
                    "status": "FAIL",
                    "error_code": "PAGE_LIMIT_EXCEEDED",
                    "error_message": (
                        f"Maximum allowed pages is "
                        f"{settings.max_pages}."
                    ),
                }

            return {
                "file_type": content_type,
                "is_supported": True,
                "is_readable": True,
                "page_count": page_count,
                "status": "PASS",
            }

        except Exception:
            return {
                "file_type": content_type,
                "is_supported": True,
                "is_readable": False,
                "page_count": 0,
                "status": "FAIL",
                "error_code": "UNREADABLE_DOCUMENT",
                "error_message": "Unable to read the PDF.",
            }

    # Images are treated as one-page documents
    return {
        "file_type": content_type,
        "is_supported": True,
        "is_readable": True,
        "page_count": 1,
        "status": "PASS",
    }