import unittest
import xml.etree.ElementTree as ET
import logging

from settings import input, output

# TODO add separate test for deeply nested elements

# Configure logging to write to a file
logging.basicConfig(filename='log.txt', level=logging.INFO, filemode='w')

cei = "{http://www.monasterium.net/NS/cei}"
tei = "{http://www.tei-c.org/ns/1.0}"
atom = "{http://www.w3.org/2001/XMLSchema-instance}"


class TestXMLTransform(unittest.TestCase):
    def setUp(self):
        self.source_file = input
        self.target_file = output

    def find_elements(self, tree, xpath):
        return [elem for elem in tree.findall(xpath) if elem.text and elem.text.strip()]

    def test_transformed_content(self):
        tag_pairs = [
            # Add the pairs of tags you want to test here
            # Format: ("source_tag", "target_tag")
            # Header
            (f"{cei}body/{cei}idno", f"{tei}msIdentifier/{tei}idno"),
            (f"{cei}witnessOrig/{cei}archIdentifier/{cei}settlement", f"{tei}msIdentifier/{tei}settlement"),
            (f"{cei}witnessOrig/{cei}archIdentifier/{cei}arch", f"{tei}msDesc/{tei}msIdentifier/{tei}institution"),
            (f"{cei}witnessOrig/{cei}archIdentifier/{cei}arch", f"{tei}msDesc/{tei}msIdentifier/{tei}institution"),
            (f"{cei}witnessOrig/{cei}archIdentifier/{cei}idno",
             f"{tei}msDesc/{tei}msIdentifier/{tei}altIdentifier/{tei}idno"),
            (f"{cei}witnessOrig/{cei}archIdentifier/{cei}archFond",
             f"{tei}msDesc/{tei}msIdentifier/{tei}collection"),
            # PhysicalDesc
            # material
            (f"{cei}witnessOrig/{cei}physicalDesc/{cei}material",
             f"{tei}msDesc/{tei}physDesc/{tei}objectDesc/{tei}supportDesc/{tei}support/{tei}material"),
            # dimensions
            # dimensions
            (f"{cei}witnessOrig/{cei}physicalDesc/{cei}dimensions",
             [f"{tei}msDesc/{tei}physDesc/{tei}objectDesc/{tei}supportDesc/{tei}support/{tei}dimensions",
              f"{tei}msDesc/{tei}physDesc/{tei}objectDesc/{tei}supportDesc/{tei}support/{tei}measure"]),
            (f"{cei}witnessOrig/{cei}physicalDesc/{cei}dimensions/{cei}height",
             f"{tei}msDesc/{tei}physDesc/{tei}objectDesc/{tei}supportDesc/{tei}support/{tei}dimensions/{tei}height"),
            (f"{cei}witnessOrig/{cei}physicalDesc/{cei}dimensions/{cei}width",
             f"{tei}msDesc/{tei}physDesc/{tei}objectDesc/{tei}supportDesc/{tei}support/{tei}dimensions/{tei}width"),
            # layout
            (f"{cei}witnessOrig/{cei}p[@type='layout']",
             f"{tei}msDesc/{tei}physDesc/{tei}objectDesc/{tei}layoutDesc/{tei}layout/{tei}p"),
            # hanDesc
            (f"{cei}witnessOrig/{cei}p[@type='handDesc']",
             f"{tei}msDesc/{tei}physDesc/{tei}handDesc/{tei}p"),
            # decoDesc
            (f"{cei}witnessOrig/{cei}decoDesc",
             f"{tei}msDesc/{tei}physDesc/{tei}decoDesc"),
            (f"{cei}witnessOrig/{cei}decoDesc//{cei}p",
             f"{tei}msDesc/{tei}physDesc/{tei}decoDesc//{cei}p"),
            # diploDesc
            # rubrum
            (f"{cei}witnessOrig/{cei}rubrum",
             f"{tei}msDesc/{tei}diploDesc/{tei}p[@sameAs='rubrum']"),
            # issued
            (f"{cei}chDesc/{cei}issued",
             f"{tei}msDesc/{tei}diploDesc/{tei}issued"),
            ([f"{cei}chDesc/{cei}issued/{cei}dateRange", f"{cei}chDesc/{cei}issued/{cei}date"], f"{tei}origDate"),
            (f"{cei}chDesc/{cei}issued/{cei}placeName",
             f"{tei}msDesc/{tei}diploDesc/{tei}issued/{tei}placeName"),
            # CopyStatus
            (f"{cei}witnessOrig/{cei}traditioForm",
             f"{tei}msDesc/{tei}diploDesc/{tei}copyStatus"),
            # diplomaticAnalysis
            (f"{cei}chDesc/{cei}diplomaticAnalysis",
             f"{tei}msDesc/{tei}diploDesc/{tei}listBibl[@type='analysis']"),
            (f"{cei}chDesc/{cei}diplomaticAnalysis/{cei}listBibl/{cei}bibl",
             f"{tei}msDesc/{tei}diploDesc/{tei}listBibl[@type='analysis']/{tei}bibl"),
            # listWit
            (f"{cei}chDesc/{cei}witListPar",
             f"{tei}listWit"),
            (f"{cei}chDesc/{cei}witListPar/{cei}witness",
             f"{tei}listWit/{tei}witness"),
            (f"{cei}chDesc/{cei}witListPar/{cei}witness/{cei}traditioForm",
             f"{tei}listWit/{tei}witness/{tei}distinct"),
            (f"{cei}chDesc/{cei}witListPar/{cei}witness/{cei}archIdentifier",
             f"{tei}listWit/{tei}witness/{tei}idno"),
            # abstract
            (f"{cei}chDesc/{cei}abstract",
             f"{tei}profileDesc/{tei}abstract/{tei}p"),
            # facsimile
            (f"{cei}chDesc/{cei}witnessOrig/{cei}figure/{cei}zone",
             f"{tei}facsimile//{tei}surface"),
            (f"{cei}chDesc/{cei}witnessOrig/{cei}figure//{cei}figDesc",
             f"{tei}facsimile/{tei}graphic/{tei}desc"),
            # auth
            (f"{cei}auth",
             f"{tei}authDesc"),
            (f"{cei}auth/{cei}sealDesc",
             f"{tei}authDesc/{tei}decoNote"),
            (f"{cei}auth/{cei}sealDesc/{cei}p",
             f"{tei}authDesc/{tei}decoNote/{tei}p"),
            (f"{cei}auth/{cei}sealDesc/{cei}seal",
             f"{tei}authDesc/{tei}seal"),
            (f"{cei}auth/{cei}sealDesc/{cei}seal//{cei}sealDimensions",
             f"{tei}authDesc//{tei}seal/{tei}measure"),
            (f"{cei}auth/{cei}sealDesc/{cei}seal/{cei}sealMaterial",
             f"{tei}authDesc/{tei}seal/{tei}material"),
            (f"{cei}auth/{cei}sealDesc/{cei}seal/{cei}sealCondition",
             f"{tei}authDesc/{tei}seal/{tei}condition"),
            # sourceDesc
            (f"{cei}sourceDesc",
             f"{tei}front/{tei}listBibl"),
            (f"{cei}sourceDesc/{cei}sourceDescRegest/{cei}bibl",
             f"{tei}front/{tei}listBibl/{tei}bibl[@type='regest']"),
            (f"{cei}sourceDesc/{cei}sourceDescVolltext/{cei}bibl",
             f"{tei}front/{tei}listBibl/{tei}bibl[@type='text']"),
            # pTenor
            (f"{cei}pTenor",
             f"{tei}div[@type='tenor']//{tei}p"),
            # back index
            (f"{cei}back//{cei}placeName",
             f"{tei}back//{tei}placeName"),
            (f"{cei}back//{cei}persName",
             f"{tei}back//{tei}persName"),
            (f"{cei}back//{cei}index",
             f"{tei}back//{tei}term"),
            # back divNotes
            (f"{cei}back/{cei}divNotes",
             f"{tei}back/{tei}div"),
            # general elements
            (f"{cei}pb",
             f"{tei}pb"),
            (f"{cei}lb",
             f"{tei}lb"),
            (f"{cei}w",
             f"{tei}w"),
            (f"{cei}c",
             f"{tei}span[@type='char']"),
            (f"{cei}pc",
             f"{tei}pc"),
            (f"{cei}expan[@abbr]",
             f"{tei}abbr"),
            (f"{cei}*/[@reg]",
             f"{tei}reg"),
            (f"{cei}lem",
             f"{tei}lem"),
            (f"{cei}rdg",
             f"{tei}rdg"),
            (f"{cei}app",
             f"{tei}app"),
            (f"{cei}hi",
             f"{tei}hi"),
            (f"{cei}seg",
             f"{tei}span[@inst='seg']"),
            (f"{cei}tenor//{cei}figure",
             f"{tei}div[@type='tenor']//{tei}figure"),
            (f"{cei}issuer",
             f"{tei}legalActor[@type='issuer']"),
            (f"{cei}ref",
             f"{tei}ref"),
            (f"{cei}lang_MOM",
             f"{tei}language"),
            (f"{cei}legend",
             f"{tei}legend"),
        ]

        source_tree = ET.parse(self.source_file)
        target_tree = ET.parse(self.target_file)

        for source_tags, target_tags in tag_pairs:
            source_elements = []
            if isinstance(source_tags, list):
                for source_tag in source_tags:
                    source_elements += self.find_elements(source_tree, f".//{source_tag}")
            else:
                source_elements = self.find_elements(source_tree, f".//{source_tags}")

            target_elements = []
            if isinstance(target_tags, list):
                for target_tag in target_tags:
                    target_elements += self.find_elements(target_tree, f".//{target_tag}")
            else:
                target_elements = self.find_elements(target_tree, f".//{target_tags}")

            self.assertEqual(len(source_elements), len(target_elements),
                             f"Different number of elements between source tags {source_tags} and target tags {target_tags}")

            for source_elem in source_elements:
                matched = False
                for target_elem in target_elements:
                    if (source_elem.text or '').strip() == (target_elem.text or '').strip():
                        logging.info(
                            f"Content matched for source tags {source_tags} and target tag {target_tags} in files {self.source_file} and {self.target_file}")
                        matched = True
                        break  # if a match is found, no need to check other target_elements
                if not matched:
                    logging.error(
                        f"No match found in files {self.source_file} and {self.target_file} for source element with tag {source_elem.tag} and text {source_elem.text}")


if __name__ == '__main__':
    unittest.main()
