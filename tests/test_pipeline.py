from src.pipeline import process_statement

import sys

from src.pipeline import process_statement


if len(sys.argv) < 2:
    print("Usage: python test_pipeline.py <pdf_path>")
    sys.exit(1)

pdf_path = sys.argv[1]

result = process_statement(pdf_path)

print("\nAccount Details:")
print(result["account_details"])

print("\nTransactions:")
print(
    result["transactions"].to_string(index=False)
)

print("\nValidation:")
print(result["validation"])
print(result["validation"])