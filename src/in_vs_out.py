import unittest
import xml.etree.ElementTree as ET
import logging

# Configure logging to write to a file
logging.basicConfig(filename='log.txt', level=logging.INFO, filemode='w')

cei = "{http://www.monasterium.net/NS/cei}"
tei = "{http://www.tei-c.org/ns/1.0}"
atom = "{http://www.w3.org/2001/XMLSchema-instance}"


class TestXMLTransform(unittest.TestCase):
    def setUp(self):
        self.source_file = '/Users/florian/Documents/zim/DiDip/transformation/CEI2TEI/exampleCharters/validated/760-06-99_Marburg.cei.xml'
        self.target_file = '/Users/florian/Documents/zim/DiDip/transformation/CEI2TEI/test.xml'

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
            # PhysicalDesc
            # material
            (f"{cei}witnessOrig/{cei}physicalDesc/{cei}material",
             f"{tei}msDesc/{tei}physDesc/{tei}objectDesc/{tei}supportDesc/{tei}support/{tei}material"),
            (f"{cei}witnessOrig/{cei}physicalDesc/{cei}dimensions",
             # dimensions
             f"{tei}msDesc/{tei}physDesc/{tei}objectDesc/{tei}supportDesc/{tei}support/{tei}dimensions"),
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
            # diploDesc
            # rubrum
            (f"{cei}witnessOrig/{cei}rubrum",
             f"{tei}msDesc/{tei}diploDesc/{tei}p[@sameAs='rubrum']"),
            # issued
            (f"{cei}chDesc/{cei}issued",
             f"{tei}msDesc/{tei}diploDesc/{tei}issued"),
            ([f"{cei}dateRange", f"{cei}date"], f"{tei}origDate"),
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
            # abstract
            (f"{cei}chDesc/{cei}abstract",
             f"{tei}profileDesc/{tei}abstract/{tei}p"),
            # facsimile
            (f"{cei}chDesc/{cei}witnessOrig/{cei}figure",
             f"{tei}facsimile"),
            (f"{cei}chDesc/{cei}witnessOrig/{cei}figure/{cei}zone",
             f"{tei}facsimile//{tei}surface"),
            (f"{cei}chDesc/{cei}witnessOrig/{cei}figure/{cei}graphic",
             f"{tei}facsimile//{tei}graphic"),
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
            (f"{cei}persName",
             f"{tei}persName"),
            (f"{cei}name",
             f"{tei}name"),
            (f"{cei}rolename",
             f"{tei}roleName"),
            (f"{cei}expan[@abbr]",
             f"{tei}abbr"),
            (f"{cei}*/[@reg]",
             f"{tei}reg"),
            (f"{cei}placeName",
             f"{tei}placeName"),
            (f"{cei}tenor//{cei}orgName",
             f"{tei}div[@type='tenor']//{tei}orgName"),
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
            # auth
            (f"{cei}auth",
             f"{tei}authDesc"),
        ]

        source_tree = ET.parse(self.source_file)
        target_tree = ET.parse(self.target_file)

        for source_tags, target_tag in tag_pairs:
            source_elements = []
            if isinstance(source_tags, list):
                for source_tag in source_tags:
                    source_elements += self.find_elements(source_tree, f".//{source_tag}")
            else:
                source_elements = self.find_elements(source_tree, f".//{source_tags}")

            target_elements = self.find_elements(target_tree, f".//{target_tag}")

            self.assertEqual(len(source_elements), len(target_elements),
                             f"Different number of elements between source tags {source_tags} and target tag {target_tag}")

            for source_elem, target_elem in zip(source_elements, target_elements):
                try:
                    self.assertEqual((source_elem.text or '').strip(), (target_elem.text or '').strip())
                    logging.info(
                        f"Content matched for source tags {source_tags} and target tag {target_tag} in files {self.source_file} and {self.target_file}")
                except AssertionError as e:
                    logging.error(
                        f"Error in files {self.source_file} and {self.target_file} for tag pair source tags {source_tags} and target tag {target_tag}. Error: {str(e)}")


if __name__ == '__main__':
    unittest.main()
