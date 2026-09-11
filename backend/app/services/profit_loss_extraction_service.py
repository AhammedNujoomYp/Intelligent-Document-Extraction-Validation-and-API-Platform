from google import genai
from google.genai import types

from app.core.config import settings
from app.schemas.extraction import ProfitLossExtraction


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=settings.gemini_api_key
)


# ============================================================
# PROFIT & LOSS EXTRACTION
# ============================================================

def extract_profit_loss_data(
    pages: list[dict],
) -> ProfitLossExtraction:
    """
    Extract structured Profit & Loss information from
    PDF/image extracted text.

    The function:
    - preserves comparative periods
    - extracts all meaningful visible line items
    - extracts case-study-specific financial fields
    - captures evidence and page numbers
    - treats bracketed values as negative
    - does not calculate or invent missing values
    """

    # --------------------------------------------------------
    # Build document text with page markers
    # --------------------------------------------------------

    document_text = "\n\n".join(
        f"--- PAGE {page['page_number']} ---\n"
        f"{page.get('text', '')}"
        for page in pages
    )

    # --------------------------------------------------------
    # Gemini extraction prompt
    # --------------------------------------------------------

    prompt = f"""
You are a financial document extraction system.

The document type is:

PROFIT AND LOSS STATEMENT

Your task is to extract structured financial information
ONLY from the supplied document text.

============================================================
CORE OBJECTIVE
============================================================

Extract ALL meaningful information that is visibly present
in the Profit & Loss statement.

Do not restrict extraction to only the predefined fields.

The output must contain:

1. Statement header information
2. Company information
3. Reporting periods
4. Currency
5. All predefined financial fields that are present
6. Every meaningful visible financial line item
7. Comparative-period values
8. Evidence for important extracted values
9. Additional fields in other_fields when required

============================================================
IMPORTANT EXTRACTION RULES
============================================================

1. Extract information ONLY from the supplied document.

2. Do NOT use outside knowledge.

3. Do NOT invent values.

4. Do NOT infer values that are not explicitly supported
   by the document.

5. Do NOT calculate missing financial values.

6. If a value is missing, unreadable, or not present,
   return null for that value or leave the corresponding
   list empty.

7. Extract every reporting period/year visible in the
   document.

8. Preserve comparative periods independently.

   Example:

   2025 -> value for 2025
   2024 -> value for 2024

   Never combine values from different periods.

9. Values shown in parentheses or brackets represent
   NEGATIVE financial values.

   Example:

   (5,000) -> -5000

   (1,250.50) -> -1250.50

10. Do not treat parentheses as formatting only.

11. Preserve the numerical value accurately.

12. Extract currency only when it is explicitly shown.

13. Extract company name only when present.

14. Extract statement title only when present.

15. Extract every meaningful visible financial line item,
    even if it does not correspond to one of the predefined
    schema fields.

16. Put additional meaningful visible information into
    other_fields.

============================================================
GENERAL PROFIT & LOSS FIELDS
============================================================

Extract the following fields when explicitly present:

- revenue
- cost_of_sales
- gross_profit
- operating_expenses
- operating_income
- other_income
- other_expenses
- pre_tax_income
- income_tax
- net_income

IMPORTANT:

Only extract a field when the corresponding value is
actually supported by the document.

Do NOT calculate these fields.

For example:

Do NOT calculate:

gross_profit = revenue - cost_of_sales

Instead, extract gross_profit only if it is explicitly
reported in the source document.

============================================================
CASE STUDY REQUIRED P&L FIELDS
============================================================

The case study requires financial validation for the
following concepts.

Look for these fields explicitly in the document.

------------------------------------------------------------
1. INTEREST EARNED
------------------------------------------------------------

Extract:

interest_earned

Possible visible labels may include concepts such as:

- Interest Earned
- Interest Income
- Interest Revenue

Use the actual document terminology and map it only when
the meaning is clearly equivalent.

Do not invent the value.

------------------------------------------------------------
2. INTEREST EXPENDED
------------------------------------------------------------

Extract:

interest_expended

Possible visible labels may include:

- Interest Expended
- Interest Expense
- Interest Paid

Only map the value when the document clearly supports
the corresponding concept.

------------------------------------------------------------
3. PROVISIONS AND CONTINGENCIES
------------------------------------------------------------

Extract:

provisions_and_contingencies

Look for the actual visible line item.

Do not calculate it.

------------------------------------------------------------
4. TOTAL INCOME
------------------------------------------------------------

Extract:

total_income

Only populate this field if a total income value is
explicitly reported.

Do NOT calculate:

interest_earned + other_income

The validation layer will perform calculations later.

------------------------------------------------------------
5. TOTAL EXPENDITURE
------------------------------------------------------------

Extract:

total_expenditure

Only populate this field if explicitly reported.

Do NOT calculate it from other fields.

------------------------------------------------------------
6. CONSOLIDATED NET PROFIT BEFORE MINORITY INTEREST
------------------------------------------------------------

Extract:

consolidated_net_profit_before_minority_interest

Look for the corresponding visible line item.

Possible wording may vary.

Only map it when the meaning is clearly supported
by the document.

------------------------------------------------------------
7. MINORITY INTEREST
------------------------------------------------------------

Extract:

minority_interest

Only populate when explicitly present.

If absent, return null/empty.

------------------------------------------------------------
8. CONSOLIDATED NET PROFIT ATTRIBUTABLE TO THE GROUP
------------------------------------------------------------

Extract:

consolidated_net_profit_attributable_to_group

Only populate when the corresponding amount is explicitly
reported.

------------------------------------------------------------
9. CURRENT PROFIT
------------------------------------------------------------

Extract:

current_profit

Only populate when explicitly present.

------------------------------------------------------------
10. BROUGHT FORWARD PROFIT
------------------------------------------------------------

Extract:

brought_forward_profit

Only populate when explicitly present.

------------------------------------------------------------
11. TOTAL AVAILABLE FOR APPROPRIATION
------------------------------------------------------------

Extract:

total_available_for_appropriation

Only populate when explicitly reported.

============================================================
DO NOT PERFORM VALIDATIONS DURING EXTRACTION
============================================================

IMPORTANT:

The extraction service must NOT calculate financial
relationships.

For example, if the document contains:

Interest Earned = 500000
Other Income = 100000
Total Income = 600000

extract all three values independently.

Do NOT generate Total Income if it is not explicitly
reported.

The financial validation service will later calculate:

Interest Earned + Other Income

and compare the calculated value against Total Income.

============================================================
LINE ITEMS
============================================================

The line_items array is extremely important.

Extract EVERY meaningful visible financial line item.

For each line item:

name:
    Use the actual visible line-item name.

values:
    Create one PeriodValue for each reporting period.

period:
    Use the corresponding reporting year/period.

value:
    Extract the actual numerical value.

evidence:
    Provide supporting source text and page number.

Example:

Visible document:

Interest Earned       500,000    450,000

Periods:

2025
2024

Then represent it conceptually as:

name:
    "Interest Earned"

values:

2025 -> 500000
2024 -> 450000

Do not combine the two values.

============================================================
EVIDENCE
============================================================

For extracted values, provide evidence whenever possible.

Evidence contains:

source_text:
    Supporting text copied from the supplied document.

page_number:
    The page where the information appears.

IMPORTANT:

Evidence must come from the supplied document.

Do NOT invent evidence.

Do NOT generate evidence that is not present in the
document.

============================================================
COMPARATIVE PERIODS
============================================================

If the document contains multiple years or periods:

Extract each period separately.

For example:

2025
2024
2023

must remain separate.

Never:

- average them
- combine them
- overwrite one with another
- calculate a new period

============================================================
NUMBER HANDLING
============================================================

Financial numbers may contain:

- commas
- decimal points
- currency symbols
- parentheses
- negative signs

Examples:

"1,250,000" -> 1250000

"1,250.50" -> 1250.50

"(500,000)" -> -500000

"(1,250.50)" -> -1250.50

"$5,000" -> 5000

Do not change the financial meaning of the number.

============================================================
MISSING / UNREADABLE VALUES
============================================================

If a value is not visible or cannot be reliably read:

return:

null

Do NOT:

- guess
- estimate
- infer
- use another year's value
- calculate a replacement value

============================================================
OTHER FIELDS
============================================================

If meaningful visible information exists that does not fit
the predefined schema fields, include it in:

other_fields

Examples may include:

- accounting policy information
- earnings per share
- dividend information
- unusual financial subtotals
- additional statement-specific fields

Only include information actually supported by the document.

============================================================
FINAL CHECK BEFORE RETURNING
============================================================

Before returning the structured response, verify:

1. All visible reporting periods were captured.
2. Comparative values remain separated.
3. All meaningful visible financial line items were captured.
4. Case-study-required fields were extracted when present.
5. Missing fields were not invented.
6. Parentheses were converted to negative values.
7. Evidence refers to actual document text.
8. Page numbers are correct.
9. No financial calculations were performed.
10. No information from outside the document was used.

============================================================
DOCUMENT TEXT
============================================================

{document_text}
"""

    # --------------------------------------------------------
    # Gemini structured generation
    # --------------------------------------------------------

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ProfitLossExtraction,
        ),
    )

    # --------------------------------------------------------
    # Validate Gemini response
    # --------------------------------------------------------

    if not response.text:
        raise ValueError(
            "Gemini returned an empty Profit & Loss extraction response."
        )

    try:
        return ProfitLossExtraction.model_validate_json(
            response.text
        )

    except Exception as exc:
        raise ValueError(
            "Gemini returned an invalid Profit & Loss "
            "structured response."
        ) from exc