import pandas as pd

from src.pdf_detector import detect_pdf_type

from src.extractor import (
    extract_text,
    extract_ocr_text,
    extract_account_details,
    extract_transactions,
    extract_ocr_coordinate_rows
)

from src.validation import (
    validate_required_columns,
    validate_transaction_values,
    validate_balance_consistency,
    validate_transaction_direction
)

from src.coordinate_extractor import (
    extract_coordinate_rows
)


from src.classifier import (
    classify_transaction,
    classify_transaction_ml
)


def process_statement(pdf_path):
    """
    End-to-end bank statement processing pipeline.
    """

    # ---------------------------------------
    # 1. Detect PDF type
    # ---------------------------------------

    pdf_type, page_count = detect_pdf_type(
        pdf_path
    )

    print("PDF Type:", pdf_type)
    print("Pages:", page_count)

    # ---------------------------------------
    # 2. Extract account information
    # ---------------------------------------

    if pdf_type == "text-based":

        text = extract_text(pdf_path)

        account_details = extract_account_details(
            text
        )

        # Use coordinate extraction for
        # structured transaction rows.
        transaction_rows = extract_coordinate_rows(
            pdf_path
        )

    else:

        text = extract_ocr_text(pdf_path)

        account_details = extract_account_details(
            text
        )

        # Use OCR coordinates for scanned tables.
        transaction_rows = extract_ocr_coordinate_rows(
            pdf_path
        )

    # ---------------------------------------
    # 3. Convert transactions to DataFrame
    # ---------------------------------------

    transactions = pd.DataFrame(
        transaction_rows,
        columns=[
            "date",
            "description",
            "debit",
            "credit",
            "balance"
        ]
    )

    # ---------------------------------------
    # 4. Validate schema
    # ---------------------------------------

    schema_result = validate_required_columns(
        transactions
    )

    if not schema_result["valid"]:

        raise ValueError(
            f"Missing columns: "
            f"{schema_result['missing_columns']}"
        )

    # ---------------------------------------
    # 5. Validate transaction values
    # ---------------------------------------

    value_errors = validate_transaction_values(
        transactions
    )

    # ---------------------------------------
    # 6. Validate balance consistency
    # ---------------------------------------

    balance_errors = validate_balance_consistency(
        transactions
    )

        # ---------------------------------------
    # 7. Classification
    # ---------------------------------------

    transactions["rule_based_category"] = (
        transactions["description"]
        .apply(classify_transaction)
    )

    transactions["ml_category"] = (
        transactions["description"]
        .apply(classify_transaction_ml)
    )

    # Primary category remains rule-based.
    transactions["category"] = (
        transactions["rule_based_category"]
    )

    direction_errors = validate_transaction_direction(
        transactions
    )

    review_rows = {
        error["row"]
        for error in direction_errors
    }

    transactions["needs_review"] = transactions.index.map(
        lambda index: index in review_rows
    )
    # ---------------------------------------
    # 8. Return complete result
    # ---------------------------------------

    return {
        "pdf_type": pdf_type,
        "page_count": page_count,
        "account_details": account_details,
        "transactions": transactions,
        "validation": {
            "value_errors": value_errors,
            "balance_errors": balance_errors,
            "direction_errors": direction_errors
    }
    }