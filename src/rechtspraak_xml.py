from pathlib import Path

from lxml import etree


def extract_rechtspraak_xml(filename: str):
    root = etree.parse(filename).getroot()
    descriptions = root.find('.//{*}RDF').getchildren()

    document_info = elem2dict(descriptions.pop(0))
    for desc in descriptions:
        document_info.update({key: value for key, value in elem2dict(desc).items() if key not in document_info})

    document_info['abstract'] = [text.strip() for text in root.find('.//{*}inhoudsindicatie').itertext()
                                 if text.strip()]
    document_info['hasVersion'] = [text.strip() for text in root.find('.//{*}hasVersion').itertext() if text.strip()]

    if root.find('.//{*}uitspraak') is not None:
        document_info['text'] = [text.strip() for text in root.find('.//{*}uitspraak').itertext() if text.strip()]

    elif root.find('.//{*}conclusie') is not None:
        document_info['text'] = [text.strip() for text in root.find('.//{*}conclusie').itertext() if text.strip()]
    else:
        print(filename)

    return document_info


def read_xmls(xml_dir="data/sample_dataset/xmls/"):
    xml_paths = Path(xml_dir).rglob("*.xml")
    for document in xml_paths:
        yield extract_rechtspraak_xml(str(document))


def elem2dict(node: etree) -> dict:
    """
    Convert an lxml.etree node tree into a dict.

    Does not work well on some types, ie. lists, references to other parts of
    the documents or duplicate tags, so extra steps are still needed.

    Based on https://gist.github.com/jacobian/795571

    :param node: lxml.etree Element
    :return: Dictionary containing the children of the original node.
    """
    d = {}
    for element in node.iterchildren():
        key = etree.QName(element).localname
        value = element.text if element.text else elem2dict(element)
        d[key] = value
    return d


if __name__ == '__main__':
    read_xmls()
