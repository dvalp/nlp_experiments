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


def download_uitspraak_zip(chunk_size: int = 1024) -> None:
    """
    Download the master zip file of all the XML documents for cases. This file
    contains zip files for each month. These files are the ones unpacked below.

    :param chunk_size: size of the download chunks
    """
    url = "http://static.rechtspraak.nl/PI/OpenDataUitspraken.zip"
    r = requests.get(url, stream=True)
    file_size = int(requests.head(url).headers["Content-Length"])

    with open(ZIP_FILE, 'wb') as fd:
        with tqdm(total=file_size, unit="B", unit_scale=True) as pbar:
            for chunk in r.iter_content(chunk_size=chunk_size):
                fd.write(chunk)
                pbar.update(len(chunk))


def extract_month_zips(year: str, month: str, refetch: bool = False) -> None:
    """
    The main zip file contains a zip file for each month of each year. These
    are extracted so the XML files can be extracted.

    Zip files to be extracted can be chosen by month and year.

    :param year: Year to extract
    :param month: Month to extract
    :param refetch: Force extraction if files exist
    """
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


def extract_xml_files(year: str, month="all", min_size=5000, unlink: bool = True) -> None:
    """
    Extract all XML files for the given year and month. Can also be limited by
    file size. Experience shows that files below a certain size have no
    useful information.

    :param year: Year to extract
    :param month: Month to extract
    :param min_size: Minimum file size to extract
    :param unlink: Remove the zip files when finished extraction
    """
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


def download_pdf(file_id: str) -> None:
    """
    Download a single rechtspraak PDF. It expected to be run in a batch, but
    can also be used individually.

    :param file_id: ID of the case PDF to download
    """
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    url = f'https://uitspraken.rechtspraak.nl/InzienDocument/GetPdf?ecli={file_id}'
    r = requests.get(url, stream=True)
    file_size = int(requests.head(url).headers["Content-Length"])
    save_file = (PDF_DIR / file_id).with_suffix(".pdf")

    with open(save_file, 'wb') as fd:
        with tqdm(total=file_size, unit="B", unit_scale=True, desc=file_id) as pbar:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)
                pbar.update(len(chunk))


def update_pdf_dir() -> None:
    """
    Check for missing PDFs and for PDFs that no longer have a matching XML.
    """
    xml_names = {fname.stem for fname in XML_DIR.rglob("*.xml")}
    pdf_names = {fname.stem for fname in PDF_DIR.rglob("*.pdf")}

    for pdf_stem in pdf_names - xml_names:
        Path(PDF_DIR, pdf_stem).with_suffix('.pdf').unlink(missing_ok=True)

    for pdf_stem in xml_names - pdf_names:
        download_pdf(pdf_stem)


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
    elif args.download_pdfs():
        update_pdf_dir()
    else:
        extract_xml_files(year=args.year, month=args.month)
