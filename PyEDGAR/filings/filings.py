import logging
import requests

from .downloader import __downloadFilings
from .parser import __parseHTML


def getAllFilings(cik: str) -> list:
    """Function to get a list of SEC filings, given a company CIK.
    
    Arguments:
        cik {str} -- CIK of the target company.
    
    Returns:
        list -- Structured list of dictionaries with filing information for a
                given company. See user guide for more info.
    """

    logging.info('Getting filings from EDGAR for CIK {0}'.format(cik))
    
    # Getting page HTML for filings
    pages_html = __downloadFilings(cik=cik)

    # Parsing HTML
    filings_parsed = __parseHTML(pages_html=pages_html)

    return filings_parsed


def getFilingByType(cik: str, filing_type: str) -> list:
    """Function to get filings by type, for a given company CIK.
    
    Arguments:
        cik {str} -- CIK of target company.
        filing_type {str} -- Target filing type.
    
    Returns:
        list -- Structured list of dictionaries with target filing information.
    """

    # Getting all filings
    filings = getAllFilings(cik=cik)

    # Separating target filings
    target_filings = list()

    for filing in filings:
        if filing_type in filing['type']:
            target_filings += [filing]
    
    return target_filings


def get10K(cik: str) -> list:
    """Function to get 10-K filings for a target company CIK.
    
    Arguments:
        cik {str} -- CIK of target company.
    
    Returns:
        list -- Structured list of dictionaries with 10-K filings.
    """

    return getFilingByType(cik=cik, filing_type='10-K')


def get10Q(cik: str) -> list:
    """Function to get 10-Q filings for a target company CIK.
    
    Arguments:
        cik {str} -- CIK of target company.
    
    Returns:
        list -- Structured list of dictionaries with 10-Q filings.
    """

    return getFilingByType(cik=cik, filing_type='10-Q')
