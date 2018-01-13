import cv2
import pytesseract
from pathlib import Path
from PIL import Image


def run_ocr(imgs: list):
    text_pages = []
    for img in imgs:
        text_pages.append(pytesseract.image_to_string(img))

    return '\n'.join(text_pages)


def open_images(filename: str):
    image_dir = Path('./data/images')
    filenames = sorted(image_dir.glob(filename))
    imgs = []
    for f in filenames:
        imgs.append(cv2.imread(str(f), cv2.IMREAD_GRAYSCALE))

    return imgs
