from google import genai
from google.genai import types, errors

from app.core.config import settings
from app.schemas.extraction import InvoiceExtraction


client = genai.Client(
    api_key=settings.gemini_api_key
)


def extract_invoice_data(
    pages: list[dict],
) -> InvoiceExtraction:

    document_text = "\n\n".join(
        f"--- PAGE {page['page_number']} ---\n"
        f"{page['text']}"
        for page in pages
    )

    prompt = f"""
You are a financial document extraction system.

The document type is: INVOICE.

Extract information ONLY from the supplied document text.

IMPORTANT RULES:

1. Extract ALL meaningful visible invoice information.
2. Do not invent, infer, or guess values.
3. If a field is missing or unreadable, return null.
4. Preserve the source value accurately.
5. Do not convert a currency symbol into an ISO currency
   unless the document explicitly provides the currency.
6. Extract every visible invoice line item.
7. Extract quantity, unit price, amount and adjustment
   when available.
8. Extract vendor and customer information.
9. Extract payment terms and payment status when present.
10. Extract bank information when visibly present.
11. For every extracted field, provide supporting evidence.
12. Evidence source_text must come from the supplied document.
13. Include the correct page number.
14. Do not perform financial calculations.
15. Do not correct OCR text unless the intended value is
    clearly supported by the source.
16. Use other_fields for meaningful visible information that
    does not fit the standard fields.

DOCUMENT TEXT:

{document_text}
"""

    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=InvoiceExtraction,
            ),
        )

    except errors.ClientError as exc:

        # Gemini quota exhausted
        if exc.code == 429:
            raise RuntimeError(
                "AI_QUOTA_EXCEEDED: Gemini API quota has been "
                "exhausted. Please check your Gemini API plan "
                "and quota before processing another document."
            ) from exc

        # Other Gemini client errors
        raise RuntimeError(
            f"AI_EXTRACTION_ERROR: Gemini API request failed: {exc}"
        ) from exc

    except Exception as exc:

        raise RuntimeError(
            f"AI_EXTRACTION_ERROR: Gemini extraction failed: {exc}"
        ) from exc

    if not response.text:
        raise RuntimeError(
            "AI_EXTRACTION_ERROR: Gemini returned an empty response."
        )

    return InvoiceExtraction.model_validate_json(
        response.text
    )