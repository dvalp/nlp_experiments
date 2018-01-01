import pytesseract
from PIL import Image


def run_ocr(files):
    text_pages = []
    for f in files:
        with Image.open(f) as img:
            text_pages.append(pytesseract.image_to_string(img))

    return '\n'.join(text_pages)
