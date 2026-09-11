from pathlib import Path

from app.services.extraction_service import extract_document_text
from app.services.gemini_extraction_service import extract_invoice_data


PDF_PATH = Path(
    "sample_documents/wordpress-pdf-invoice-plugin-sample.pdf"
)


if not PDF_PATH.exists():
    print("ERROR: Invoice PDF not found")
    print(PDF_PATH.resolve())
    raise SystemExit(1)


file_bytes = PDF_PATH.read_bytes()


# Phase 2
pages, ocr_used = extract_document_text(
    file_bytes=file_bytes,
    file_type="application/pdf"
)


print("=" * 70)
print("PHASE 3 - GEMINI INVOICE EXTRACTION")
print("=" * 70)

print(f"OCR used: {ocr_used}")
print(f"Pages: {len(pages)}")


# Phase 3
result = extract_invoice_data(pages)


print("\n" + "=" * 70)
print("STRUCTURED EXTRACTION")
print("=" * 70)

print(result.model_dump_json(indent=2))