import sys
import json
import re

import re
import json
from json import JSONDecoder
import xml.etree.ElementTree as ET
from xml.dom import minidom
import html

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


# Function to extract and reformat XML data from log entries
def reformat_xml_log(log_entries):
    # Extract XML segments using regular expressions
    pattern = r"<?xml[^>]+?><([^>\s]+)[\s>].*?</\1>"
    # Find all XML matches in the log entries
    xml_matches = re.findall(pattern, log_entries, re.DOTALL)
    for x in xml_matches:
        match = re.search(r"&lt;\?xml.*?\?&gt;", x)
        nx = re.sub(r"&lt;\?xml.*?\?&gt;", "verySpeical", x)
        print(nx)
        xml = ET.fromstring(nx)
        s = ET.tostring(xml,encoding='unicode',xml_declaration = True)
        # xml_bytes = s.encode("utf-8")
        reformatted_xml_bytes = html.unescape(s)
        # reformatted_xml_string = reformatted_xml_bytes.decode("utf-8")  
        # print (reformatted_xml_bytes)
        dom = minidom.parseString(reformatted_xml_bytes)

        # Pretty-print the XML
        pretty_xml = dom.toprettyxml(indent="  ")
        if match:
            substring = match.group()
            substring = substring.replace("&lt;", "<")
            substring = substring.replace("&gt;", ">")
            pretty_xml = pretty_xml.replace("verySpeical", substring)
        else:
            pretty_xml = pretty_xml.replace("verySpeical", '<?xml version="1.0" encoding="UTF-8"?>')

        print(pretty_xml)
        print("--------------")
        out = log_entries.replace(x, "\n"+ pretty_xml)
    print(out)
    return out
def reformat_xml_log_1(log_entries):
    # Extract XML segments using regular expressions
    pattern = r"<\?xml[^>]+?><([^>\s]+)[\s>].*?</\1>"
    # Find all XML matches in the log entries
    matchObj = [match.group() for match in re.finditer(pattern, log_entries)]
    for x in matchObj:    
        match = re.search(r"&lt;\?xml.*?\?&gt;", x)
        if match:
            nx = re.sub(r"&lt;\?xml.*?\?&gt;", "verySpeical", x)
        else:
            nx = x
        print(nx)
        xml = ET.fromstring(nx)
        s = ET.tostring(xml,encoding='unicode',xml_declaration = True)
        # xml_bytes = s.encode("utf-8")
        reformatted_xml_bytes = html.unescape(s)
        # reformatted_xml_string = reformatted_xml_bytes.decode("utf-8")  
        # print (reformatted_xml_bytes)
        dom = minidom.parseString(reformatted_xml_bytes)

        # Pretty-print the XML
        pretty_xml = dom.toprettyxml(indent="  ")
        if match:
            substring = match.group()
            substring = substring.replace("&lt;", "<")
            substring = substring.replace("&gt;", ">")
            pretty_xml = pretty_xml.replace("verySpeical", substring)
        else:
            pretty_xml = pretty_xml.replace("verySpeical", '<?xml version="1.0" encoding="UTF-8"?>')

        print(pretty_xml)
        print("--------------")
        log_entries = log_entries.replace(x, "\n"+ pretty_xml)
    return log_entries

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python log_formatter.py <log_file_path>')
    else:
        log_file_path = sys.argv[1]
        out = extract_nested_json(log_file_path)
        # print(out)

        formatted_text = reformat_xml_log_1(out)
        # print(formatted_text)

        with open(log_file_path, 'w') as log_file:
            log_file.write(formatted_text)

