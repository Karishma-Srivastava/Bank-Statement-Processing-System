from src.pipeline import process_statement
from src.exporter import export_csv, export_excel


pdf_path = "E:\\Bank_statement_project\\data\\samples\\sample_bank_statement_text.pdf"

result = process_statement(pdf_path)

transactions = result["transactions"]

csv_path = export_csv(
    transactions,
    "output/transactions.csv"
)

excel_path = export_excel(
    transactions,
    "output/transactions.xlsx"
)

print("CSV created:", csv_path)
print("Excel created:", excel_path)