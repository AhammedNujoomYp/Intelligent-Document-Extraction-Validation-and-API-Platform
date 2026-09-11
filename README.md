# Financial Document Intelligence Platform

An AI-powered financial document intelligence platform for extracting structured financial information from invoices, balance sheets, profit & loss statements, and cash flow statements.

The system supports both digital and scanned/image-based documents, performs OCR when required, extracts structured financial data using an LLM, validates financial relationships using deterministic Python calculations, persists results in a database, and exposes the results through REST APIs and a web interface.

---

## 1. Project Overview

The Financial Document Intelligence Platform processes financial documents and converts unstructured document content into structured JSON.

### Supported document types

The platform supports exactly four document types:

1. Invoice
2. Balance Sheet
3. Profit & Loss
4. Cash Flow Statement

### Supported input formats

- PDF
- JPG
- PNG

### Document characteristics

The platform supports:

- Digital PDFs
- Scanned PDFs
- JPG images
- PNG images
- Comparative-period financial statements
- Financial tables and line items

PDF documents are limited to a maximum of 3 pages.

---

## 2. Main Features

### Document Processing

- File type validation
- File readability validation
- PDF page-count validation
- Maximum 3-page validation
- Empty/corrupt document handling
- PDF text extraction
- OCR fallback for scanned PDFs
- Image OCR

### AI Extraction

- Structured financial information extraction
- Pydantic-based response validation
- Document-type-specific extraction
- Comparative-period extraction
- Evidence/source text
- Page-number evidence
- Missing values represented as null/empty values
- No intentional calculation or invention during extraction

### Financial Validation

The extracted financial data is validated using deterministic Python calculations.

Validation results contain:

- Formula/check
- Input values
- Calculated value
- Reported value
- Variance
- PASS / FAIL / NOT_APPLICABLE status

### Persistence

Processed documents and results are persisted using SQLite.

### REST API

The backend exposes:

- Document processing endpoint
- Document retrieval endpoint
- Processed document listing endpoint
- Health endpoint
- Swagger/OpenAPI documentation

### Frontend

The web interface provides:

- Document type selection
- File upload
- Document processing
- Processing status
- Processed document dashboard
- Extracted financial information
- Financial validation results
- Validation failures
- Raw JSON result

---

# 3. System Architecture

```text
                         ┌───────────────────────┐
                         │       Frontend        │
                         │      HTML/CSS/JS      │
                         └───────────┬───────────┘
                                     │
                                     │ HTTP
                                     ▼
                         ┌───────────────────────┐
                         │        FastAPI        │
                         │       REST API        │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   File Validation     │
                         │                       │
                         │ PDF/JPG/PNG           │
                         │ Page count            │
                         │ Readability           │
                         │ Integrity              │
                         └───────────┬───────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │      Text / OCR Extraction     │
                    │                                │
                    │ Digital PDF → PyMuPDF          │
                    │ Scanned PDF → Tesseract OCR    │
                    │ JPG/PNG → Tesseract OCR        │
                    └────────────────┬───────────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │    AI Extraction      │
                         │                       │
                         │    Gemini API         │
                         │ Structured JSON       │
                         │ Pydantic validation   │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │ Financial Validation  │
                         │                       │
                         │ Invoice               │
                         │ Balance Sheet         │
                         │ Profit & Loss         │
                         │ Cash Flow              │
                         └───────────┬───────────┘
                                     │
                         ┌───────────┴───────────┐
                         ▼                       ▼
                ┌──────────────────┐    ┌─────────────────┐
                │     SQLite       │    │ Structured JSON │
                │    Database      │    │   API Response  │
                └──────────────────┘    └─────────────────┘