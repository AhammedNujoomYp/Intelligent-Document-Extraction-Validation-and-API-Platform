from google import genai
from app.core.config import settings
from app.schemas.extraction import CashFlowExtraction


client = genai.Client(api_key=settings.gemini_api_key)


def extract_cash_flow_data(pages: list[dict]) -> CashFlowExtraction:
    document_text = "\n\n".join(
        f"PAGE {page['page_number']}\n{page['text']}"
        for page in pages
    )

    prompt = f"""
You are a financial document extraction system.

Extract ALL meaningful visible financial information from the
Cash Flow Statement below.

DOCUMENT:
{document_text}

REQUIREMENTS:

1. Extract the statement title.
2. Extract company name.
3. Extract reporting periods.
4. Extract currency if explicitly visible.
5. Extract operating cash flow.
6. Extract investing cash flow.
7. Extract financing cash flow.
8. Extract foreign exchange effect if present.
9. Extract net change in cash.
10. Extract opening cash balance if present.
11. Extract closing cash balance.
12. Extract all meaningful visible cash-flow line items.
13. Preserve comparative periods exactly.
14. For every numeric value, preserve the correct period.
15. Provide source text evidence where practical.
16. Provide the page number for evidence.
17. Do NOT calculate or infer missing values.
18. If a value is not present, return null or an empty list as
    appropriate.
19. Parentheses normally represent negative values; preserve the
    financial meaning.
20. Extract information exactly from the document.

IMPORTANT:
Do not invent values.
Do not calculate values that are not explicitly reported.
Do not combine values from different periods.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": CashFlowExtraction,
        },
    )

    return CashFlowExtraction.model_validate_json(response.text)