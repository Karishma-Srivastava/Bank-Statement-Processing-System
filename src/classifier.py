CATEGORY_RULES = {
    "salary": [
        "salary",
        "payroll",
        "wages"
    ],

    "food": [
        "swiggy",
        "zomato",
        "restaurant",
        "food",
        "cafe",
        "dominos",
        "mcdonald"
    ],

    "shopping": [
        "amazon",
        "flipkart",
        "myntra",
        "shopping",
        "purchase"
    ],

    "transport": [
        "uber",
        "ola",
        "metro",
        "rapido",
        "fuel",
        "petrol"
    ],

    "utilities": [
        "electricity",
        "water bill",
        "gas bill",
        "mobile bill",
        "internet",
        "broadband"
    ],

    "entertainment": [
        "netflix",
        "spotify",
        "prime video",
        "hotstar",
        "movie"
    ],

    "cash_withdrawal": [
        "atm",
        "cash withdrawal",
        "cash withdraw"
    ],

    "transfer": [
        "upi transfer",
        "bank transfer",
        "neft",
        "imps",
        "rtgs"
    ]
}


def classify_transaction(description):
    """
    Classify a transaction using deterministic
    keyword-based rules.
    """

    description = str(description).lower().strip()

    for category, keywords in CATEGORY_RULES.items():

        for keyword in keywords:

            if keyword in description:
                return category

    return "other"