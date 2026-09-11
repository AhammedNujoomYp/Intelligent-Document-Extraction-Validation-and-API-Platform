from typing import Any

from app.schemas.extraction import ProfitLossExtraction


# Financial statements often contain rounding differences.
TOLERANCE = 1.00


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


def add_check(
    checks,
    issues,
    name,
    formula,
    operands,
    calculated,
    reported,
):
    """
    Add a standardized validation result.

    If required values are missing, return NOT_APPLICABLE
    instead of assuming or inventing a value.
    """

    if calculated is None or reported is None:

        checks.append({
            "name": name,
            "formula": formula,
            "operands": operands,
            "calculated_value": None,
            "reported_value": reported,
            "variance": None,
            "status": "NOT_APPLICABLE",
        })

        return

    variance = calculated - reported

    status = (
        "PASS"
        if values_match(calculated, reported)
        else "FAIL"
    )

    checks.append({
        "name": name,
        "formula": formula,
        "operands": operands,
        "calculated_value": round(calculated, 2),
        "reported_value": round(reported, 2),
        "variance": round(variance, 2),
        "status": status,
    })

    if status == "FAIL":
        issues.append(
            f"{name} failed. "
            f"Calculated={round(calculated, 2)}, "
            f"Reported={round(reported, 2)}, "
            f"Variance={round(variance, 2)}"
        )


def validate_profit_loss(
    profit_loss: ProfitLossExtraction,
) -> dict[str, Any]:

    checks = []
    issues = []

    for period in profit_loss.periods:

        # -----------------------------------------------------
        # Existing fields
        # -----------------------------------------------------

        revenue = get_period_value(
            profit_loss.revenue,
            period,
        )

        cost_of_sales = get_period_value(
            profit_loss.cost_of_sales,
            period,
        )

        gross_profit = get_period_value(
            profit_loss.gross_profit,
            period,
        )

        operating_expenses = get_period_value(
            profit_loss.operating_expenses,
            period,
        )

        operating_income = get_period_value(
            profit_loss.operating_income,
            period,
        )

        other_income = get_period_value(
            profit_loss.other_income,
            period,
        )

        other_expenses = get_period_value(
            profit_loss.other_expenses,
            period,
        )

        pre_tax_income = get_period_value(
            profit_loss.pre_tax_income,
            period,
        )

        income_tax = get_period_value(
            profit_loss.income_tax,
            period,
        )

        net_income = get_period_value(
            profit_loss.net_income,
            period,
        )

        # -----------------------------------------------------
        # Assignment-specific fields
        # -----------------------------------------------------

        interest_earned = get_period_value(
            profit_loss.interest_earned,
            period,
        )

        interest_expended = get_period_value(
            profit_loss.interest_expended,
            period,
        )

        provisions = get_period_value(
            profit_loss.provisions_and_contingencies,
            period,
        )

        total_income = get_period_value(
            profit_loss.total_income,
            period,
        )

        total_expenditure = get_period_value(
            profit_loss.total_expenditure,
            period,
        )

        profit_before_minority = get_period_value(
            profit_loss.consolidated_net_profit_before_minority_interest,
            period,
        )

        minority_interest = get_period_value(
            profit_loss.minority_interest,
            period,
        )

        consolidated_profit = get_period_value(
            profit_loss.consolidated_net_profit_attributable_to_group,
            period,
        )

        current_profit = get_period_value(
            profit_loss.current_profit,
            period,
        )

        brought_forward_profit = get_period_value(
            profit_loss.brought_forward_profit,
            period,
        )

        total_available = get_period_value(
            profit_loss.total_available_for_appropriation,
            period,
        )

        # =====================================================
        # EXISTING VALIDATIONS
        # =====================================================

        # -----------------------------------------------------
        # 1. Gross Profit
        # -----------------------------------------------------

        calculated = None

        if (
            revenue is not None
            and cost_of_sales is not None
        ):
            calculated = (
                revenue - cost_of_sales
            )

        add_check(
            checks,
            issues,
            f"gross_profit_check_{period}",
            "revenue - cost_of_sales ≈ gross_profit",
            {
                "revenue": revenue,
                "cost_of_sales": cost_of_sales,
            },
            calculated,
            gross_profit,
        )

        # -----------------------------------------------------
        # 2. Operating Income
        # -----------------------------------------------------

        calculated = None

        if (
            gross_profit is not None
            and operating_expenses is not None
        ):
            calculated = (
                gross_profit
                - operating_expenses
            )

        add_check(
            checks,
            issues,
            f"operating_income_check_{period}",
            "gross_profit - operating_expenses ≈ operating_income",
            {
                "gross_profit": gross_profit,
                "operating_expenses": operating_expenses,
            },
            calculated,
            operating_income,
        )

        # -----------------------------------------------------
        # 3. Pre-tax Income
        # -----------------------------------------------------

        calculated = None

        if (
            operating_income is not None
            and other_income is not None
            and other_expenses is not None
        ):
            calculated = (
                operating_income
                + other_income
                - other_expenses
            )

        add_check(
            checks,
            issues,
            f"pre_tax_income_check_{period}",
            "operating_income + other_income - other_expenses ≈ pre_tax_income",
            {
                "operating_income": operating_income,
                "other_income": other_income,
                "other_expenses": other_expenses,
            },
            calculated,
            pre_tax_income,
        )

        # -----------------------------------------------------
        # 4. Net Income
        # -----------------------------------------------------

        calculated = None

        if (
            pre_tax_income is not None
            and income_tax is not None
        ):
            calculated = (
                pre_tax_income
                - income_tax
            )

        add_check(
            checks,
            issues,
            f"net_income_check_{period}",
            "pre_tax_income - income_tax ≈ net_income",
            {
                "pre_tax_income": pre_tax_income,
                "income_tax": income_tax,
            },
            calculated,
            net_income,
        )

        # =====================================================
        # CASE STUDY REQUIRED VALIDATIONS
        # =====================================================

        # -----------------------------------------------------
        # 5. Total Income
        #
        # Interest Earned + Other Income ≈ Total Income
        # -----------------------------------------------------

        calculated = None

        if (
            interest_earned is not None
            and other_income is not None
        ):
            calculated = (
                interest_earned
                + other_income
            )

        add_check(
            checks,
            issues,
            f"total_income_check_{period}",
            "interest_earned + other_income ≈ total_income",
            {
                "interest_earned": interest_earned,
                "other_income": other_income,
            },
            calculated,
            total_income,
        )

        # -----------------------------------------------------
        # 6. Total Expenditure
        #
        # Interest Expended
        # + Operating Expenses
        # + Provisions & Contingencies
        # ≈ Total Expenditure
        # -----------------------------------------------------

        calculated = None

        if (
            interest_expended is not None
            and operating_expenses is not None
            and provisions is not None
        ):
            calculated = (
                interest_expended
                + operating_expenses
                + provisions
            )

        add_check(
            checks,
            issues,
            f"total_expenditure_check_{period}",
            (
                "interest_expended + operating_expenses "
                "+ provisions_and_contingencies "
                "≈ total_expenditure"
            ),
            {
                "interest_expended": interest_expended,
                "operating_expenses": operating_expenses,
                "provisions_and_contingencies": provisions,
            },
            calculated,
            total_expenditure,
        )

        # -----------------------------------------------------
        # 7. Profit Before Minority Interest
        #
        # Total Income - Total Expenditure
        # ≈ Consolidated Net Profit Before Minority Interest
        # -----------------------------------------------------

        calculated = None

        if (
            total_income is not None
            and total_expenditure is not None
        ):
            calculated = (
                total_income
                - total_expenditure
            )

        add_check(
            checks,
            issues,
            f"profit_before_minority_check_{period}",
            (
                "total_income - total_expenditure "
                "≈ consolidated_net_profit_before_minority_interest"
            ),
            {
                "total_income": total_income,
                "total_expenditure": total_expenditure,
            },
            calculated,
            profit_before_minority,
        )

        # -----------------------------------------------------
        # 8. Consolidated Net Profit
        #
        # Profit Before Minority Interest
        # - Minority Interest
        # ≈ Consolidated Net Profit Attributable to Group
        # -----------------------------------------------------

        calculated = None

        if (
            profit_before_minority is not None
            and minority_interest is not None
        ):
            calculated = (
                profit_before_minority
                - minority_interest
            )

        add_check(
            checks,
            issues,
            f"consolidated_profit_check_{period}",
            (
                "profit_before_minority_interest "
                "- minority_interest "
                "≈ consolidated_net_profit_attributable_to_group"
            ),
            {
                "profit_before_minority_interest": profit_before_minority,
                "minority_interest": minority_interest,
            },
            calculated,
            consolidated_profit,
        )

        # -----------------------------------------------------
        # 9. Appropriation
        #
        # Current Profit + Brought Forward Profit
        # ≈ Total Available for Appropriation
        # -----------------------------------------------------

        calculated = None

        if (
            current_profit is not None
            and brought_forward_profit is not None
        ):
            calculated = (
                current_profit
                + brought_forward_profit
            )

        add_check(
            checks,
            issues,
            f"appropriation_check_{period}",
            (
                "current_profit + brought_forward_profit "
                "≈ total_available_for_appropriation"
            ),
            {
                "current_profit": current_profit,
                "brought_forward_profit": brought_forward_profit,
            },
            calculated,
            total_available,
        )

    # =========================================================
    # OVERALL STATUS
    # =========================================================

    failed_checks = [
        check
        for check in checks
        if check["status"] == "FAIL"
    ]

    applicable_checks = [
        check
        for check in checks
        if check["status"] in {
            "PASS",
            "FAIL",
        }
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