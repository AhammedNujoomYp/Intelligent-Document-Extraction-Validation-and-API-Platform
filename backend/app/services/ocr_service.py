from io import BytesIO

from PIL import Image
import pytesseract
import pymupdf

from app.core.config import settings


pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd


def ocr_image(file_bytes: bytes) -> str:
    image = Image.open(BytesIO(file_bytes))

    text = pytesseract.image_to_string(image)

    return text.strip()


def ocr_pdf(file_bytes: bytes) -> list[dict]:
    document = pymupdf.open(
        stream=file_bytes,
        filetype="pdf"
    )

    pages = []

    try:
        for page_index, page in enumerate(document):

            # Convert PDF page to image
            pixmap = page.get_pixmap(
                matrix=pymupdf.Matrix(2, 2)
            )

            image_bytes = pixmap.tobytes("png")

            # OCR the rendered image
            text = ocr_image(image_bytes)

            pages.append({
                "page_number": page_index + 1,
                "text": text
            })

    finally:
        document.close()

    return pages