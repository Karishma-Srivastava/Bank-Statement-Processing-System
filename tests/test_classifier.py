from src.classifier import classify_transaction


transactions = [
    "MONTHLY SALARY CREDIT",
    "SWIGGY FOOD ORDER",
    "AMAZON PURCHASE",
    "UBER TRIP",
    "ELECTRICITY BILL",
    "NETFLIX SUBSCRIPTION",
    "ATM CASH WITHDRAWAL",
    "UPI TRANSFER TO FRIEND",
    "UNKNOWN TRANSACTION"
]


for transaction in transactions:

    category = classify_transaction(transaction)

    print(
        f"{transaction:30} → {category}"
    )