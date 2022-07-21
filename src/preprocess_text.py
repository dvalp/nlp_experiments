import ftfy
from unidecode import unidecode


def fix_text(text: str) -> str:
    return unidecode(ftfy.fix_text(text))


