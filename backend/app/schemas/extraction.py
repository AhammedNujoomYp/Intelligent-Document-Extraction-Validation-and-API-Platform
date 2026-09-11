from typing import Optional

from pydantic import BaseModel, Field


# ============================================================
# COMMON SCHEMAS
# ============================================================

class Evidence(BaseModel):
    source_text: Optional[str] = Field(
        default=None,
        description="Exact supporting text from the source document."
    )

    page_number: Optional[int] = Field(
        default=None,
        description="Page number where the value appears."
    )


class ExtractedField(BaseModel):
    value: Optional[str | float | int] = Field(
        default=None,
        description="Extracted value. Return null when missing or unreadable."
    )

    evidence: Optional[Evidence] = Field(
        default=None,
        description="Supporting source text and page number."
    )


class NumericField(BaseModel):
    value: Optional[float] = Field(
        default=None,
        description="Numeric financial value."
    )

    evidence: Optional[Evidence] = Field(
        default=None,
        description="Supporting source text and page number."
    )


# ============================================================
# INVOICE
# ============================================================

class InvoiceLineItem(BaseModel):
    description: Optional[str] = None

    quantity: Optional[float] = None

    unit_price: Optional[float] = None

    amount: Optional[float] = None

    adjustment: Optional[str] = None

    evidence: Optional[Evidence] = None


class InvoiceExtraction(BaseModel):
    invoice_number: Optional[ExtractedField] = None

    order_number: Optional[ExtractedField] = None

    invoice_date: Optional[ExtractedField] = None

    due_date: Optional[ExtractedField] = None

    vendor_name: Optional[ExtractedField] = None

    vendor_address: Optional[ExtractedField] = None

    vendor_email: Optional[ExtractedField] = None

    customer_name: Optional[ExtractedField] = None

    customer_address: Optional[ExtractedField] = None

    customer_email: Optional[ExtractedField] = None

    currency: Optional[ExtractedField] = None

    subtotal: Optional[NumericField] = None

    tax_amount: Optional[NumericField] = None

    discount: Optional[NumericField] = None

    total_amount: Optional[NumericField] = None

    total_due: Optional[NumericField] = None

    payment_terms: Optional[ExtractedField] = None

    late_payment_terms: Optional[ExtractedField] = None

    payment_status: Optional[ExtractedField] = None

    bank_name: Optional[ExtractedField] = None

    bank_account_number: Optional[ExtractedField] = None

    bank_bsb: Optional[ExtractedField] = None

    line_items: list[InvoiceLineItem] = Field(
        default_factory=list
    )

    other_fields: list[ExtractedField] = Field(
        default_factory=list
    )


# ============================================================
# COMMON PERIOD VALUE
# ============================================================

class PeriodValue(BaseModel):
    period: str = Field(
        description="Financial reporting period, such as 2025 or FY2025."
    )

    value: Optional[float] = Field(
        default=None,
        description=(
            "Financial value for the period. "
            "Parentheses/brackets must be represented as negative numbers. "
            "Return null when missing or unreadable."
        )
    )

    evidence: Optional[Evidence] = Field(
        default=None,
        description="Supporting source text and page number."
    )


# ============================================================
# BALANCE SHEET
# ============================================================

class BalanceSheetLineItem(BaseModel):
    name: Optional[str] = None

    values: list[PeriodValue] = Field(
        default_factory=list
    )

    evidence: Optional[Evidence] = None


class BalanceSheetExtraction(BaseModel):
    statement_title: Optional[ExtractedField] = None

    company_name: Optional[ExtractedField] = None

    periods: list[str] = Field(
        default_factory=list
    )

    currency: Optional[ExtractedField] = None

    total_assets: list[PeriodValue] = Field(
        default_factory=list
    )

    total_liabilities: list[PeriodValue] = Field(
        default_factory=list
    )

    total_equity: list[PeriodValue] = Field(
        default_factory=list
    )

    # Required where the document explicitly reports
    # Total Capital & Liabilities.
    total_capital_and_liabilities: list[PeriodValue] = Field(
        default_factory=list
    )

    line_items: list[BalanceSheetLineItem] = Field(
        default_factory=list
    )

    other_fields: list[ExtractedField] = Field(
        default_factory=list
    )


# ============================================================
# PROFIT & LOSS
# ============================================================

class ProfitLossLineItem(BaseModel):
    name: Optional[str] = None

    values: list[PeriodValue] = Field(
        default_factory=list
    )

    evidence: Optional[Evidence] = None


class ProfitLossExtraction(BaseModel):
    statement_title: Optional[ExtractedField] = None

    company_name: Optional[ExtractedField] = None

    periods: list[str] = Field(
        default_factory=list
    )

    currency: Optional[ExtractedField] = None

    # --------------------------------------------------------
    # Existing / general P&L fields
    # --------------------------------------------------------

    revenue: list[PeriodValue] = Field(
        default_factory=list
    )

    cost_of_sales: list[PeriodValue] = Field(
        default_factory=list
    )

    gross_profit: list[PeriodValue] = Field(
        default_factory=list
    )

    operating_expenses: list[PeriodValue] = Field(
        default_factory=list
    )

    operating_income: list[PeriodValue] = Field(
        default_factory=list
    )

    other_income: list[PeriodValue] = Field(
        default_factory=list
    )

    other_expenses: list[PeriodValue] = Field(
        default_factory=list
    )

    pre_tax_income: list[PeriodValue] = Field(
        default_factory=list
    )

    income_tax: list[PeriodValue] = Field(
        default_factory=list
    )

    net_income: list[PeriodValue] = Field(
        default_factory=list
    )

    # --------------------------------------------------------
    # CASE STUDY REQUIRED P&L FIELDS
    # --------------------------------------------------------

    # Interest Earned
    interest_earned: list[PeriodValue] = Field(
        default_factory=list
    )

    # Interest Expended
    interest_expended: list[PeriodValue] = Field(
        default_factory=list
    )

    # Provisions & Contingencies
    provisions_and_contingencies: list[PeriodValue] = Field(
        default_factory=list
    )

    # Total Income
    total_income: list[PeriodValue] = Field(
        default_factory=list
    )

    # Total Expenditure
    total_expenditure: list[PeriodValue] = Field(
        default_factory=list
    )

    # Consolidated Net Profit before Minority Interest
    consolidated_net_profit_before_minority_interest: list[PeriodValue] = Field(
        default_factory=list
    )

    # Minority Interest
    minority_interest: list[PeriodValue] = Field(
        default_factory=list
    )

    # Consolidated Net Profit attributable to the Group
    consolidated_net_profit_attributable_to_group: list[PeriodValue] = Field(
        default_factory=list
    )

    # Current Profit
    current_profit: list[PeriodValue] = Field(
        default_factory=list
    )

    # Brought Forward Profit
    brought_forward_profit: list[PeriodValue] = Field(
        default_factory=list
    )

    # Total Available for Appropriation
    total_available_for_appropriation: list[PeriodValue] = Field(
        default_factory=list
    )

    # --------------------------------------------------------
    # Complete visible line items
    # --------------------------------------------------------

    line_items: list[ProfitLossLineItem] = Field(
        default_factory=list
    )

    # Any meaningful visible fields not represented above.
    other_fields: list[ExtractedField] = Field(
        default_factory=list
    )


# ============================================================
# CASH FLOW STATEMENT
# ============================================================

class CashFlowLineItem(BaseModel):
    name: Optional[str] = None

    values: list[PeriodValue] = Field(
        default_factory=list
    )

    evidence: Optional[Evidence] = None


class CashFlowExtraction(BaseModel):
    statement_title: Optional[ExtractedField] = None

    company_name: Optional[ExtractedField] = None

    periods: list[str] = Field(
        default_factory=list
    )

    currency: Optional[ExtractedField] = None

    # --------------------------------------------------------
    # Cash flow categories
    # --------------------------------------------------------

    operating_cash_flow: list[PeriodValue] = Field(
        default_factory=list
    )

    investing_cash_flow: list[PeriodValue] = Field(
        default_factory=list
    )

    financing_cash_flow: list[PeriodValue] = Field(
        default_factory=list
    )

    foreign_exchange_effect: list[PeriodValue] = Field(
        default_factory=list
    )

    # --------------------------------------------------------
    # Cash reconciliation
    # --------------------------------------------------------

    net_change_in_cash: list[PeriodValue] = Field(
        default_factory=list
    )

    opening_cash: list[PeriodValue] = Field(
        default_factory=list
    )

    closing_cash: list[PeriodValue] = Field(
        default_factory=list
    )

    # --------------------------------------------------------
    # Complete visible line items
    # --------------------------------------------------------

    line_items: list[CashFlowLineItem] = Field(
        default_factory=list
    )

    other_fields: list[ExtractedField] = Field(
        default_factory=list
    )