from pathlib import Path
import requests

UITSPRAAK_DIR = Path("../../data/uitspraak_documents")
XML_DIR = Path(UITSPRAAK_DIR, "xmls")
ZIP_DIR = Path(UITSPRAAK_DIR, "zipfiles")
PDF_DIR = Path(UITSPRAAK_DIR, "pdfs")
ZIP_FILE = Path(ZIP_DIR, 'OpenDataUitspraken.zip')
PARSED_FILE = Path(UITSPRAAK_DIR, "parsed_xmls.pkl")
SMALL_ZIP_FILE_NAME = ['Uitspraken201712.zip']


def download_uitspraak_zip(url="http://static.rechtspraak.nl/PI/OpenDataUitspraken.zip", chunk_size=128):
    r = requests.get(url, stream=True)
    with open(ZIP_DIR, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def extract_xml(year: str, month: str, min_length=5000, refetch=False) -> None:
    year = str(year)
    month = str(month)

    XML_DIR.mkdir(parents=True, exist_ok=True)
    ZIP_DIR.mkdir(parents=True, exist_ok=True)
    xml_subset = XML_DIR/year/month



def extract_pdf():
    pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Download and extract documents from rechtspraak.nl")
    parser.add_argument("-r", "--refetch", action="store_true", help="Download XML files again")
    parser.add_argument("-y", "--year", default="2020", help="Year to download from (four digit year)")
    parser.add_argument("-m", "--month", default="01",
                        help="Month to download from (two digit month or 'all' for the whole year)")
    parser.add_argument("-c", "--case-count", default=20, type=int, help="Number of cases to download")
    parser.add_argument("-x", "--xml-only", action="store_true", help="Only download the XML versions, not the PDFs")

    args = parser.parse_args()


