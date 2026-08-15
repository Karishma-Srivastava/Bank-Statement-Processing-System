import pymupdf

def detect_pdf_type(pdf_path):
    doc = pymupdf.open(pdf_path)

    total_text = ""
    page_count = len(doc)

    for page in doc:
        text = page.get_text("text")
        total_text += text.strip()

    doc.close()

    if len(total_text) > 100:
        return "text-based", page_count

    return "image-based", page_count