"""
Transform XML files utilizing multithreading
"""
import os
import json
from multiprocessing import Pool
from lxml import etree

with open('settings.json', 'r', encoding='utf-8') as settings_file:
    settings = json.load(settings_file)

input_path = settings['input_directory']
output_path = settings['output_directory']
style_path = settings['xslt_stylesheet']


def transform_xml_file(input_file, output_dir, xslt_bytes):
    """
    transforms XML file using a provided XSLT stylesheet
    :param input_file:
    :param output_dir:
    :param xslt_bytes:
    :return:
    """
    # Parse the XSLT stylesheet
    xslt = etree.fromstring(xslt_bytes)

    # Load the input XML
    input_xml = etree.parse(input_file)

    # Create the XSLT transformer
    transformer = etree.XSLT(xslt)

    # Apply the transformation
    output_xml = transformer(input_xml)

    # Make sure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get the output file path
    output_file = os.path.join(output_dir, os.path.basename(input_file))

    # Save the transformed XML to the output file
    with open(output_file, 'wb') as file:
        file.write(etree.tostring(output_xml, pretty_print=True))

    print(f"Transformed '{input_file}' -> '{output_file}'")


def transform_xml_files(input_dir, output_dir, xslt_file, num_processes=4):
    """
    split files into pools
    :param input_dir:
    :param output_dir:
    :param xslt_file:
    :param num_processes:
    :return:
    """
    # Read the XSLT file into bytes
    with open(xslt_file, 'rb') as file:
        xslt_bytes = file.read()

    # Create a process pool
    pool = Pool(num_processes)

    # List to hold the AsyncResult objects
    results = []

    # Walk through input directory recursively
    for root, dirs, files in os.walk(input_dir):
        xml_files = [file for file in files if file.endswith('.xml')]
        for file in xml_files:
            input_file = os.path.join(root, file)

            # Maintain the same directory structure in the output directory
            relative_path = os.path.relpath(root, input_dir)
            output_subdir = os.path.join(output_dir, relative_path)

            # Apply transformation to each file using multiple processes
            result = pool.apply_async(transform_xml_file, args=(input_file,
                                                                output_subdir, xslt_bytes))

            # Append the result to the results list
            results.append(result)

    # Close the process pool
    pool.close()

    # Call get() on each result to wait for the transformations to complete
    for result in results:
        result.get()

    # Wait for all processes to finish
    pool.join()


def main():
    """
    set paths and number of process for transformation
    :return:
    """
    # Example usage
    input_directory = input_path
    output_directory = output_path
    xslt_stylesheet = style_path
    num_processes = 4

    transform_xml_files(input_directory, output_directory, xslt_stylesheet, num_processes)

if __name__ == '__main__':
    main()
