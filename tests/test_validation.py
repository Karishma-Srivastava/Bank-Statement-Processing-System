from src.validation import (
    validate_required_columns,
    validate_transaction_values,
    validate_balance_consistency,
    validate_transaction_direction
)

import pandas as pd


df = pd.DataFrame([
    {
        "date": "01/08/2026",
        "description": "SALARY",
        "debit": None,
        "credit": 80000,
        "balance": 80000
    },
    {
        "date": "02/08/2026",
        "description": "SWIGGY",
        "debit": 450,
        "credit": None,
        "balance": 79550
    },
    {
        "date": "03/08/2026",
        "description": "AMAZON",
        "debit": 2200,
        "credit": None,
        "balance": 77350
    }
])


print("Required columns:")
print(validate_required_columns(df))

print("\nTransaction validation:")
print(validate_transaction_values(df))

print("\nBalance validation:")
print(validate_balance_consistency(df))

print("\nDirection validation:")
print(validate_transaction_direction(df))