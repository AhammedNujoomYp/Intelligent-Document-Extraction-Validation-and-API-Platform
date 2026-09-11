import io

import pymupdf
from PIL import Image
import pytesseract

from app.core.config import settings


# ---------------------------------------------------------
# Tesseract Configuration
# ---------------------------------------------------------
# Render/Linux:
# Tesseract is installed by Docker and is available in PATH.
#
# Windows:
# Set TESSERACT_CMD in .env if Tesseract is not in PATH.

if settings.tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = (
        settings.tesseract_cmd
    )


# ---------------------------------------------------------
# PDF Text Extraction
# ---------------------------------------------------------

def extract_text_from_pdf(
    file_bytes: bytes,
) -> list[dict]:

    document = pymupdf.open(
        stream=file_bytes,
        filetype="pdf",
    )

    pages = []

    try:
        for page_index, page in enumerate(document):

            page_number = page_index + 1

            # ---------------------------------------------
            # Native PDF text extraction
            # ---------------------------------------------

            text = page.get_text("text").strip()

            print(
                f"[PDF] Page {page_number}: "
                f"native text length = {len(text)}"
            )

            # ---------------------------------------------
            # OCR fallback
            # ---------------------------------------------

            if len(text) < 50:

                matrix = pymupdf.Matrix(3, 3)

                pixmap = page.get_pixmap(
                    matrix=matrix,
                    alpha=False,
                )

                image_bytes = pixmap.tobytes("png")

                image = Image.open(
                    io.BytesIO(image_bytes)
                )

                ocr_text = pytesseract.image_to_string(
                    image,
                    config="--psm 6",
                ).strip()

                print(
                    f"[OCR] Page {page_number}: "
                    f"OCR text length = {len(ocr_text)}"
                )

                if len(ocr_text) > len(text):
                    text = ocr_text

            pages.append(
                {
                    "page_number": page_number,
                    "text": text,
                }
            )

    finally:
        document.close()

    return pages