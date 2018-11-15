from .downloader import __downloadInfoPage
from .parser import __parseHTML

from bs4 import BeautifulSoup
from requests import exceptions, get
import logging


def getInfo(cik: str, includeRaw: bool=False) -> dict:
    """Function to get company information, given a company CIK.
    
    Arguments:
        cik {str} -- CIK of the target company.
    
    Keyword Arguments:
        includeRaw {bool} -- Flag to include raw HTML (default: {False}).
    
    Returns:
        dict -- Dictionary of company infomation. See user guide for more info.
    """

    page_html = __downloadInfoPage(cik=cik)

    # Parsing page HTML
    company_parsed = __parseHTML(page_html=page_html)
    # Reattaching CIK
    company_parsed['cik'] = cik

    # Raw page HTML
    if includeRaw: company_parsed['_raw'] = [page_html]

    return company_parsed
