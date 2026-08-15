from src.normalizer import find_transaction_header
from src.extractor import get_normalized_headers


lines = [
    "SAMPLE BANK STATEMENT",
    "Account Holder: Rahul Sharma",
    "Account Number: XXXX1234",
    "Date        Description                  Debit       Credit       Balance",
]


header = find_transaction_header(lines)

print("Detected Header:")
print(header)

normalized = get_normalized_headers(header)

print("\nNormalized Headers:")
print(normalized)