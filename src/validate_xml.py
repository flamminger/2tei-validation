"""
Work in progress


TODO:

Write function to one-shot validate xml schema on dump and log result.


Write functions to find out:
- Which elements can be nested?
- Which elements have duplicates, i.e., can be placed in different parts of the cei?
- What is the scope of duplicates, i.e., in which environments (parents, children) can they be placed? 
"""




import xmlschema
from pprint import pprint
from lxml import etree
import os

xsd = xmlschema.XMLSchema("fsdb/data/schema/cei.xsd")
#file_path = "fsdb/data/db/mom-data/metadata.charter.public/AFM/1.1.1.cei.xml"
file_directory = "fsdb/data/db/mom-data/metadata.charter.public/"


from random import sample

def print_space(length=3):
    for i in range(1,length):
        print("\n")

def get_cei_text(file_path):
    cei_tree = etree.parse(file_path)
    cei_text = cei_tree.find(".//cei:text", namespaces={"cei": "http://www.monasterium.net/NS/cei"})
    content_str = etree.tostring(cei_text, encoding="unicode")
    content_tree = etree.ElementTree(etree.fromstring(content_str))
    return content_tree


file_paths = []
for root, _, files in os.walk(file_directory):
    for file_name in files:
        if file_name.endswith("cei.xml"):
            file_path = os.path.join(root, file_name)
            file_paths.append(file_path)

print(len(file_paths))
valids = []

for file in sample(file_paths, k=1000):
    transformed_text = get_cei_text(file)
    print(transformed_text)
    print(type(transformed_text))
    print(etree.tostring(transformed_text, pretty_print=True, encoding='unicode'))

    validation_result = xsd.is_valid(transformed_text)
    if validation_result:
        valids.append(file)
  

print(len(valids)) # must be erroneouos as such
