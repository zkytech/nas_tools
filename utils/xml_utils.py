import xml.etree.ElementTree as ET

def create_xml(rss_data_list,html_title,html_url):
    """

    Args:
        rss_data_list (_type_): [{name:"",url:""}]
    """
    ET.Element("rss")
    rss = ET.Element("rss")
    rss.set("version","2.0")
    channel = ET.SubElement(rss,"channel")
    title = ET.SubElement(channel,"title")
    title.text = html_title
    link = ET.SubElement(channel,"link")
    link.text = html_url
    for rss_data in rss_data_list:
        item = ET.SubElement(channel,"item")
        title = ET.SubElement(item,"title")
        title.text = rss_data["name"]
        link = ET.SubElement(item,"link")
        link.text = rss_data["url"]
    return rss

def xml_to_str(xml):
    return ET.tostring(xml,encoding="utf-8",method="xml").decode("utf-8")


