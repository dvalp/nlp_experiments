"""
Extract text and metadata from xml downloaded from rechtspraak.nl

Elements are extracted and added to the document metadata. This can also be
run as a batch, in which case it returns a generator for iterating through
results.

TODO: The recursive function that makes a dictionary does not handle duplicate
    fields well.
"""
from collections import defaultdict
from itertools import chain
from pathlib import Path
from typing import Dict, Any, Iterator

from lxml import etree

from src.uitspraak_files.process_rechtspraak_zips import XML_DIR
from src.vector_models.fasttext_model import vectorize_text, load_model, VECTOR_SIZE


def parse_xmls(xml_dir: Path = XML_DIR) -> Iterator[Dict[str, Any]]:
    """
    The main work of extracting information from xml is done here. Improving
    access to the metadata by fields would help a lot.

    :return: Dict of data from an XML file
    """
    try:
        vector_model = load_model()
    except FileNotFoundError:
        vector_model = None
        print("No model was loaded because it could not be found, word vectors will be set to zeroes. "
              "This is necessary if training a model for the first time.")

    for fname in xml_dir.rglob('*.xml'):
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

        match = root.find(".//{*}inhoudsindicatie")
        if match is not None:
            document_info["abstract"] = [
                text.strip()
                for text in match.itertext()
                if text.strip()
            ]
        else:
            document_info["abstract"] = [""]

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

        document_info["doc_vector"] = apply_doc_vector(document_info["text"], model=vector_model)

        yield document_info


def apply_doc_vector(text: Dict[str, Any], model):
    if model is None:
        return [0.0] * VECTOR_SIZE
    return vectorize_text(' '.join(chain(*text.values())), ft_model=model)


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
