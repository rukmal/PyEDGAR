from bs4 import BeautifulSoup
import html
import logging


def __parseHTML(pages_html: list) -> list:
    """Function to parse raw HTML filings from EDGAR, and return a structured
    list of dictionaries with filing information.
    
    Arguments:
        pages_html {list} -- Raw HTML of listings pages.
    
    Returns:
        list -- Structured list of dictionaries of filing information.
    """

    filings = list()

    for page in pages_html:
        # Parsing page with BeautifulSoup
        page_parsed = BeautifulSoup(page, features='html.parser')
        # Getting filings for each page
        page_filings = __parsePageFilings(page_parsed=page_parsed)
        # Adding page filing to list
        filings += page_filings
    
    return filings


def __parsePageFilings(page_parsed: BeautifulSoup) -> list:
    """Function to extract filings from a parsed HTML EDGAR listings page.
    
    Arguments:
        page_parsed {BeautifulSoup} -- Parsed HTML for filing extraction.
    
    Returns:
        list -- Structured list of dictionaries of filing information.
    """

    # Getting list of filings
    filings = page_parsed.find_all('entry')

    # Filing information container
    filings_parsed = list()

    # Required fields and corresponding XML tag (misspelling is intentional)
    required_fields = {'accession-number': 'accession-nunber',
                       'type': 'filing-type',
                       'url': 'filing-href',
                       'date': 'filing-date'}
    # Optional fields and corresponding XML tag
    optional_fields = {'act': 'act',
                       'file_number': 'file-number',
                       'file_number_url': 'file-number-href',
                       'film_number': 'film-number',
                       'name': 'form-name',
                       'description': 'items-desc',
                       'size': 'size'}

    # Iterating through each filing, extracting information
    for filing in filings:
        f_parsed = dict()
        # Getting all required fields
        for k, v in required_fields.items():
            f_parsed[k] = filing.find(v).text
        # Getting optional fields (empty string if not available)
        for k, v in optional_fields.items():
            try:
                f_parsed[k] = filing.find(v).text
            except:
                f_parsed[k] = ''
    
        # Adding to list of filings
        filings_parsed += [f_parsed]

    return filings_parsed
