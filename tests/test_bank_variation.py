from src.normalizer import normalize_headers


bank_a = [
    "Date",
    "Description",
    "Debit",
    "Credit",
    "Balance"
]

bank_b = [
    "Txn Date",
    "Narration",
    "Withdrawal",
    "Deposit",
    "Closing Balance"
]

bank_c = [
    "Transaction Date",
    "Particulars",
    "Money Out",
    "Money In",
    "Available Balance"
]


for name, headers in [
    ("Bank A", bank_a),
    ("Bank B", bank_b),
    ("Bank C", bank_c)
]:

    normalized, unknown = normalize_headers(headers)

    print(f"\n{name}")
    print("Original :", headers)
    print("Normalized:", normalized)
    print("Unknown  :", unknown)

bank_d = [
    "Date",
    "Narration",
    "Credit",
    "Debit",
    "Balance"
]

normalized, unknown = normalize_headers(bank_d)

print("\nBank D")
print("Original :", bank_d)
print("Normalized:", normalized)
print("Unknown  :", unknown)