from app.services.gemini_extraction_service import extract_invoice_data
from app.services.balance_sheet_extraction_service import extract_balance_sheet_data
from app.services.profit_loss_extraction_service import extract_profit_loss_data
from app.services.cash_flow_extraction_service import extract_cash_flow_data


def extract_financial_data(
    document_type: str,
    pages: list[dict],
):
    if document_type == "invoice":
        return extract_invoice_data(pages)

    if document_type == "balance_sheet":
        return extract_balance_sheet_data(pages)

    if document_type == "profit_and_loss":
        return extract_profit_loss_data(pages)

    if document_type == "cash_flow_statement":
        return extract_cash_flow_data(pages)

    raise ValueError(
        f"Unsupported document type for AI extraction: {document_type}"
    )