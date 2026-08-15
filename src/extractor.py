import pymupdf
import re
import os
import pandas as pd
import pytesseract
from PIL import Image
from src.normalizer import normalize_column, find_transaction_header

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

if os.name == "nt":

    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    ]

    for path in possible_paths:

        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break

def get_normalized_headers(header_line):
    """
    Convert a detected OCR header line into
    our standard transaction schema.
    """

    text = header_line.lower().strip()

    # Normalize punctuation
    text = text.replace(".", "")
    text = text.replace("/", " ")
    text = text.replace("-", " ")

    # Remove extra spaces
    text = " ".join(text.split())

    # Check known column names/phrases.
    # Order matters for multi-word headers.
    header_aliases = [
        ("date", [
            "transaction date",
            "txn date",
            "date"
        ]),

        ("description", [
            "narration",
            "description",
            "particulars",
            "details"
        ]),

        ("debit", [
            "withdrawal amt",
            "withdrawal amount",
            "withdrawal",
            "debit",
            "money out"
        ]),

        ("credit", [
            "deposit amt",
            "deposit amount",
            "deposit",
            "credit",
            "money in"
        ]),

        ("balance", [
            "closing balance",
            "available balance",
            "balance"
        ])
    ]

    normalized_headers = []

    for canonical, aliases in header_aliases:

        for alias in aliases:

            if alias in text:
                normalized_headers.append(canonical)
                break

    return normalized_headers

def extract_text(pdf_path):
    """
    Extract all text from the PDF.
    """

    doc = pymupdf.open(pdf_path)

    pages = []

    for page in doc:
        text = page.get_text("text")
        pages.append(text)

    doc.close()

    return "\n".join(pages)

def extract_ocr_text(pdf_path):
    """
    Extract text from a scanned/image-based PDF using OCR.
    """

    doc = pymupdf.open(pdf_path)

    pages = []

    for page in doc:

        # Render PDF page as an image
        pix = page.get_pixmap(
            matrix=pymupdf.Matrix(2, 2),
            alpha=False
        )

        # Convert PyMuPDF image to PIL image
        image = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        # Run OCR
        text = pytesseract.image_to_string(
            image,
            config="--psm 6"
        )

        pages.append(text)

    doc.close()

    return "\n".join(pages)

def extract_ocr_coordinate_rows(pdf_path):
    """
    Extract transaction rows from scanned PDFs using
    OCR word coordinates.

    This preserves the table structure instead of relying
    only on OCR plain text.
    """

    doc = pymupdf.open(pdf_path)

    all_rows = []

    date_pattern = re.compile(
        r"^\d{2}/\d{2}/(?:\d{2}|\d{4})$"
    )

    amount_pattern = re.compile(
    r"^[\d,]+(?:\.\d{1,2})?$"
)

    for page in doc:

        pix = page.get_pixmap(
            matrix=pymupdf.Matrix(2, 2),
            alpha=False
        )

        image = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        # IMPORTANT:
        # image_to_data preserves OCR coordinates.
        data = pytesseract.image_to_data(
            image,
            config="--psm 6",
            output_type=pytesseract.Output.DICT
        )

        words = []

        for i in range(len(data["text"])):

            text = data["text"][i].strip()

            if not text:
                continue

            confidence = float(
                data["conf"][i]
            )

            if confidence < 20:
                continue

            words.append({
                "text": text,
                "x": data["left"][i],
                "y": data["top"][i],
                "width": data["width"][i],
                "height": data["height"][i]
            })

        # Group words into visual lines.
        lines = []

        for word in sorted(
            words,
            key=lambda w: (w["y"], w["x"])
        ):

            placed = False

            for line in lines:

                if abs(
                    line["y"] - word["y"]
                ) <= 8:

                    line["words"].append(word)
                    placed = True
                    break

            if not placed:

                lines.append({
                    "y": word["y"],
                    "words": [word]
                })

        for line in lines:

            line["words"].sort(
                key=lambda w: w["x"]
            )

        previous_balance = None

        for line in lines:

            row_words = line["words"]

            if not row_words:
                continue

            # Find a date anywhere near the beginning
            # of the row.
            date_index = None

            for i, word in enumerate(row_words):

                if date_pattern.match(
                    word["text"]
                ):

                    date_index = i
                    break

            if date_index is None:
                continue

            date = row_words[
                date_index
            ]["text"]

            remaining_words = row_words[
                date_index + 1:
            ]

            amounts = []

            for word in remaining_words:

                cleaned = word["text"].replace(
                    "|", ""
                ).replace(
                    ";", ""
                )

                if amount_pattern.match(
                    cleaned
                ):

                    amounts.append({
                        "value": float(
                            cleaned.replace(",", "")
                        ),
                        "x": word["x"]
                    })

            # A valid transaction normally needs
            # at least transaction amount + balance.
            if len(amounts) < 2:
                continue

            balance = amounts[-1]["value"]

            transaction_amount = amounts[-2]["value"]

            # Description = non-numeric words.
            description_words = []

            for word in remaining_words:

                cleaned = word["text"].strip()

                if amount_pattern.match(
                    cleaned.replace("|", "")
                ):
                    continue

                description_words.append(
                    cleaned
                )

            description = " ".join(
                description_words
            ).strip(" |;")

            description_upper = description.upper()

            debit = None
            credit = None

            # Explicit transaction direction.
            if (
                "NEFT DR" in description_upper
                or " RTGS DR" in description_upper
                or description_upper.startswith("DR")
                or " DEBIT" in description_upper
            ):

                debit = transaction_amount

            elif (
                "NEFT CR" in description_upper
                or " RTGS CR" in description_upper
                or description_upper.startswith("CR")
                or " CREDIT" in description_upper
            ):

                credit = transaction_amount

            # Otherwise use balance movement.
            elif previous_balance is not None:

                if balance < previous_balance:
                    debit = transaction_amount

                elif balance > previous_balance:
                    credit = transaction_amount

            all_rows.append({
                "date": date,
                "description": description,
                "debit": debit,
                "credit": credit,
                "balance": balance
            })

            previous_balance = balance

    doc.close()

    return all_rows

def extract_account_details(text):
    """
    Extract account-level information from the statement.
    """

    account_details = {}

    patterns = {
    "account_holder": (
        r"(?:Account\s+Holder|Customer\s+Name|"
        r"A/C\s+Holder|A/C\s+Name)\s*:\s*(.+)"
    ),

    "account_number": (
        r"(?:Account\s+Number|Account\s+No|"
        r"A/C\s+No|A/C\s+Number)\s*:\s*([A-Z0-9]+)"
    ),

    "ifsc": (
        r"(?:IFSC|IFSC\s+Code|RTGS/NEFT\s+IFSC)"
        r"\s*:\s*([A-Z0-9]+)"
    ),

    "branch": (
        r"(?:Branch|Account\s+Branch)\s*:\s*(.+)"
    ),
}

    for field, pattern in patterns.items():

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            account_details[field] = match.group(1).strip()
        else:
            account_details[field] = None

    return account_details


def extract_transactions(text):
    """
    Extract transactions from OCR text.

    The OCR header may be missing or corrupted, so
    transaction rows are identified using dates and
    monetary values instead of relying on the header.
    """

    transactions = []

    lines = text.splitlines()

    previous_balance = None

    for line in lines:

        line = line.strip()

        # OCR can distort dates, so support common
        # dd/mm/yy and dd/mm/yyyy formats.
        date_match = re.match(
            r"^(\d{2}/\d{2}/(?:\d{2}|\d{4}))\s*[|;]?\s*(.*)",
            line
        )

        if not date_match:
            continue

        date = date_match.group(1)
        remaining = date_match.group(2)

        # Find all monetary values.
        amounts = re.findall(
            r"[\d,]+\.\d{2}",
            remaining
        )

        if not amounts:
            continue

        amounts = [
            float(
                amount.replace(",", "")
            )
            for amount in amounts
        ]

        # In the HDFC OCR output, the LAST amount
        # is the closing balance.
        balance = amounts[-1]

        # Everything before the monetary values is
        # treated as the transaction description.
        description = re.sub(
            r"[\d,]+\.\d{2}",
            " ",
            remaining
        )

        description = re.sub(
            r"\s+",
            " ",
            description
        ).strip(" |;")

        debit = None
        credit = None

        # Determine transaction direction.
        #
        # Prefer explicit DR / CR information when
        # available in the narration.
        description_upper = description.upper()

        if (
            " DR-" in f" {description_upper}"
            or description_upper.startswith("DR")
            or " DEBIT" in description_upper
        ):
            debit = amounts[-2] if len(amounts) >= 2 else None

        elif (
            " CR-" in f" {description_upper}"
            or description_upper.startswith("CR")
            or " CREDIT" in description_upper
        ):
            credit = amounts[-2] if len(amounts) >= 2 else None

        # If narration does not explicitly tell us,
        # use balance movement.
        elif previous_balance is not None:

            transaction_amount = (
                amounts[-2]
                if len(amounts) >= 2
                else None
            )

            if transaction_amount is not None:

                if balance > previous_balance:
                    credit = transaction_amount

                elif balance < previous_balance:
                    debit = transaction_amount

        transactions.append({
            "date": date,
            "description": description,
            "debit": debit,
            "credit": credit,
            "balance": balance
        })

        previous_balance = balance

    return pd.DataFrame(
        transactions,
        columns=[
            "date",
            "description",
            "debit",
            "credit",
            "balance"
        ]
    )