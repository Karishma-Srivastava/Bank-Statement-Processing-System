from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


output_path = "data/samples/bank_b_statement.pdf"

c = canvas.Canvas(
    output_path,
    pagesize=A4
)

# Title
c.setFont("Helvetica-Bold", 16)
c.drawString(
    200,
    800,
    "ABC BANK"
)

# Account information
c.setFont("Helvetica", 10)

c.drawString(
    50,
    760,
    "Customer Name: Rahul Sharma"
)

c.drawString(
    50,
    742,
    "A/C No: XXXX1234"
)

c.drawString(
    50,
    724,
    "IFSC Code: HDFC0001234"
)

c.drawString(
    50,
    706,
    "Branch: Delhi Main Branch"
)


# Different bank-style headers
headers = [
    ("Txn Date", 45),
    ("Narration", 95),
    ("Withdrawal", 210),
    ("Deposit", 300),
    ("Closing Balance", 390)
]

c.setFont("Helvetica-Bold", 9)

for header, x in headers:
    c.drawString(
        x,
        660,
        header
    )


# Transactions
transactions = [
    ("01/08/2026", "MONTHLY SALARY", "", "80000.00", "80000.00"),
    ("02/08/2026", "SWIGGY FOOD ORDER", "450.00", "", "79550.00"),
    ("03/08/2026", "AMAZON PURCHASE", "2200.00", "", "77350.00"),
    ("04/08/2026", "UBER TRIP", "320.00", "", "77030.00"),
    ("05/08/2026", "ELECTRICITY BILL", "1800.00", "", "75230.00"),
    ("06/08/2026", "UPI TRANSFER", "1000.00", "", "74230.00"),
]

y = 640

c.setFont("Helvetica", 9)

for row in transactions:

    date, description, withdrawal, deposit, balance = row

    c.drawString(45, y, date)
    c.drawString(95, y, description)

    if withdrawal:
        c.drawRightString(
            270,
            y,
            withdrawal
        )

    if deposit:
        c.drawRightString(
            360,
            y,
            deposit
        )

    c.drawRightString(
        470,
        y,
        balance
    )

    y -= 25


c.drawString(
    50,
    y - 20,
    "Synthetic statement for testing multiple bank layouts."
)

c.save()

print(
    f"Created: {output_path}"
)