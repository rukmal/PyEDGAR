import logging
import requests

from .downloader import __downloadFilings
from .parser import __parseHTML


def getAllFilings(cik: str, includeRaw: bool=False) -> list:
    """Function to get a list of SEC filings, given a company CIK.
    
    Arguments:
        cik {str} -- CIK of the target company.
    
    Keyword Arguments:
        includeRaw {bool} -- Flag to include raw HTML (default: {False}).
    
    Returns:
        list -- Structured list of dictionaries with filing information for a
                given company. See user guide for more info.
    """

    logging.info('Getting filings from EDGAR for CIK {0}'.format(cik))
    
    # Getting page HTML for filings
    pages_html = __downloadFilings(cik=cik)

    # Parsing HTML
    filings_parsed = __parseHTML(pages_html=pages_html)

    # Raw page HTML
    if includeRaw: filings_parsed['_raw'] = pages_html

    return filings_parsed
