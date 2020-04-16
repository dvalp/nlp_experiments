"""
Extract text and metadata from xml downloaded from rechspraak.nl

Elements are extracted and added to the document metadata. This can also be
run as a batch, in which case it returns a generator for iterating through
results.

TODO: The recursive function that makes a dictionary does not handle duplicate
    fields well.
"""
from collections import defaultdict
from typing import Dict

from lxml import etree

from uitspraak_files.download_uitspraken import XML_DIR


def parse_xmls() -> Dict[str, str]:
    """
    The main work of extracting information from an xml is done here. Improving
    access to the metadata by fields would help a lot.

    :return: Dict of data from an XML file
    """
    for fname in XML_DIR.rglob('*.xml'):
        root = etree.parse(str(fname)).getroot()
        datafields = root.find(".//{*}RDF").getchildren()

        document_info = elem2dict(datafields.pop(0))
        document_info["file_id"] = fname.stem
        for desc in datafields:
            document_info.update(
                {
                    key: value
                    for key, value in elem2dict(desc).items()
                    if key not in document_info
                }
            )

        document_info["abstract"] = [
            text.strip()
            for text in root.find(".//{*}inhoudsindicatie").itertext()
            if text.strip()
        ]
        document_info["hasVersion"] = [
            text.strip()
            for text in root.find(".//{*}hasVersion").itertext()
            if text.strip()
        ]
        document_info["legal_domain"] = document_info.get("subject", "").split(";")[0]

        if root.find(".//{*}uitspraak") is not None:
            text_elements = root.find(".//{*}uitspraak").getchildren()
        elif root.find(".//{*}conclusie") is not None:
            text_elements = root.find(".//{*}conclusie").getchildren()
        else:
            text_elements = []
            print(f"Failed to find 'uitspraak' or 'conclusie': {str(fname)}")

        document_info["text"] = defaultdict(dict)
        subsection_id = 1
        for child in text_elements:
            child_text = [
                " ".join(text.split()) for text in child.itertext() if text.strip()
            ]

            if ".info" in child.tag:
                document_info["text"]["info"] = child_text
            elif child.attrib.get("role"):
                document_info["text"][child.attrib.get("role")] = child_text
            else:
                document_info["text"][f"subsection_{subsection_id}"] = child_text
                subsection_id += 1

        yield document_info


def elem2dict(node: etree) -> dict:
    """
    Convert an lxml.etree node tree into a dict using recursion.

    Does not work well on some types, ie. lists, references to other parts of
    the documents or duplicate tags, so extra steps are still needed.

    Based on https://gist.github.com/jacobian/795571

    :param node: lxml.etree Element
    :return: Dictionary containing the children of the original node.
    """
    doc_metadata = {}
    for element in node.iterchildren():
        key = etree.QName(element).localname
        value = element.text.strip() if element.text else elem2dict(element)
        doc_metadata[key] = value
    return doc_metadata
