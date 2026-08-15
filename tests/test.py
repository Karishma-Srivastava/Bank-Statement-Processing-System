from src.pdf_detector import detect_pdf_type
from src.extractor import (
    extract_text,
    extract_ocr_text,
    extract_account_details,
    extract_transactions
)


pdf_path = "E:\Bank_statement_project\data\samples\sample_bank_statement_scanned.pdf"
# pdf_path = "E:\\Bank_statement_project\\data\\samples\\sample_bank_statement_text.pdf"


# --------------------------------
# 1. Detect PDF type
# --------------------------------

pdf_type, page_count = detect_pdf_type(pdf_path)

print("PDF Type:", pdf_type)
print("Pages:", page_count)


# --------------------------------
# 2. Extract text
# --------------------------------

if pdf_type == "text-based":

    text = extract_text(pdf_path)

else:

    text = extract_ocr_text(pdf_path)


# --------------------------------
# 3. Account details
# --------------------------------

account_details = extract_account_details(text)

print("\nAccount Details:")
print(account_details)


# --------------------------------
# 4. Transactions
# --------------------------------

transactions = extract_transactions(text)

print("\nTransactions:")
print(transactions.to_string(index=False))