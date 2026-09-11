from typing import Any

from app.schemas.extraction import InvoiceExtraction


TOLERANCE = 0.01


def values_match(
    calculated: float,
    reported: float,
    tolerance: float = TOLERANCE,
) -> bool:
    return abs(calculated - reported) <= tolerance


def validate_invoice(
    invoice: InvoiceExtraction,
) -> dict[str, Any]:

    checks = []
    issues = []

    # --------------------------------------------------
    # 1. Line item validation
    # Quantity × Unit Price ≈ Amount
    # --------------------------------------------------

    for index, item in enumerate(invoice.line_items):

        if (
            item.quantity is not None
            and item.unit_price is not None
            and item.amount is not None
        ):

            calculated = (
                item.quantity * item.unit_price
            )

            variance = calculated - item.amount

            status = (
                "PASS"
                if values_match(
                    calculated,
                    item.amount
                )
                else "FAIL"
            )

            checks.append({
                "name": f"line_item_{index + 1}_check",
                "formula": "quantity * unit_price",
                "operands": {
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                },
                "calculated_value": round(
                    calculated, 2
                ),
                "reported_value": item.amount,
                "variance": round(
                    variance, 2
                ),
                "status": status,
            })

            if status == "FAIL":
                issues.append(
                    f"Line item {index + 1} amount "
                    f"does not reconcile."
                )

    # --------------------------------------------------
    # 2. Line items → subtotal
    # --------------------------------------------------

    line_amounts = [
        item.amount
        for item in invoice.line_items
        if item.amount is not None
    ]

    if line_amounts and invoice.subtotal is not None:

        calculated = sum(line_amounts)

        variance = calculated - invoice.subtotal.value

        status = (
            "PASS"
            if values_match(
                calculated,
                invoice.subtotal.value
            )
            else "FAIL"
        )

        checks.append({
            "name": "line_items_subtotal_check",
            "formula": "sum(line_item_amounts)",
            "operands": {
                "line_item_amounts": line_amounts,
            },
            "calculated_value": round(
                calculated, 2
            ),
            "reported_value": invoice.subtotal.value,
            "variance": round(
                variance, 2
            ),
            "status": status,
        })

        if status == "FAIL":
            issues.append(
                "Line item amounts do not reconcile "
                "with the reported subtotal."
            )

    # --------------------------------------------------
    # 3. Subtotal + Tax - Discount ≈ Total
    # --------------------------------------------------

    if (
        invoice.subtotal is not None
        and invoice.total_amount is not None
    ):

        subtotal = invoice.subtotal.value

        tax = (
            invoice.tax_amount.value
            if invoice.tax_amount is not None
            else 0.0
        )

        discount = (
            invoice.discount.value
            if invoice.discount is not None
            else 0.0
        )

        calculated = subtotal + tax - discount

        reported = invoice.total_amount.value

        variance = calculated - reported

        status = (
            "PASS"
            if values_match(
                calculated,
                reported
            )
            else "FAIL"
        )

        checks.append({
            "name": "invoice_total_check",
            "formula": (
                "subtotal + tax_amount - discount"
            ),
            "operands": {
                "subtotal": subtotal,
                "tax_amount": tax,
                "discount": discount,
            },
            "calculated_value": round(
                calculated, 2
            ),
            "reported_value": reported,
            "variance": round(
                variance, 2
            ),
            "status": status,
        })

        if status == "FAIL":
            issues.append(
                "Subtotal, tax and discount do not "
                "reconcile with total amount."
            )

    # --------------------------------------------------
    # Overall status
    # --------------------------------------------------

    failed_checks = [
        check
        for check in checks
        if check["status"] == "FAIL"
    ]

    if failed_checks:
        overall_status = "FAIL"

    elif checks:
        overall_status = "PASS"

    else:
        overall_status = "NOT_APPLICABLE"

    return {
        "checks": checks,
        "overall_status": overall_status,
        "issues": issues,
    }