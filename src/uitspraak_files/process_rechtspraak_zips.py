from datetime import date
from pathlib import Path
from zipfile import ZipFile

import requests
from tqdm import tqdm

ALL_MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

UITSPRAAK_DIR = Path("/Users/davidvalpey/practice/nlp_experiments/data/uitspraak_documents")
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


def extract_month_zips(year: str, month: str, refetch=False) -> None:
    year = str(year)
    month = str(month).zfill(2)

    ZIP_DIR.mkdir(parents=True, exist_ok=True)

    if month == "all":
        if year == date.today().year:
            months = ALL_MONTHS[:date.today().month]
        else:
            months = ALL_MONTHS
    else:
        months = [month]
    xml_zips_exist = all((ZIP_DIR / f'{year}/{year}{month_number}.zip').is_file() for month_number in months)

    if xml_zips_exist and not refetch:
        print("Zip files available for the given months, refetch if files are missing.")
    else:
        if not ZIP_FILE.is_file():
            download_uitspraak_zip()

        # Extract XMLs from ZIP files
        with ZipFile(ZIP_FILE, 'r') as z:
            if month == 'all':
                files_list = [name for name in z.namelist() if name.startswith(year)]
            else:
                files_list = [f'{year}/{year}{month}.zip']
            z.extractall(path=ZIP_DIR, members=files_list)


def extract_xml_files(year: str, month="all", min_size=5000, unlink=True) -> None:
    year = str(year)
    month = str(month).zfill(2)

    if month == "all":
        zip_paths = (ZIP_DIR / year).rglob("*.zip")
    else:
        zip_paths = [ZIP_DIR / f"{year}/{year}{month}.zip"]

    extract_month_zips(year=year, month=month)

    for fname in zip_paths:
        month = fname.name[4:6]
        with ZipFile(fname, 'r') as z:
            save_path = XML_DIR / year / month
            members = (inf.filename for inf in z.infolist() if inf.file_size > min_size)
            z.extractall(path=save_path, members=members)

        # don't keep completed zip files around
        if unlink:
            fname.unlink()


def download_pdfs():
    # TODO: Make this happen
    pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Download and extract documents from rechtspraak.nl")
    parser.add_argument("-r", "--refetch", action="store_true", help="Download XML files again")
    parser.add_argument("-y", "--year", default="2020", help="Year to download from (four digit year)")
    parser.add_argument("-m", "--month", default="01",
                        help="Month to download from (two digit month or 'all' for the whole year)")
    parser.add_argument("-d", "--download-only", action="store_true",
                        help="Only download the main zip file, don't unpack any months.")
    parser.add_argument("-p", "--download-pdfs", action="store_true",
                        help="Also download PDFs for any extracted XML files.")
    args = parser.parse_args()

    if args.download_only:
        download_uitspraak_zip()
    else:
        extract_xml_files(year=args.year, month=args.month)
