import re


COLUMN_ALIASES = {
    "date": [
        "date",
        "txn date",
        "transaction date",
        "value date",
    ],

    "description": [
        "description",
        "narration",
        "particulars",
        "particular",
        "transaction details",
        "details",
    ],

    "debit": [
        "debit",
        "withdrawal",
        "withdrawals",
        "money out",
        "outflow",
        "dr",
    ],

    "credit": [
        "credit",
        "deposit",
        "deposits",
        "money in",
        "inflow",
        "cr",
    ],

    "balance": [
        "balance",
        "closing balance",
        "available balance",
        "closing amount",
        "closing amt",
    ],
        "date": [
        "date",
        "txn date",
        "transaction date"
    ],

    "description": [
        "description",
        "narration",
        "particulars",
        "details"
    ],

    "debit": [
        "debit",
        "withdrawal",
        "withdrawal amt",
        "withdrawal amount",
        "money out"
    ],

    "credit": [
        "credit",
        "deposit",
        "deposit amt",
        "deposit amount",
        "money in"
    ],

    "balance": [
        "balance",
        "closing balance",
        "available balance"
    ],
}


def clean_column_name(column):
    """
    Standardize formatting of an extracted column name.
    """

    column = str(column).lower().strip()

    column = re.sub(r"\s+", " ", column)

    return column


def normalize_column(column):
    """
    Convert bank-specific column names
    into our canonical schema.
    """

    if not column:
        return None

    column = column.lower().strip()

    # Normalize punctuation
    column = column.replace(".", "")
    column = column.replace("/", " ")
    column = column.replace("-", " ")

    # Remove extra spaces
    column = " ".join(column.split())

    aliases = {
        "date": [
            "date",
            "txn date",
            "transaction date"
        ],

        "description": [
            "description",
            "narration",
            "particulars",
            "details"
        ],

        "debit": [
            "debit",
            "withdrawal",
            "withdrawal amt",
            "withdrawal amount",
            "money out"
        ],

        "credit": [
            "credit",
            "deposit",
            "deposit amt",
            "deposit amount",
            "money in"
        ],

        "balance": [
            "balance",
            "closing balance",
            "available balance"
        ]
    }

    for canonical_name, possible_names in aliases.items():

        if column in possible_names:
            return canonical_name

    return None

def normalize_headers(headers):
    """
    Convert bank-specific headers into our standard schema.

    Example:
    ["Date", "Narration", "Withdrawal", "Deposit", "Balance"]

    becomes:
    ["date", "description", "debit", "credit", "balance"]
    """

    normalized_headers = []
    unknown_headers = []

    for header in headers:

        normalized = normalize_column(header)

        if normalized is None:
            unknown_headers.append(header)
            normalized_headers.append(None)
        else:
            normalized_headers.append(normalized)

    return normalized_headers, unknown_headers

def find_transaction_header(lines):
    """
    Find the line that most likely represents
    the transaction table header.

    Supports different bank-specific terminology.
    """

    for line in lines:

        normalized_line = line.lower()

        # Normalize punctuation
        normalized_line = normalized_line.replace(".", "")
        normalized_line = normalized_line.replace("/", " ")
        normalized_line = normalized_line.replace("-", " ")

        normalized_line = " ".join(
            normalized_line.split()
        )

        # Date-related headers
        has_date = any(
            word in normalized_line
            for word in [
                "date",
                "txn date",
                "transaction date"
            ]
        )

        # Description-related headers
        has_description = any(
            word in normalized_line
            for word in [
                "description",
                "narration",
                "particular",
                "details"
            ]
        )

        # Debit-related headers
        has_debit = any(
            word in normalized_line
            for word in [
                "debit",
                "withdrawal",
                "withdrawal amt",
                "withdrawal amount",
                "money out"
            ]
        )

        # Credit-related headers
        has_credit = any(
            word in normalized_line
            for word in [
                "credit",
                "deposit",
                "deposit amt",
                "deposit amount",
                "money in"
            ]
        )

        # Balance-related headers
        has_balance = any(
            word in normalized_line
            for word in [
                "balance",
                "closing balance",
                "available balance"
            ]
        )

        # Require the core transaction structure.
        if (
            has_date
            and has_description
            and has_balance
            and (has_debit or has_credit)
        ):
            return line

    return None