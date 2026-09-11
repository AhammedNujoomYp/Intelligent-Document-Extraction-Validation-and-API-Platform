from pathlib import Path

from app.services.ocr_service import ocr_image


image_path = Path(
    "sample_documents/20251118_000612.jpg"
)

if not image_path.exists():
    raise FileNotFoundError(
        image_path
    )

text = ocr_image(
    image_path.read_bytes()
)

print(text)