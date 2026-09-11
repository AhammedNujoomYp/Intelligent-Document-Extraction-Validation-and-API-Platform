from app.services.pdf_extraction_service import extract_text_from_pdf
from app.services.ocr_service import ocr_image, ocr_pdf


SUPPORTED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
}


def extract_document_text(
    file_bytes: bytes,
    file_type: str
) -> tuple[list[dict], bool]:

    # --------------------------------
    # PDF
    # --------------------------------
    if file_type == "application/pdf":

        # First try normal PDF text extraction
        pages = extract_text_from_pdf(file_bytes)

        total_text_length = sum(
            len(page["text"])
            for page in pages
        )

        # Native/digital PDF
        if total_text_length > 50:
            return pages, False

        # Scanned/image-based PDF
        pages = ocr_pdf(file_bytes)

        return pages, True

    # --------------------------------
    # JPG / PNG
    # --------------------------------
    if file_type in SUPPORTED_IMAGE_TYPES:

        text = ocr_image(file_bytes)

        return [
            {
                "page_number": 1,
                "text": text
            }
        ], True

    raise ValueError(
        f"Unsupported file type: {file_type}"
    )