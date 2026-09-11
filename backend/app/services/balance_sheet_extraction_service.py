from google import genai
from google.genai import types

from app.core.config import settings
from app.schemas.extraction import BalanceSheetExtraction


client = genai.Client(
    api_key=settings.gemini_api_key
)


def extract_balance_sheet_data(
    pages: list[dict],
) -> BalanceSheetExtraction:

    document_text = "\n\n".join(
        f"--- PAGE {page['page_number']} ---\n"
        f"{page['text']}"
        for page in pages
    )

    prompt = f"""
You are a financial document extraction system.

The document type is: BALANCE SHEET.

Extract information ONLY from the supplied document text.

IMPORTANT RULES:

1. Extract ALL meaningful visible information.
2. Extract all statement header information.
3. Extract company name when present.
4. Extract every visible reporting period/year.
5. Extract currency when explicitly shown.
6. Extract EVERY visible financial line item and value.
7. Extract total_assets when present.
8. Extract total_liabilities when present.
9. Extract total_equity when present.
10. Preserve values exactly as represented by the source.
11. Parentheses/bracketed negative values must be represented as negative numbers.
12. Missing values must be null.
13. Do not invent or infer missing financial values.
14. Do not perform financial calculations.
15. For each extracted value, provide supporting evidence.
16. Evidence source_text must come from the supplied document.
17. Include the correct page number.
18. Comparative periods must be preserved separately.
19. Do not omit financial line items merely because they are not in the minimum fields.
20. Put additional meaningful visible fields into other_fields.

For line_items:
- name = exact financial line-item name.
- values = reporting period/year mapped to the corresponding numeric value.
- evidence = supporting source text and page number.

DOCUMENT TEXT:

{document_text}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=BalanceSheetExtraction,
        ),
    )

    return BalanceSheetExtraction.model_validate_json(
        response.text
    )