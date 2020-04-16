from pathlib import Path
from zipfile import ZipFile

import requests
from tqdm import tqdm

UITSPRAAK_DIR = Path("../../data/uitspraak_documents")
XML_DIR = Path(UITSPRAAK_DIR, "xmls")
ZIP_DIR = Path(UITSPRAAK_DIR, "zipfiles")
PDF_DIR = Path(UITSPRAAK_DIR, "pdfs")
ZIP_FILE = Path(ZIP_DIR, 'OpenDataUitspraken.zip')
PARSED_FILE = Path(UITSPRAAK_DIR, "parsed_xmls.pkl")


def download_uitspraak_zip(chunk_size=1024) -> None:
    url = "http://static.rechtspraak.nl/PI/OpenDataUitspraken.zip"
    r = requests.get(url, stream=True)
    file_size = int(requests.head(url).headers["Content-Length"])

    with open(ZIP_FILE, 'wb') as fd:
        with tqdm(total=file_size, unit="B", unit_scale=True) as pbar:
            for chunk in tqdm(r.iter_content(chunk_size=chunk_size),
                              total=file_size, unit="B", unit_scale=True):
                fd.write(chunk)
                pbar.update(chunk_size)


def extract_xml(year: str, month: str, refetch=False) -> None:
    year = str(year)
    month = str(month).zfill(2)

    XML_DIR.mkdir(parents=True, exist_ok=True)
    ZIP_DIR.mkdir(parents=True, exist_ok=True)

    if month == "all":
        months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    else:
        months = [month]
    xml_dirs_exist = all((XML_DIR / year / month_number).is_dir() for month_number in months)

    if xml_dirs_exist and not refetch:
        print("XML directory is available for the given months, refetch if files are missing.")
    else:
        if not ZIP_FILE.is_file():
            download_uitspraak_zip()

        # Extract XMLs from ZIP files
        with ZipFile(ZIP_FILE, 'rb') as zipfile:
            if month == 'all':
                files_list = [name for name in zipfile.namelist() if name.startswith(year)]
            else:
                files_list = [f'{year}/{year}{month}.zip']
            zipfile.extractall(path=ZIP_DIR, members=files_list)


def extract_pdf():
    # TODO: Make this happen
    pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Download and extract documents from rechtspraak.nl")
    parser.add_argument("-r", "--refetch", action="store_true", help="Download XML files again")
    parser.add_argument("-y", "--year", default="2020", help="Year to download from (four digit year)")
    parser.add_argument("-m", "--month", default="01",
                        help="Month to download from (two digit month or 'all' for the whole year)")
    parser.add_argument("-d", "--download-only", action="stroe_true",
                        help="Only download the main zip file, don't unpack any months.")
    parser.add_argument("-p", "--download-pdfs", action="store_true",
                        help="Also download PDFs for any extracted XML files.")
    args = parser.parse_args()

    if args.download_only:
        download_uitspraak_zip()
    else:
        extract_xml(year=args.year, month=args.month, refetch=args.refetch)
