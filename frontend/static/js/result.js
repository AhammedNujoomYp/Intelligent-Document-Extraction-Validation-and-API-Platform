const params = new URLSearchParams(window.location.search);

const documentName = params.get("document_name");


const summaryContainer =
    document.getElementById("summary");

const fileValidationContainer =
    document.getElementById("fileValidation");

const extractedDataContainer =
    document.getElementById("extractedData");

const financialValidationContainer =
    document.getElementById("validation");

const processingMetadataContainer =
    document.getElementById("processingMetadata");

const rawJsonContainer =
    document.getElementById("rawJson");

const documentTitle =
    document.getElementById("documentTitle");

const documentSubtitle =
    document.getElementById("documentSubtitle");


function escapeHtml(value) {

    const div = document.createElement("div");

    div.textContent = value ?? "";

    return div.innerHTML;
}


function formatLabel(key) {

    return String(key)
        .replace(/_/g, " ")
        .replace(/\b\w/g, char => char.toUpperCase());
}


function formatValue(value) {

    if (value === null || value === undefined) {
        return "Not available";
    }

    if (typeof value === "boolean") {
        return value ? "Yes" : "No";
    }

    if (typeof value === "number") {
        return value.toLocaleString();
    }

    return escapeHtml(String(value));
}


function formatDocumentType(type) {

    const labels = {
        invoice: "Invoice",
        balance_sheet: "Balance Sheet",
        profit_and_loss: "Profit & Loss",
        cash_flow_statement: "Cash Flow Statement"
    };

    return labels[type] || formatLabel(type);
}


function getStatusClass(status) {

    const value =
        String(status || "").toUpperCase();

    if (value === "PASS") {
        return "status-pass";
    }

    if (
        value === "FAIL" ||
        value === "FAILED"
    ) {
        return "status-failed";
    }

    return "";
}


function renderObject(value) {

    if (
        value === null ||
        value === undefined
    ) {
        return "Not available";
    }


    if (
        typeof value !== "object"
    ) {
        return formatValue(value);
    }


    if (Array.isArray(value)) {

        if (value.length === 0) {
            return "Not available";
        }

        return `
            <div class="data-list">

                ${value.map(
                    (item, index) => `
                        <div class="data-card">

                            <h4>
                                Item ${index + 1}
                            </h4>

                            ${renderObject(item)}

                        </div>
                    `
                ).join("")}

            </div>
        `;
    }


    const entries =
        Object.entries(value);


    if (entries.length === 0) {
        return "Not available";
    }


    return `
        <div class="data-grid">

            ${entries.map(
                ([key, itemValue]) => `

                    <div class="data-item">

                        <div class="data-label">
                            ${escapeHtml(
                                formatLabel(key)
                            )}
                        </div>

                        <div class="data-value">
                            ${renderObject(
                                itemValue
                            )}
                        </div>

                    </div>

                `
            ).join("")}

        </div>
    `;
}


function renderProcessingSummary(data) {

    const status =
        String(
            data.processing_status || ""
        ).toUpperCase();


    summaryContainer.innerHTML = `

        <div class="result-grid">

            <div>

                <strong>
                    Document Name
                </strong>

                <p>
                    ${escapeHtml(
                        data.document_name
                    )}
                </p>

            </div>


            <div>

                <strong>
                    Document Type
                </strong>

                <p>
                    ${escapeHtml(
                        formatDocumentType(
                            data.document_type
                        )
                    )}
                </p>

            </div>


            <div>

                <strong>
                    Processing Status
                </strong>

                <p>

                    <span class="status ${getStatusClass(status)}">

                        ${escapeHtml(status)}

                    </span>

                </p>

            </div>


            <div>

                <strong>
                    Confidence
                </strong>

                <p>
                    ${
                        data.confidence !== null &&
                        data.confidence !== undefined
                            ? `${escapeHtml(
                                String(data.confidence)
                              )}%`
                            : "Not available"
                    }
                </p>

            </div>

        </div>

    `;
}


function renderFileValidation(data) {

    const validation =
        data.file_validation || {};


    fileValidationContainer.innerHTML = `

        <div class="result-grid">

            <div>

                <strong>
                    File Type
                </strong>

                <p>
                    ${formatValue(
                        validation.file_type
                    )}
                </p>

            </div>


            <div>

                <strong>
                    Supported
                </strong>

                <p>
                    ${formatValue(
                        validation.is_supported
                    )}
                </p>

            </div>


            <div>

                <strong>
                    Readable
                </strong>

                <p>
                    ${formatValue(
                        validation.is_readable
                    )}
                </p>

            </div>


            <div>

                <strong>
                    Page Count
                </strong>

                <p>
                    ${formatValue(
                        validation.page_count
                    )}
                </p>

            </div>


            <div>

                <strong>
                    Status
                </strong>

                <p>

                    <span class="status ${
                        getStatusClass(
                            validation.status
                        )
                    }">

                        ${formatValue(
                            validation.status
                        )}

                    </span>

                </p>

            </div>

        </div>


        ${
            validation.error_message
                ? `
                    <p class="error-text">

                        ${escapeHtml(
                            validation.error_message
                        )}

                    </p>
                `
                : ""
        }

    `;
}


function renderExtractedData(data) {

    if (
        data.extracted_data === null ||
        data.extracted_data === undefined
    ) {

        extractedDataContainer.innerHTML = `
            <p>
                No extracted data available.
            </p>
        `;

        return;
    }


    extractedDataContainer.innerHTML =
        renderObject(
            data.extracted_data
        );
}


function renderFinancialValidation(data) {

    const validation =
        data.validation || {};

    const checks =
        validation.checks || [];

    const overallStatus =
        validation.overall_status ||
        "NOT_APPLICABLE";


    let html = `

        <div class="validation-summary">

            <strong>
                Overall Status:
            </strong>

            <span class="status ${
                getStatusClass(
                    overallStatus
                )
            }">

                ${escapeHtml(
                    overallStatus
                )}

            </span>

        </div>

    `;


    if (checks.length === 0) {

        html += `

            <p>
                No financial validation
                checks were applicable.
            </p>

        `;

        financialValidationContainer.innerHTML =
            html;

        return;
    }


    html += `

        <div class="validation-checks">

            ${checks.map(
                (check, index) => `

                    <div class="data-card">

                        <h4>

                            ${escapeHtml(
                                check.name ||
                                `Validation Check ${index + 1}`
                            )}

                        </h4>


                        <p>

                            <strong>
                                Formula:
                            </strong>

                            ${escapeHtml(
                                check.formula || "-"
                            )}

                        </p>


                        <p>

                            <strong>
                                Status:
                            </strong>

                            <span class="status ${
                                getStatusClass(
                                    check.status
                                )
                            }">

                                ${escapeHtml(
                                    check.status ||
                                    "NOT_APPLICABLE"
                                )}

                            </span>

                        </p>


                        <p>

                            <strong>
                                Calculated Value:
                            </strong>

                            ${formatValue(
                                check.calculated_value
                            )}

                        </p>


                        <p>

                            <strong>
                                Reported Value:
                            </strong>

                            ${formatValue(
                                check.reported_value
                            )}

                        </p>


                        <p>

                            <strong>
                                Variance:
                            </strong>

                            ${formatValue(
                                check.variance
                            )}

                        </p>


                        <p>

                            <strong>
                                Input Values:
                            </strong>

                        </p>


                        ${renderObject(
                            check.input_values ||
                            check.operands ||
                            {}
                        )}

                    </div>

                `
            ).join("")}

        </div>

    `;


    financialValidationContainer.innerHTML =
        html;
}


function renderProcessingMetadata(data) {

    const metadata =
        data.processing_metadata || {};


    processingMetadataContainer.innerHTML =
        renderObject(metadata);
}


async function loadResult() {

    if (!documentName) {

        summaryContainer.innerHTML = `

            <p class="error-text">

                No document name was provided.

            </p>

        `;

        return;
    }


    try {

        const encodedName =
            encodeURIComponent(
                documentName
            );


        const response =
            await fetch(
                `/api/v1/documents/${encodedName}`
            );


        if (!response.ok) {

            let errorMessage =
                "Failed to load document result.";


            try {

                const errorData =
                    await response.json();


                errorMessage =
                    errorData?.detail?.error?.message ||
                    errorData?.detail?.message ||
                    errorMessage;

            } catch (_) {

                // Ignore JSON parsing error.

            }


            throw new Error(
                errorMessage
            );
        }


        const data =
            await response.json();


        /*
         * Update page header
         */

        documentTitle.textContent =
            data.document_name ||
            "Document Result";


        documentSubtitle.textContent =
            `${formatDocumentType(
                data.document_type
            )} processing result`;


        /*
         * Render all sections
         */

        renderProcessingSummary(data);

        renderFileValidation(data);

        renderExtractedData(data);

        renderFinancialValidation(data);

        renderProcessingMetadata(data);


        /*
         * Raw JSON
         */

        rawJsonContainer.textContent =
            JSON.stringify(
                data,
                null,
                2
            );


    } catch (error) {

        console.error(
            "Error loading document result:",
            error
        );


        const errorMessage =
            error.message ||
            "Unable to load document result.";


        const errorHtml = `

            <p class="error-text">

                ${escapeHtml(
                    errorMessage
                )}

            </p>

        `;


        summaryContainer.innerHTML =
            errorHtml;

        fileValidationContainer.innerHTML =
            errorHtml;

        extractedDataContainer.innerHTML =
            errorHtml;

        financialValidationContainer.innerHTML =
            errorHtml;

        processingMetadataContainer.innerHTML =
            errorHtml;

        rawJsonContainer.textContent =
            errorMessage;
    }
}


function goBack() {

    window.location.href = "/";
}


loadResult();