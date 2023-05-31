import re
from lxml import etree

def extract_xml_data(string):
 pattern = r'<\?xml[^>]+\?>\s*((?:<!.*?>\s*)*<[^>]+>.*?)(?:<\/[^>]+>)?'
 matches = re.findall(pattern, string, re.DOTALL)
 xml_data = []

 for match in matches:
    try:
        root = etree.fromstring(match)
        xml_data.append(root)
    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML: {e}")

 return xml_data

string = '''sdfsdfsdfsd sdfsdf<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:xsd="http:LSchema" xmlns:xsi="http://www.w3." xmlns:s="http://schemas.xmlsoape/">
 <s:Body>
 <s:Element1>foo</s:Element1>
 <s:Element2>bar</s:Element2>
 <s:Element3>baz</s:Element3>
 </s:Body>
</s:Envelope>!sdfsd # Use ! as a delimiter instead of #

earthjkds<?xml version="1.0" encoding="utf-8"?>
<bookstore xmlns:bk="http://example.com/books">
 <book id="b1" bk:genre="fiction">
 <title>Harry Potter and the Philosopher's Stone</title>
 <author>J.K. Rowling</author>
 <price>12.99</price>
 </book>
 <book id="b2" bk:genre="non-fiction">
 <title>A Brief History of Time</title>
 <author>Stephen Hawking</author>
 <price>15.99</price>
 </book>
</bookstore>!1dfsdasdf # Close the bookstore tag correctly

asdfkjhasdkjgh<?xml version="1.0" encoding="utf-8"?>
<!-- This is a comment -->
<catalog>
 <?xml-stylesheet type="text/css" href="style.css"?>
 <product id="p1">
 <name>iPhone 14</name>
 <description><![CDATA[The latest smartphone from Apple]]></description>
 <price currency="USD">999.99</price>
 </product>
 <product id="p2">
 <name>Samsung Galaxy S22</name>
 <description><![CDATA[The latest smartphone from Samsung]]></description>
 <price currency="USD">899.99</price>
 </product>
</catalog>''' # Close the catalog tag correctly

xml_data = extract_xml_data(string)

# Example: Printing the tag names of the root elements of each XML block
for data in xml_data:
 print(data.tag)
