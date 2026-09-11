from pathlib import Path

from app.services.text_extraction_service import extract_document_text


pdf_path = Path(
    "sample_documents/wordpress-pdf-invoice-plugin-sample.pdf"
)

if not pdf_path.exists():
    print("ERROR: PDF not found")
    print(pdf_path.resolve())
    raise SystemExit(1)


file_bytes = pdf_path.read_bytes()


pages, ocr_used = extract_document_text(
    file_bytes,
    "application/pdf"
)


print(f"OCR used: {ocr_used}")
print(f"Pages: {len(pages)}")

for page in pages:
    print("\n" + "=" * 60)
    print(f"PAGE {page['page_number']}")
    print("=" * 60)
    print(page["text"])