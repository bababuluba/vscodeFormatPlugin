import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
import html
# Function to extract and reformat XML data from log entries
def reformat_xml_log(log_entries):
    # Extract XML segments using regular expressions
    pattern = r"<\?xml.*?>\n"
    # Find all XML matches in the log entries
    xml_matches = re.findall(pattern, log_entries, re.DOTALL)
    for x in xml_matches:
        match = re.search(r"&lt;\?xml.*?\?&gt;", x)
        nx = re.sub(r"&lt;\?xml.*?\?&gt;", "verySpeical", x)
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
        print(x)
        log_entries = log_entries.replace(x, "\n"+ pretty_xml)
    print(log_entries)
# Sample log entries
log_entries = '''
2023-05-29 15:11:30.913 invenco-apc local1.debug iNFX-conexxuseps[887]: #1580) ClientManager::SendRequestImpl 192.168.3.200:33292 is sending 319 bytes to 192.168.3.3:4004 #012<?xml version="1.0" encoding="utf-8"?><something Req="POSConfigUpdate" ><CurrentTime>2023-03-24T04:38:17.414</CurrentTime></something>
2023-05-29 15:11:30.824 invenco-apc local1.info iNFX-conexxuseps[887]: #1575)<?xml version="1.0" encoding="UTF-8"?><ServiceRequest  IFSFVersion="3.0" WorkstationID="P00" POPID="00" RequestID="82" POSAddress="102"><POSDa Clerkel="5"><POSStamp>202206T13:16:43.917</POSStamp><POSName>PPRT</POSName><POSVersion>1 </POSVersion><ContactICCCapable>false</ContactICCCapable><ContactlessICCCapable>false</ContactlessICCCapable><BarcodeCapable>true</BarcodeCapable></POSDa><Admin AdminReq="EPSConfigUpdate"><AdminData>&lt;?xml version="1.0" encoding="UTF-8" standalone="yes"?&gt;&lt;ns1:ConfigUpdate xmlns:xsi ="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns1 ="http://MLSchema" &gt;&lt;EPSConfigUpdate&gt;&lt;SecondaryLoyaltySupport&gt;true&lt;/SecondaryLoyaltySupport&gt;&lt;SecondaryPaymentSupport&gt;true&lt;/SecondaryPaymentSupport&gt;&lt;MinimumFuelPrice&gt;0&lt;/MinimumFuelPrice&gt;&lt;IndoorBarcodeScannerAvailable&gt;true&lt;/IndoorBarcodeScannerAvailable&gt;&lt;WidePrinterForReportsAvailable&gt;true&lt;/WidePrinterForReportsAvailable&gt;&lt;MerchantName&gt;PASSPORT TERM #603&lt;/MerchantName&gt;&lt;PrinterRequestMaxLength&gt;2000&lt;/PrinterRequestMaxLength&gt;&lt;/EPSConfigUpdate&gt;&lt;/ns1:ConfigUpdate&gt;</AdminData></Admin><CurrentTime>2022-10-06T13:16:43.917</CurrentTime></ServiceRequest>
'''

# Extract and reformat XML data from log entries
reformat_xml_log(log_entries)
