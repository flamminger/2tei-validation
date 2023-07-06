import json
import unittest
import xml.etree.ElementTree as ET
import logging
import os
import glob

with open('transform_settings.json', 'r', encoding='utf-8') as settings_file:
    settings = json.load(settings_file)

input_dir = settings['input_directory']
output_dir = settings['output_directory']

# Configure logging to write to a file
logging.basicConfig(filename='log.txt', level=logging.INFO, filemode='w')

cei = "{http://www.monasterium.net/NS/cei}"
tei = "{http://www.tei-c.org/ns/1.0}"
atom = "{http://www.w3.org/2001/XMLSchema-instance}"

# Get list of input and output files
input_files = glob.glob(os.path.join(input_dir, '**', '*.xml'), recursive=True)
output_files = glob.glob(os.path.join(output_dir, '**', '*.xml'), recursive=True)

# Ensure both directories have the same number of files
assert len(input_files) == len(output_files), "Mismatch in number of input and output files."

def gather_text(node):
    """Recursive function to get text from current and all child nodes"""
    text = node.text or ''
    for child in node:
        text += gather_text(child)
    return text

def jaccard_similarity(set1, set2):
    """
    Calculate Jaccard similarity between two sets
    :param set1: set 1
    :param set2: set 2
    :return: Jaccard similarity value
    """
    intersection = len(set(set1).intersection(set(set2)))
    union = (len(set(set1)) + len(set(set2))) - intersection
    return float(intersection) / union if union != 0 else 1.0

def create_test(source_file, target_file):
    class TestXMLTransform(unittest.TestCase):
        def setUp(self):
            self.source_file = source_file
            self.target_file = target_file

        def find_elements(self, tree, xpath):
            return [elem for elem in tree.findall(xpath)]

        def test_transformed_content(self):
            tag_pairs = [
                (f"{cei}tenor", f"{tei}div[@type='tenor']")
            ]

            source_tree = ET.parse(self.source_file)
            target_tree = ET.parse(self.target_file)

            for source_tags, target_tags in tag_pairs:
                source_elements = self.find_elements(source_tree, f".//{source_tags}")
                target_elements = self.find_elements(target_tree, f".//{target_tags}")

                source_texts = [set(gather_text(source_elem).split()) for source_elem in source_elements]
                target_texts = [set(gather_text(target_elem).split()) for target_elem in target_elements]

                # Calculate Jaccard similarity for each pair of source and target texts
                for source_text, target_text in zip(source_texts, target_texts):
                    similarity = jaccard_similarity(source_text, target_text)

                    logging.info(f"Jaccard similarity for {source_tags} and {target_tags}: {similarity}")
                    self.assertGreater(similarity, 0.9,
                                       f"Low similarity between source tags {source_tags} and target tags {target_tags}")

    return TestXMLTransform

# Create a test suite
suite = unittest.TestSuite()

# Create and add test case for each pair of input and output files
for i in range(len(input_files)):
    test_case = create_test(input_files[i], output_files[i])
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_case))


if __name__ == '__main__':
    # Run all the tests in the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)
