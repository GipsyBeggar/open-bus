import os
import urllib.request
import pytz
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from http.client import IncompleteRead

REQUEST_TEMPLATE_FILE = "request.template.xml"
templates_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
REQUEST_TEMPLATE = Environment(loader=FileSystemLoader(templates_folder)).get_template(REQUEST_TEMPLATE_FILE)
HEADERS = {'Content-Type': 'text/xml; charset=utf-8'}
SIRI_SERVICES_URL = 'http://siri.motrealtime.co.il:8081/Siri/SiriServices'


def get_arrivals_response_xml(request_xml, use_proxy=False, proxy_url=None):
    """
    Args:
        request_xml - Siri request XML (String)
    Returns:
        Siri response XML (String)
    """
    try:
        print("Running get_arrivals_response_xml %s proxy" % ("with" if use_proxy else "without"))
        proxy = urllib.request.ProxyHandler({'http': proxy_url})
        if use_proxy:
            opener = urllib.request.build_opener(proxy)
            urllib.request.install_opener(opener)
        req = urllib.request.Request(SIRI_SERVICES_URL, headers=HEADERS, data=request_xml.encode('utf8'))
        res = urllib.request.urlopen(req).read()
        return res.decode('utf-8')
    except IncompleteRead as e:
        print("http.client.IncompleteRead happened on sending SIRI request:", e)
        return e.partial


def get_arrivals_request_xml(stops, siri_user):
    """
    Args:
        stops - List of stop IDs
    Returns:
        Siri request XML (String)
    """
    timestamp = datetime.now(pytz.timezone("Israel")).isoformat()
    request_xml = REQUEST_TEMPLATE.render(stops=stops, timestamp=timestamp, siri_user=siri_user)
    return request_xml
