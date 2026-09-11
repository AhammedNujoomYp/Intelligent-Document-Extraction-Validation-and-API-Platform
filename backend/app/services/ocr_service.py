from io import BytesIO

from PIL import Image
import pytesseract
import pymupdf

from app.core.config import settings


# ---------------------------------------------------------
# Tesseract Configuration
# ---------------------------------------------------------
# On Render/Linux, Tesseract is installed in the Docker image
# and can be found automatically.
#
# On Windows, set TESSERACT_CMD in .env if needed.
# Example:
# TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe

if settings.tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = (
        settings.tesseract_cmd
    )


# ---------------------------------------------------------
# OCR Image
# ---------------------------------------------------------

def ocr_image(file_bytes: bytes) -> str:
    image = Image.open(BytesIO(file_bytes))

    text = pytesseract.image_to_string(
        image,
        config="--psm 6",
    )

    return text.strip()


# ---------------------------------------------------------
# OCR PDF
# ---------------------------------------------------------

def ocr_pdf(file_bytes: bytes) -> list[dict]:
    document = pymupdf.open(
        stream=file_bytes,
        filetype="pdf",
    )

    pages = []

    try:
        for page_index, page in enumerate(document):

            pixmap = page.get_pixmap(
                matrix=pymupdf.Matrix(2, 2),
                alpha=False,
            )

            image_bytes = pixmap.tobytes("png")

            text = ocr_image(image_bytes)

            pages.append(
                {
                    "page_number": page_index + 1,
                    "text": text,
                }
            )

    finally:
        document.close()

    return pages