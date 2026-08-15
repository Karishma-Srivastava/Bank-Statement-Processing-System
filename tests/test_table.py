import pdfplumber
from src.coordinate_extractor import extract_coordinate_rows

pdf_path = "E:\Bank_statement_project\data\samples\sample_bank_statement_text.pdf"


rows = extract_coordinate_rows(pdf_path)

print("\nExtracted rows:")

for row in rows:
    print(row)

# with pdfplumber.open(pdf_path) as pdf:

#     page = pdf.pages[0]

#     words = page.extract_words()

#     for word in words:
#         print(
#             word["text"],
#             "x0=", round(word["x0"], 2),
#             "x1=", round(word["x1"], 2),
#             "top=", round(word["top"], 2)
#  )