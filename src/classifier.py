from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

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

# --------------------------------------------------
# Traditional ML Classifier
# --------------------------------------------------

ML_TRAINING_DATA = [
    # -----------------------------
    # Salary
    # -----------------------------
    ("monthly salary credit", "salary"),
    ("salary credited", "salary"),
    ("monthly payroll", "salary"),
    ("employee wages", "salary"),
    ("salary payment", "salary"),
    ("salary deposit", "salary"),
    ("salary income", "salary"),

    # -----------------------------
    # Food
    # -----------------------------
    ("swiggy food order", "food"),
    ("zomato restaurant order", "food"),
    ("restaurant payment", "food"),
    ("dominos food", "food"),
    ("cafe payment", "food"),
    ("food delivery", "food"),
    ("food delivery order", "food"),
    ("meal delivery", "food"),
    ("restaurant bill", "food"),
    ("dining payment", "food"),

    # -----------------------------
    # Shopping
    # -----------------------------
    ("amazon purchase", "shopping"),
    ("flipkart purchase", "shopping"),
    ("myntra shopping", "shopping"),
    ("online shopping", "shopping"),
    ("online marketplace payment", "shopping"),
    ("ecommerce purchase", "shopping"),
    ("e commerce order", "shopping"),
    ("online store purchase", "shopping"),
    ("shopping website payment", "shopping"),
    ("retail purchase", "shopping"),

    # -----------------------------
    # Transport
    # -----------------------------
    ("uber trip", "transport"),
    ("ola ride", "transport"),
    ("metro recharge", "transport"),
    ("rapido ride", "transport"),
    ("petrol station", "transport"),
    ("cab booking", "transport"),
    ("taxi ride", "transport"),
    ("ride booking", "transport"),
    ("cab fare", "transport"),
    ("fuel payment", "transport"),

    # -----------------------------
    # Utilities
    # -----------------------------
    ("electricity bill payment", "utilities"),
    ("water bill payment", "utilities"),
    ("gas bill payment", "utilities"),
    ("mobile bill payment", "utilities"),
    ("internet bill", "utilities"),
    ("electricity payment", "utilities"),
    ("water utility bill", "utilities"),
    ("gas utility payment", "utilities"),
    ("broadband bill", "utilities"),
    ("phone bill payment", "utilities"),

    # -----------------------------
    # Entertainment
    # -----------------------------
    ("netflix subscription", "entertainment"),
    ("spotify subscription", "entertainment"),
    ("prime video subscription", "entertainment"),
    ("movie ticket", "entertainment"),
    ("music streaming subscription", "entertainment"),
    ("movie booking", "entertainment"),
    ("cinema ticket", "entertainment"),
    ("video streaming payment", "entertainment"),
    ("music subscription", "entertainment"),

    # -----------------------------
    # Cash Withdrawal
    # -----------------------------
    ("atm cash withdrawal", "cash_withdrawal"),
    ("cash withdrawal", "cash_withdrawal"),
    ("atm withdrawal", "cash_withdrawal"),
    ("cash withdrawn from atm", "cash_withdrawal"),
    ("atm transaction", "cash_withdrawal"),
    ("cash withdrawal transaction", "cash_withdrawal"),

    # -----------------------------
    # Transfer
    # -----------------------------
    ("upi transfer to friend", "transfer"),
    ("bank transfer", "transfer"),
    ("neft transfer", "transfer"),
    ("imps transfer", "transfer"),
    ("rtgs transfer", "transfer"),
    ("upi payment transfer", "transfer"),
    ("fund transfer", "transfer"),
    ("money transfer", "transfer"),
    ("account transfer", "transfer"),
    ("online bank transfer", "transfer")
]

def evaluate_ml_model():
    """
    Evaluate the traditional ML classifier on a held-out test set.
    """

    texts = [item[0] for item in ML_TRAINING_DATA]
    labels = [item[1] for item in ML_TRAINING_DATA]

    X_train_text, X_test_text, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels
    )

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2)
    )

    X_train = vectorizer.fit_transform(X_train_text)
    X_test = vectorizer.transform(X_test_text)

    model = LogisticRegression(
        max_iter=1000
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(X_test)

    return {
        "accuracy": accuracy_score(
            y_test,
            predictions
        ),
        "precision": precision_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0
        ),
        "recall": recall_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0
        ),
        "f1": f1_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0
        )
    }

_ml_texts = [
    item[0]
    for item in ML_TRAINING_DATA
]

_ml_labels = [
    item[1]
    for item in ML_TRAINING_DATA
]


_ml_vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2)
)

_ml_X = _ml_vectorizer.fit_transform(
    _ml_texts
)


_ml_model = LogisticRegression(
    max_iter=1000
)

_ml_model.fit(
    _ml_X,
    _ml_labels
)


def classify_transaction_ml(description):
    """
    Classify a transaction using a traditional
    machine-learning model.

    TF-IDF is used for text representation and
    Logistic Regression is used for classification.
    """

    description = str(description).lower().strip()

    if not description:
        return "other"

    X = _ml_vectorizer.transform(
        [description]
    )

    prediction = _ml_model.predict(X)

    return prediction[0]