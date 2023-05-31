import sys
import json
import re

import re
import json
from json import JSONDecoder
import xml.etree.ElementTree as ET


def extract_nested_json(json_string,decoder=JSONDecoder()):
    with open(log_file_path, 'r') as log_file:
        log_contents = log_file.read()
    pos = 0
    out= log_contents[0:0]
    while True:
        match = log_contents.find('{', pos)
        if match == -1:
            out += log_contents[pos:]
            break
        try:
            result, index = decoder.raw_decode(log_contents[match:])
            obj = json.dumps(result, indent=4)
            out += log_contents[pos:match] + "\n" + obj
            # print(obj)
           
            pos = match + index
        except ValueError:
            pos = match + 1
    return out


# Function to reformat all XML objects in a file with multiple roots
def reformat_all_xml_objects(xml_data):

    # Create an iterator for parsing the XML file incrementally
    context = ET.iterparse(xml_data, events=("start", "end"))

    # Skip the root element of the XML file
    _, root = next(context)

    # Iterate over the remaining elements in the XML tree
    for event, elem in context:
        if event == "end" and elem is not root:
            # Convert the element to a string with proper formatting
            elem_string = ET.tostring(elem, encoding='unicode')
            reformatted_string = elem_string.replace('\n', '').replace('  ', '\t')

            # Replace the original element with the reformatted one
            parent = elem.getparent()
            parent.remove(elem)
            parent.append(ET.fromstring(reformatted_string))

            # Clear the element from memory
            elem.clear()
    out = ET.tostring(root, encoding='unicode')
    print(out)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python log_formatter.py <log_file_path>')
    else:
        log_file_path = sys.argv[1]
        out = extract_nested_json(log_file_path)
        # print(out)

        reformat_all_xml_objects(out)
        # print(formatted_text)

        with open(log_file_path, 'w') as log_file:
            log_file.write(out)

