import json
import unittest
import xml.etree.ElementTree as ET
import logging
import os
import glob

with open('settings.json', 'r', encoding='utf-8') as settings_file:
    settings = json.load(settings_file)

input_dir = settings['input_directory']
output_dir = settings['output_directory']

# Configure logging to write to a file
logging.basicConfig(filename='log.txt', level=logging.INFO, filemode='w')

cei = "{http://www.monasterium.net/NS/cei}"
tei = "{http://www.tei-c.org/ns/1.0}"
atom = "{http://www.w3.org/2001/XMLSchema-instance}"

# Get list of input and output files
input_files = glob.glob(os.path.join(input_dir, '*'))
output_files = glob.glob(os.path.join(output_dir, '*'))

# Ensure both directories have the same number of files
assert len(input_files) == len(output_files), "Mismatch in number of input and output files."


def create_test(source_file, target_file):
    class TestXMLTransform(unittest.TestCase):
        def setUp(self):
            self.source_file = source_file
            self.target_file = target_file

        def find_elements(self, tree, xpath):
            return [elem for elem in tree.findall(xpath) if elem.text and elem.text.strip()]

        def test_transformed_content(self):
            tag_pairs = [
                (f"{cei}tenor", f"{tei}div[@type='tenor']")
            ]

            source_tree = ET.parse(self.source_file)
            target_tree = ET.parse(self.target_file)

            for source_tags, target_tags in tag_pairs:
                source_elements = self.find_elements(source_tree, f".//{source_tags}")
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

    return TestXMLTransform


suite = unittest.TestSuite()

# Create and add test case for each pair of input and output files
for i in range(len(input_files)):
    test_case = create_test(input_files[i], output_files[i])
    unittest.TestLoader().loadTestsFromTestCase(test_case)

if __name__ == '__main__':
    # Run all the tests in the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)
