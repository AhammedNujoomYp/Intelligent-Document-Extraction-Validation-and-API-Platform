from app.schemas.extraction import BalanceSheetExtraction
from app.services.balance_sheet_validation_service import (
    validate_balance_sheet,
)


balance_sheet = BalanceSheetExtraction(
    statement_title=None,
    company_name=None,
    periods=["2025", "2024"],
    currency=None,

    total_assets={
    "2025": 1000000.00,
    },

    total_liabilities={
    "2025": 600000.00,
    },

    total_equity={},

    line_items=[],
    other_fields=[],
)


print("=" * 70)
print("BALANCE SHEET VALIDATION TEST")
print("=" * 70)

validation = validate_balance_sheet(balance_sheet)

print(validation)