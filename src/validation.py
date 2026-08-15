import pandas as pd

REQUIRED_COLUMNS = [
    "date",
    "description",
    "debit",
    "credit",
    "balance"
]


def validate_required_columns(df):
    """
    Check whether the normalized transaction DataFrame
    contains all required columns.
    """

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    return {
        "valid": len(missing) == 0,
        "missing_columns": missing
    }


def validate_transaction_values(df):
    """
    Validate individual transaction values.
    """

    errors = []

    for index, row in df.iterrows():

        # Both debit and credit should not be populated
        if (
            pd.notna(row["debit"])
            and pd.notna(row["credit"])
        ):
            errors.append({
                "row": index,
                "error": "Both debit and credit are populated"
            })

        # Amounts should not be negative
        for column in ["debit", "credit", "balance"]:

            value = row[column]

            if pd.notna(value) and value < 0:

                errors.append({
                    "row": index,
                    "error": f"Negative value in {column}"
                })

    return errors

def validate_balance_consistency(df, tolerance=0.01):
    """
    Check whether the running balance is consistent
    with debit and credit transactions.
    """

    errors = []

    for i in range(1, len(df)):

        previous_balance = df.iloc[i - 1]["balance"]
        current_balance = df.iloc[i]["balance"]

        debit = df.iloc[i]["debit"]
        credit = df.iloc[i]["credit"]

        if pd.isna(previous_balance) or pd.isna(current_balance):
            continue

        debit = 0 if pd.isna(debit) else debit
        credit = 0 if pd.isna(credit) else credit

        expected_balance = (
            previous_balance
            + credit
            - debit
        )

        if abs(expected_balance - current_balance) > tolerance:

            errors.append({
                "row": i,
                "expected_balance": expected_balance,
                "actual_balance": current_balance,
                "error": "Balance mismatch"
            })

    return errors

def validate_transaction_direction(df):
    """
    Identify transactions where neither debit nor credit
    could be determined.
    """

    errors = []

    for index, row in df.iterrows():

        debit_missing = pd.isna(row["debit"])
        credit_missing = pd.isna(row["credit"])

        if debit_missing and credit_missing:

            errors.append({
                "row": index,
                "error": "Transaction direction could not be determined"
            })

    return errors