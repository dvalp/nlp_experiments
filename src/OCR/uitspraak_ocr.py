from pathlib import Path

import pdf2image
import pytesseract


def ocr_document(pdf_path: Path) -> list[str]:
    """
    Use poppler (in pdf2image) to provide images of pdfs stored in memory. No
    files are stored permanently on the drive. This is probably an improvement
    over the old version that created and stored images for all PDFs on the
    drive.

    :param pdf_path: Path to the PDF being converted
    :return: List of strings, with a string for each page.
    """
    images = pdf2image.convert_from_path(pdf_path, dpi=300, fmt="png", thread_count=6, use_pdftocairo=True)
    texts = [pytesseract.image_to_string(image, lang="nld") for image in images]
    return texts
