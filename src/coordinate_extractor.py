import re
import pymupdf
from src.normalizer import normalize_column


DATE_PATTERN = re.compile(
    r"^\d{2}/\d{2}/(?:\d{2}|\d{4})$"
)

AMOUNT_PATTERN = re.compile(
    r"^-?[\d,]+\.\d{2}$"
)


def group_words_by_line(words, tolerance=3):
    """
    Group PDF words into visual lines using their y-position.
    """

    lines = []

    for word in sorted(words, key=lambda w: (w["top"], w["x0"])):

        placed = False

        for line in lines:

            if abs(line["top"] - word["top"]) <= tolerance:

                line["words"].append(word)
                placed = True
                break

        if not placed:

            lines.append({
                "top": word["top"],
                "words": [word]
            })

    for line in lines:
        line["words"].sort(key=lambda w: w["x0"])

    return lines


def detect_header(words):
    """
    Detect transaction headers and convert bank-specific
    names into the canonical schema.
    """

    lines = group_words_by_line(words)

    for line in lines:

        line_words = line["words"]

        detected = {}
        i = 0

        while i < len(line_words):

            found = False

            # Try 3-word, then 2-word, then 1-word headers.
            for size in [3, 2, 1]:

                if i + size > len(line_words):
                    continue

                phrase_words = line_words[i:i + size]

                phrase = " ".join(
                    word["text"]
                    for word in phrase_words
                )

                normalized = normalize_column(
                    phrase
                )

                if normalized:

                    detected[normalized] = (
                        phrase_words[0]["x0"]
                    )

                    i += size
                    found = True
                    break

            if not found:
                i += 1

        # A transaction header should contain
        # at least date + description + balance,
        # with debit/credit usually also present.
        required = {
            "date",
            "description",
            "balance"
        }

        if required.issubset(detected.keys()):

            print("Detected Header:")

            print(
                " ".join(
                    word["text"]
                    for word in line_words
                )
            )

            print("\nNormalized Header:")

            print(
                list(detected.keys())
            )

            return line["top"], detected

    return None, {}


def parse_amount(value):
    """
    Convert a bank amount string into float.
    """

    try:
        return float(
            value.replace(",", "")
        )
    except ValueError:
        return None


def extract_coordinate_rows(pdf_path):
    """
    Extract transaction rows using PDF word coordinates.

    Works with different column orders and bank-specific
    header names after normalization.
    """

    doc = pymupdf.open(pdf_path)

    all_rows = []

    for page in doc:

        words_raw = page.get_text("words")

        words = []

        for word in words_raw:

            words.append({
                "text": word[4].strip(),
                "x0": word[0],
                "x1": word[2],
                "top": word[1]
            })

        header_y, column_positions = detect_header(
            words
        )

        if not column_positions:
            continue

        # Transaction rows occur below the header.
        transaction_words = [
            word
            for word in words
            if word["top"] > header_y + 5
        ]

        lines = group_words_by_line(
            transaction_words
        )

        for line in lines:

            line_words = line["words"]

            if not line_words:
                continue

            # First word of a transaction should be a date.
            if not DATE_PATTERN.match(
                line_words[0]["text"]
            ):
                continue

            date = line_words[0]["text"]

            description_parts = []

            debit = None
            credit = None
            balance = None

            # Store numeric values together with x-position.
            amounts = []

            for word in line_words[1:]:

                text = word["text"]

                if AMOUNT_PATTERN.match(text):

                    amount = parse_amount(text)

                    amounts.append({
                        "value": amount,
                        "x0": word["x0"]
                    })

                else:

                    description_parts.append(text)

            # Assign each amount to the nearest detected
            # financial column.
            financial_columns = {
                key: x
                for key, x in column_positions.items()
                if key in {
                    "debit",
                    "credit",
                    "balance"
                }
            }

                        # Sort amounts by their horizontal position.
                        # Sort amounts by their horizontal position.
            amounts = sorted(
                amounts,
                key=lambda item: item["x0"]
            )

            if len(amounts) == 3:

                debit = amounts[0]["value"]
                credit = amounts[1]["value"]
                balance = amounts[2]["value"]

            elif len(amounts) == 2:

                balance = amounts[-1]["value"]

                transaction_amount = amounts[0]["value"]

                debit_x = financial_columns.get("debit")
                credit_x = financial_columns.get("credit")
                balance_x = financial_columns.get("balance")

                if (
                    debit_x is not None
                    and credit_x is not None
                    and balance_x is not None
                ):

                    credit_balance_midpoint = (
                        credit_x + balance_x
                    ) / 2

                    if amounts[0]["x0"] < credit_balance_midpoint:
                        debit = transaction_amount
                    else:
                        credit = transaction_amount

            description = " ".join(
                description_parts
            ).strip()
            all_rows.append({
                "date": date,
                "description": description,
                "debit": debit,
                "credit": credit,
                "balance": balance
            })

    doc.close()

    return all_rows