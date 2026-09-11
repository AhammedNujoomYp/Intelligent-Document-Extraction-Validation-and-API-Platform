const form = document.getElementById("documentForm");
const message = document.getElementById("message");
const documentsTable = document.getElementById("documentsTable");
const processButton = form.querySelector("button[type='submit']");


function setMessage(text, type = "") {
    message.textContent = text;
    message.className = type;
}


function formatDocumentType(type) {
    const labels = {
        invoice: "Invoice",
        balance_sheet: "Balance Sheet",
        profit_and_loss: "Profit & Loss",
        cash_flow_statement: "Cash Flow Statement"
    };

    return labels[type] || type;
}


function formatStatus(status) {
    const value = String(status || "").toUpperCase();

    if (value === "PASS") {
        return `<span class="status status-pass">PASS</span>`;
    }

    if (value === "FAILED" || value === "FAIL") {
        return `<span class="status status-failed">FAILED</span>`;
    }

    return `<span class="status">${value}</span>`;
}


function formatDate(dateString) {
    if (!dateString) {
        return "-";
    }

    const date = new Date(dateString);

    if (Number.isNaN(date.getTime())) {
        return dateString;
    }

    return date.toLocaleString();
}


function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value ?? "";
    return div.innerHTML;
}


async function loadDocuments() {
    try {
        const response = await fetch("/api/v1/documents");

        if (!response.ok) {
            throw new Error(
                "Failed to load processed documents."
            );
        }

        const documents = await response.json();

        documentsTable.innerHTML = "";

        if (!documents || documents.length === 0) {
            documentsTable.innerHTML = `
                <tr>
                    <td colspan="5">
                        No processed documents found.
                    </td>
                </tr>
            `;
            return;
        }

        /*
         * IMPORTANT:
         * Use "doc" instead of "document" here.
         *
         * "document" is already the browser's global DOM object.
         * Using "document" as the loop variable would break:
         * document.createElement(...)
         */

        documents.forEach((doc) => {

            const row = document.createElement("tr");

            const documentName = escapeHtml(
                doc.document_name
            );

            const documentType = escapeHtml(
                formatDocumentType(
                    doc.document_type
                )
            );

            const status = formatStatus(
                doc.processing_status
            );

            const processedAt = escapeHtml(
                formatDate(
                    doc.processed_at
                )
            );

            const encodedName = encodeURIComponent(
                doc.document_name
            );

            row.innerHTML = `
                <td>
                    ${documentName}
                </td>

                <td>
                    ${documentType}
                </td>

                <td>
                    ${status}
                </td>

                <td>
                    ${processedAt}
                </td>

                <td>
                    <a
                        href="/result.html?document_name=${encodedName}"
                        class="view-button"
                    >
                        View Result
                    </a>
                </td>
            `;

            documentsTable.appendChild(row);
        });

    } catch (error) {

        console.error(
            "Error loading documents:",
            error
        );

        documentsTable.innerHTML = `
            <tr>
                <td colspan="5">
                    Unable to load processed documents.
                </td>
            </tr>
        `;
    }
}


form.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const documentType =
            document.getElementById(
                "documentType"
            ).value;

        const file =
            document.getElementById(
                "documentFile"
            ).files[0];

        if (!documentType || !file) {

            setMessage(
                "Please select a document type and file.",
                "message-error"
            );

            return;
        }

        const formData = new FormData();

        formData.append(
            "document_type",
            documentType
        );

        formData.append(
            "file",
            file
        );

        processButton.disabled = true;

        processButton.textContent =
            "Processing...";

        setMessage(
            "Processing document...",
            "message-info"
        );

        try {

            const response = await fetch(
                "/api/v1/documents/process",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data =
                await response.json();

            if (!response.ok) {

                const errorMessage =
                    data?.detail?.error?.message ||
                    data?.detail?.message ||
                    "Document processing failed.";

                throw new Error(
                    errorMessage
                );
            }

            setMessage(
                "Document processed successfully.",
                "message-success"
            );

            /*
             * Reload the processed-document
             * table after successful processing.
             */
            await loadDocuments();

        } catch (error) {

            console.error(
                "Processing error:",
                error
            );

            setMessage(
                error.message ||
                "Document processing failed.",
                "message-error"
            );

        } finally {

            processButton.disabled = false;

            processButton.textContent =
                "Process Document";
        }
    }
);


/*
 * Load existing documents when the page opens.
 */
loadDocuments();