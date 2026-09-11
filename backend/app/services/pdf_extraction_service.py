import io

import pymupdf
from PIL import Image
import pytesseract


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_pdf(file_bytes: bytes) -> list[dict]:
    document = pymupdf.open(
        stream=file_bytes,
        filetype="pdf"
    )

    pages = []

    try:
        for page_index, page in enumerate(document):

            page_number = page_index + 1

            # Try native PDF text extraction
            text = page.get_text("text").strip()

            # OCR fallback for scanned PDFs
            if len(text) < 50:

                matrix = pymupdf.Matrix(3, 3)

                pixmap = page.get_pixmap(
                    matrix=matrix,
                    alpha=False
                )

                image_bytes = pixmap.tobytes("png")

                image = Image.open(
                    io.BytesIO(image_bytes)
                )

                # OCR
                ocr_text = pytesseract.image_to_string(
                    image,
                    config="--psm 6"
                ).strip()

                if len(ocr_text) > len(text):
                    text = ocr_text

            pages.append({
                "page_number": page_number,
                "text": text
            })

    finally:
        document.close()

    return pages