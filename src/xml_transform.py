import os
import glob
import lxml.etree as etree
from multiprocessing import Pool

def transform_xml_file(input_file, output_dir, xslt):
    # Load the input XML
    input_xml = etree.parse(input_file)

    # Create the XSLT transformer
    transformer = etree.XSLT(xslt)

    # Apply the transformation
    output_xml = transformer(input_xml)

    # Get the output file path
    output_file = os.path.join(output_dir, os.path.basename(input_file))

    # Save the transformed XML to the output file
    with open(output_file, 'wb') as f:
        f.write(etree.tostring(output_xml, pretty_print=True))

    print(f"Transformed '{input_file}' -> '{output_file}'")

def transform_xml_files(input_dir, output_dir, xslt_file, num_processes=4):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get a list of all XML files in the input directory
    input_files = glob.glob(os.path.join(input_dir, '*.xml'))

    # Load the XSLT stylesheet
    xslt = etree.parse(xslt_file)

    # Create a process pool
    pool = Pool(num_processes)

    # Apply transformation to each file using multiple processes
    pool.starmap(transform_xml_file, [(file, output_dir, xslt) for file in input_files])

    # Close the process pool
    pool.close()
    pool.join()

# Example usage
input_directory = '/path/to/input/files'
output_directory = '/path/to/output/files'
xslt_stylesheet = '/path/to/stylesheet.xsl'
num_processes = 4

transform_xml_files(input_directory, output_directory, xslt_stylesheet, num_processes)