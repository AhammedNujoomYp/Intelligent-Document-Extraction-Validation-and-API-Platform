from app.schemas.extraction import (
    Evidence,
    InvoiceExtraction,
    NumericField,
)

from app.services.financial_validation_service import (
    validate_invoice,
)


invoice = InvoiceExtraction(
    subtotal=NumericField(
        value=85.00,
        evidence=Evidence(
            source_text="$85.00",
            page_number=1,
        ),
    ),

    tax_amount=NumericField(
        value=8.50,
        evidence=Evidence(
            source_text="$8.50",
            page_number=1,
        ),
    ),

    discount=NumericField(
        value=0.00,
        evidence=None,
    ),

    total_amount=NumericField(
        value=100,
        evidence=Evidence(
            source_text="$93.50",
            page_number=1,
        ),
    ),
)


result = validate_invoice(invoice)


print("=" * 70)
print("FINANCIAL VALIDATION TEST")
print("=" * 70)

print(result)