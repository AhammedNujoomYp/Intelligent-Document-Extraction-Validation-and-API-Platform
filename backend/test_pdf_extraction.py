from pathlib import Path

from app.services.pdf_extraction_service import (
    extract_text_from_pdf,
)


pdf_path = Path(
    "sample_documents/"
    "wordpress-pdf-invoice-plugin-sample.pdf"
)

file_bytes = pdf_path.read_bytes()

pages = extract_text_from_pdf(file_bytes)

for page in pages:
    print("=" * 60)
    print(f"PAGE {page['page_number']}")
    print("=" * 60)
    print(page["text"])