from typing import Any

from app.schemas.extraction import BalanceSheetExtraction


TOLERANCE = 0.01


def values_match(
    calculated: float,
    reported: float,
) -> bool:
    return abs(calculated - reported) <= TOLERANCE


def get_period_value(
    values,
    period: str,
):
    for item in values:
        if item.period == period:
            return item.value

    return None


def validate_balance_sheet(
    balance_sheet: BalanceSheetExtraction,
) -> dict[str, Any]:

    checks = []
    issues = []

    # ---------------------------------------------------------
    # Validate each reporting period independently
    # ---------------------------------------------------------

    for period in balance_sheet.periods:

        assets = get_period_value(
            balance_sheet.total_assets,
            period,
        )

        liabilities = get_period_value(
            balance_sheet.total_liabilities,
            period,
        )

        equity = get_period_value(
            balance_sheet.total_equity,
            period,
        )

        # -----------------------------------------------------
        # Required fields unavailable
        # -----------------------------------------------------

        if (
            assets is None
            or liabilities is None
            or equity is None
        ):

            checks.append({
                "name": f"balance_sheet_check_{period}",

                "formula": (
                    "total_liabilities + total_equity "
                    "≈ total_assets"
                ),

                "operands": {
                    "total_assets": assets,
                    "total_liabilities": liabilities,
                    "total_equity": equity,
                },

                "calculated_value": None,

                "reported_value": assets,

                "variance": None,

                "status": "NOT_APPLICABLE",
            })

            continue

        # -----------------------------------------------------
        # Financial calculation
        # -----------------------------------------------------

        calculated = liabilities + equity

        variance = calculated - assets

        status = (
            "PASS"
            if values_match(
                calculated,
                assets,
            )
            else "FAIL"
        )

        checks.append({
            "name": f"balance_sheet_check_{period}",

            "formula": (
                "total_liabilities + total_equity "
                "≈ total_assets"
            ),

            "operands": {
                "total_liabilities": liabilities,
                "total_equity": equity,
            },

            "calculated_value": round(
                calculated,
                2,
            ),

            "reported_value": assets,

            "variance": round(
                variance,
                2,
            ),

            "status": status,
        })

        if status == "FAIL":

            issues.append(
                f"Balance Sheet does not reconcile "
                f"for period {period}."
            )

    # ---------------------------------------------------------
    # Overall validation status
    # ---------------------------------------------------------

    failed_checks = [
        check
        for check in checks
        if check["status"] == "FAIL"
    ]

    applicable_checks = [
        check
        for check in checks
        if check["status"] in {"PASS", "FAIL"}
    ]

    if failed_checks:

        overall_status = "FAIL"

    elif applicable_checks:

        overall_status = "PASS"

    else:

        overall_status = "NOT_APPLICABLE"

    return {
        "checks": checks,
        "overall_status": overall_status,
        "issues": issues,
    }