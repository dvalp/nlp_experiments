from pathlib import Path

import pdf2image
import pytesseract


def ocr_document(pdf_path: Path):
    images = pdf2image.convert_from_path(pdf_path)
    texts = [pytesseract.image_to_string(image, lang="nld") for image in images]
    return texts
