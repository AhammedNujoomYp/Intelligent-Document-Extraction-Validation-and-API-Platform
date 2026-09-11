from pathlib import Path

from app.services.extraction_service import extract_document_text


IMAGE_PATH = Path(
    "sample_documents/20251118_000612.jpg"
)


if not IMAGE_PATH.exists():
    print("ERROR: Image not found")
    print(f"Expected file: {IMAGE_PATH.resolve()}")
    raise SystemExit(1)


file_bytes = IMAGE_PATH.read_bytes()


pages, ocr_used = extract_document_text(
    file_bytes=file_bytes,
    file_type="image/jpeg"
)


print("=" * 70)
print("IMAGE OCR TEST")
print("=" * 70)

print(f"File: {IMAGE_PATH.name}")
print(f"OCR used: {ocr_used}")
print(f"Pages: {len(pages)}")


for page in pages:
    print("\n" + "=" * 70)
    print(f"PAGE {page['page_number']}")
    print("=" * 70)

    print(page["text"])