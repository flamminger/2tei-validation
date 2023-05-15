import unittest
from lxml import etree

NAMESPACE = {'cei': 'http://www.monasterium.net/NS/cei',
             '': 'http://www.tei-c.org/ns/1.0'}


class TestXMLTransform(unittest.TestCase):
    def get_element_text(self, xml, element):
        element = xml.xpath(f"//*[local-name() = '{element}']")
        return element[0].text if element else None

    def compare_elements(self, input_xml, output_xml, element):
        input_text = self.get_element_text(input_xml, element)
        output_text = self.get_element_text(output_xml, element)
        if input_text != output_text:
            print(f"Mismatch in '{element}': '{input_text}' != '{output_text}'")
            return False
        return True

    def test_xml_transform(self):
        # parse the input xml file
        input_xml = etree.parse('../data/input.xml')

        # parse the output xml file
        output_xml = etree.parse('../data/output.xml')

        # elements to compare
        elements_to_compare = ['idno', 'settlement', 'material', 'zone']

        # list to store names of files which failed the test
        failed_files = []

        for element in elements_to_compare:
            if not self.compare_elements(input_xml, output_xml, element):
                failed_files.append('../data/input.xml')  # replace with actual file name

        # write failed file names to a .txt file
        if failed_files:
            with open('failed_files.txt', 'w') as f:
                for file_name in failed_files:
                    f.write(f"{file_name}\n")

        # fail the test if there are any failed files
        self.assertEqual(failed_files, [], "Some files failed the test. Check 'failed_files.txt' for details.")


if __name__ == '__main__':
    unittest.main()
