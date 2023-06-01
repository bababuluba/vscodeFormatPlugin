import sys
import json
import re

import re
import json
from json import JSONDecoder
import xml.etree.ElementTree as ET
from xml.dom import minidom
import html
from xml.sax.saxutils import unescape

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
    pattern = r"<\?xml[^>]+?><([^>\s]+)[\s>].*?</\1>"
    # Find all XML matches in the log entries
    matchObj = [match.group() for match in re.finditer(pattern, log_entries)]
    print(len(matchObj))
    for x in matchObj:
        # x = x.replace('\n', ' ')
        # print(x)
        match = re.search(r"&lt;\?xml.*?\?&gt;", x)
        if match:
            nx = re.sub(r"&lt;\?xml.*?\?&gt;", "verySpeical", x)
        else:
            nx = x
        # print(nx)
        xml = ET.fromstring(nx)
        s = ET.tostring(xml,encoding='unicode',xml_declaration = True)
        # xml_bytes = s.encode("utf-8")
        reformatted_xml_bytes = html.unescape(s)
        # reformatted_xml_string = reformatted_xml_bytes.decode("utf-8")  
        reformatted_xml_bytes = reformatted_xml_bytes.replace('&', '&amp;')
        print (reformatted_xml_bytes)
        dom = minidom.parseString(reformatted_xml_bytes)
        # unescape_xml_elements(dom.documentElement)

        # Pretty-print the XML
        pretty_xml = dom.toprettyxml(indent="  ")
        pretty_xml = html.unescape(pretty_xml)
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
def reformat_xml_log_1(log_entries):
    # Extract XML segments using regular expressions
    pattern = r"<\?xml[^>]+?><([^>\s]+)[\s>].*?</\1>"
    # Find all XML matches in the log entries
    matchObj = [match.group() for match in re.finditer(pattern, log_entries)]
    print(len(matchObj))
    for x in matchObj:
        # x = x.replace('\n', ' ')
        # print(x)
        match = re.search(r"&lt;\?xml.*?\?&gt;", x)
        if match:
            nx = re.sub(r"&lt;\?xml.*?\?&gt;", "verySpeical", x)
        else:
            nx = x
        # print(nx)
        xml = ET.fromstring(nx)
        s = ET.tostring(xml,encoding='unicode',xml_declaration = True)
        # xml_bytes = s.encode("utf-8")
        reformatted_xml_bytes = html.unescape(s)
        # reformatted_xml_string = reformatted_xml_bytes.decode("utf-8")  
        # print (reformatted_xml_bytes)
        dom = minidom.parseString(s)
        # unescape_xml_elements(dom.documentElement)

        # Pretty-print the XML
        pretty_xml = dom.toprettyxml(indent="  ")
        pretty_xml = html.unescape(pretty_xml)
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


# Unescape element names and values
def unescape_xml_elements(element):
    if element.nodeType == element.ELEMENT_NODE:
        element.tagName = unescape(element.tagName)
        if element.firstChild and element.firstChild.nodeType == element.TEXT_NODE:
            # print(unescape(element.firstChild.nodeValue)) 
            # print(element.firstChild.nodeValue) 
            element.firstChild.nodeValue = unescape(element.firstChild.nodeValue)
    for child in element.childNodes:
        unescape_xml_elements(child)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python log_formatter.py <log_file_path>')
    else:
        log_file_path = sys.argv[1]
        out = extract_nested_json(log_file_path)
        # print(out)

        formatted_text = reformat_xml_log(out)
        # print(formatted_text)

        with open(log_file_path, 'w') as log_file:
            log_file.write(formatted_text)

