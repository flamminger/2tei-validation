"""
Work in progress


Used for finding path variety in Monasterium.net's eXist database dump.
Returns truncated and non-truncated unique xpaths.
Can be used to find variety and position of elements and attributes.

# TODO: Return dict .json with example charter (best with url) as evidence for use of elements/attributes

"""

import os
import re
from lxml import etree
from pprint import pprint
from tqdm import tqdm


def filter_xpath(xpath):
    """Filters an xpath by occurrence of an item order specification.
    """
    return re.sub(r"\[\d+\]", "", xpath)


def extract_xpaths_from_file(file_path, truncate):
    try:
        tree = etree.parse(file_path)
        elements = tree.xpath("//*")
        xpaths = set()

        for element in elements:
            xpath = tree.getpath(element)
            if "*" not in xpath:
                xpaths.add(filter_xpath(xpath)) if truncate == True else xpaths.add(xpath)

            attributes = element.attrib
            for attr, value in attributes.items():
                attr_xpath = f"{xpath}/@{attr}"
                if "*" not in attr_xpath:
                    xpaths.add(filter_xpath(attr_xpath)) if truncate == True else xpaths.add(xpath)

        return list(xpaths)

    except etree.XMLSyntaxError:
        print(f"Error parsing XML file: {file_path}")
        return []


def extract_xpaths_from_directory(directory, truncate=False):
    xpaths = set()

    file_paths = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith("cei.xml"):
                file_path = os.path.join(root, file_name)
                file_paths.append(file_path)

    with tqdm(total=len(file_paths)) as pbar:
        for file_path in file_paths:
            xpaths.update(extract_xpaths_from_file(file_path, truncate=truncate))
            pbar.update(1)

    return list(xpaths)


directory_path = "data/db/mom-data/metadata.charter.public/"

xpath_result = extract_xpaths_from_directory(directory_path)
with open("data/out/xpaths.txt", mode="w") as f:
    for line in sorted(xpath_result):
        f.write(f"{line}\n") 


xpath_result_truncate = extract_xpaths_from_directory(directory_path, truncate=True)
with open("data/out/xpaths_truncated.txt", mode="w") as f:
    for line in sorted(xpath_result_truncate):
        f.write(f"{line}\n")




# TODO: print custom tree
#  def generate_xml_structure(xpath_list):
#     root_element = {}

#     for xpath in xpath_list:
#         elements = xpath.strip('/').split('/')
#         current_element = root_element

#         for element in elements:
#             if element not in current_element:
#                 current_element[element] = {}
#             current_element = current_element[element]

#     def generate_indentation(indent_level):
#         return '  ' * 2 * indent_level

#     def generate_xml_element(element, indent_level=0):
#         result = ''
#         indentation = generate_indentation(indent_level)

#         for key, value in element.items():
#             result += f"{indentation}<{key}>\n"
#             result += generate_xml_element(value, indent_level + 1)
#             result += f"{indentation}</{key}>\n"

#         return result

#     xml_structure = generate_xml_element(root_element)
#     print(xml_structure)