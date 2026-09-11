def values_match(calculated, reported, tolerance=0.01):
    if calculated is None or reported is None:
        return False

    return abs(calculated - reported) <= tolerance


def get_period_value(values, period):
    for item in values:
        if item.period == period:
            return item.value

    return None


def add_check(
    checks,
    formula,
    input_values,
    calculated_value,
    reported_value,
):
    if calculated_value is None or reported_value is None:
        status = "NOT_APPLICABLE"
        variance = None
    else:
        variance = calculated_value - reported_value
        status = (
            "PASS"
            if values_match(calculated_value, reported_value)
            else "FAIL"
        )

    checks.append(
        {
            "formula": formula,
            "input_values": input_values,
            "calculated_value": calculated_value,
            "reported_value": reported_value,
            "variance": variance,
            "status": status,
        }
    )


def validate_cash_flow(extracted_data):
    checks = []

    for period in extracted_data.periods:

        operating = get_period_value(
            extracted_data.operating_cash_flow,
            period,
        )

        investing = get_period_value(
            extracted_data.investing_cash_flow,
            period,
        )

        financing = get_period_value(
            extracted_data.financing_cash_flow,
            period,
        )

        fx = get_period_value(
            extracted_data.foreign_exchange_effect,
            period,
        )

        net_change = get_period_value(
            extracted_data.net_change_in_cash,
            period,
        )

        components = [
            operating,
            investing,
            financing,
        ]

        if fx is not None:
            components.append(fx)

        if all(value is not None for value in components):
            calculated_net_change = sum(components)
        else:
            calculated_net_change = None

        add_check(
            checks=checks,
            formula="Operating Cash Flow + Investing Cash Flow + Financing Cash Flow + Foreign Exchange Effect ≈ Net Change in Cash",
            input_values={
                "period": period,
                "operating_cash_flow": operating,
                "investing_cash_flow": investing,
                "financing_cash_flow": financing,
                "foreign_exchange_effect": fx,
            },
            calculated_value=calculated_net_change,
            reported_value=net_change,
        )

        opening_cash = get_period_value(
            extracted_data.opening_cash,
            period,
        )

        closing_cash = get_period_value(
            extracted_data.closing_cash,
            period,
        )

        if opening_cash is not None and net_change is not None:
            calculated_closing_cash = opening_cash + net_change
        else:
            calculated_closing_cash = None

        add_check(
            checks=checks,
            formula="Opening Cash + Net Change in Cash ≈ Closing Cash",
            input_values={
                "period": period,
                "opening_cash": opening_cash,
                "net_change_in_cash": net_change,
            },
            calculated_value=calculated_closing_cash,
            reported_value=closing_cash,
        )

    applicable_checks = [
        check for check in checks
        if check["status"] != "NOT_APPLICABLE"
    ]

    if not applicable_checks:
        overall_status = "NOT_APPLICABLE"
    elif any(
        check["status"] == "FAIL"
        for check in applicable_checks
    ):
        overall_status = "FAIL"
    else:
        overall_status = "PASS"

    return {
        "overall_status": overall_status,
        "checks": checks,
    }