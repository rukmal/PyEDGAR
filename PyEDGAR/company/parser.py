from bs4 import BeautifulSoup
import html
import logging
import re


def __parseHTML(page_html: str) -> dict:
    """Function to parse EDGAR page HTML, returning a dict of company info.
    
    Arguments:
        page_html {str} -- Raw HTML of page.
    
    Returns:
        dict -- Structured dictionary of company attributes.
    """

    # Dict for final output
    company_info = dict()

    # Parsing HTML
    parsed = BeautifulSoup(page_html, features='html.parser')

    # Getting company addresses
    company_info['addresses'] = __getAddresses(parsed=parsed)
    # Getting company name
    company_info['name'] = __getCompanyName(parsed=parsed)
    # Getting former company names
    company_info['former_names'] = __getFormerNames(parsed=parsed)
    # Getting company metadata
    company_info['metadata'] = __getCompanyMetadata(parsed=parsed)

    return company_info

def __getAddresses(parsed: BeautifulSoup) -> list:
    """Function to extract company addresses from the parsed HTML EDGAR page.
    Searches for address information in divs with class name 'mailer'.
    
    Arguments:
        parsed {BeautifulSoup} -- Parsed HTML from company EDGAR filing.
    
    Returns:
        list -- List of addresses.
    """

    # Addresses container
    address_divs = parsed.find_all('div', class_='mailer')

    # Building RegEx for phone number
    # The following RegEx extracts phone numbers in the following formats:
    #   1. (###) ###-####
    #   2. ###-###-####
    #   3. ##########
    phone_number_regex = re.compile(
        r'(\(\d{3}\) \d{3}-\d{4}|\d{3}-\d{3}-\d{4}|\d{10})')

    # List for final addresses
    addresses = list()

    for address in address_divs:
        # Create dict for address
        address_parsed = dict()
        # Split text by newline
        address_items = address.text.split('\n')
        # Removing leading and trailing spaces
        address_items = [i.strip() for i in address_items]

        # Variable to store street address
        street_address = ''

        # Iterate through each line
        for idx, address_item in enumerate(address_items):
            # First line is address type
            if idx == 0:
                address_parsed['type'] = address_item
                continue

            # Check if line has phone number
            phone_matches = phone_number_regex.findall(address_item)
            if len(phone_matches) == 1:
                # Stripping non-digit characters from phone number
                phone_number = re.sub('[^0-9]', '', phone_matches[0])
                address_parsed['phone'] = phone_number
                continue
            
            # If no number, add to address line
            street_address += address_item.strip() + ' '
    
        # Adding street address to parsed address
        address_parsed['street_address'] = street_address.strip()

        # Adding parsed address to addresses master list
        addresses += [address_parsed]

    return addresses


def __getCompanyName(parsed: BeautifulSoup) -> str:
    """Function to extract the company name from the parsed HTML EDGAR page.
    Searches for company name in a span with class 'companyName'.
    
    Arguments:
        parsed {BeautifulSoup} -- Parsed HTML from company EDGAR filing.
    
    Returns:
        str -- Name of company.
    """

    # Company name container
    name_container = parsed.find('span', class_='companyName')

    # Extracting raw text elements
    name_raw_text = [s for s in name_container.children if isinstance(s, str)]

    # Getting name (first raw text instance)
    return name_raw_text[0].strip()


def __getFormerNames(parsed: BeautifulSoup) -> list:
    """Function to extract former company names, and dates through which reports
    were filed under that name from the parsed HTML EDGAR page.
    Searches for strings matching format for previous names first, then extracts
    former name and filings-through date separately.
    
    Arguments:
        parsed {BeautifulSoup} -- Parsed HTML from company EDGAR filing.
    
    Returns:
        list -- List of former names (if any), empty list otherwise.
    """

    # Former names container
    former_container = parsed.find('p', class_='identInfo')

    # List for former names
    former_names = list()

    # Building RegEx for former name sentence
    former_sentence_re = re.compile(r'(formerly:.+?\(filings through .+?\))')
    # Getting sentence matches
    former_sentences = former_sentence_re.findall(former_container.text)
    
    # Building RegEx for name and filings-through date extraction
    name_and_date_re = re.compile(r'formerly:(.*)\(.*(\d{4}-\d{2}-\d{2})')
    # Extracting former name and filings-through date for each sentence
    for sentence in former_sentences:
        matches = name_and_date_re.findall(sentence)
        former_name = dict()
        former_name['former_name'] = matches[0][0].strip()
        former_name['filings_through'] = matches[0][1]
        former_names += [former_name]

    return former_names


def __getCompanyMetadata(parsed: BeautifulSoup) -> dict:
    """Function to extract company Standard Industrial Classification (SIC)
    code, SIC type (i.e. description), company location, state of incorporation,
    and the end of its fiscal year.
    Searches the raw HTML of the company identification section of the page
    using regular expressions.
    
    Arguments:
        parsed {BeautifulSoup} -- Parsed HTML from company EDGAR filing.
    
    Returns:
        dict -- Company metadata with keys `sic`, `sic_type`, `location`,
                `incorporation_state`, and `fiscal_year_end`.
    """

    # Company metadata container
    metadata_container = parsed.find('p', class_='identInfo')
    # String representation of HTML (used in RegEx)
    metadata_str = str(metadata_container)

    # Dictionary for company metadata
    company_metadata = dict()

    # RegEx for extracting SIC and SIC type
    sic_re = re.compile(r'SIC.+?:.+?(\d+?)<\/a> -(.+?)<br')
    # Getting SIC and SIC type match
    sic_matches = sic_re.findall(metadata_str)
    # Saving SIC and stripped, HTML-parsed SIC type
    company_metadata['sic'] = sic_matches[0][0]
    company_metadata['sic_type'] = html.unescape(sic_matches[0][1]).strip()

    # RegEx for extracting company location (state)
    location_re = re.compile(r'State location:.+?>(\w+?)<\/a>')
    # Getting company location
    location_matches = location_re.findall(metadata_str)
    # Saving company location
    company_metadata['location'] = location_matches[0].strip()

    # RegEx for extracting state of incorporation
    incorp_state_re = re.compile(r'State of Inc\.:.+?>(\w+?)<\/strong>')
    # Getting state of incorporation
    incorp_match = incorp_state_re.findall(metadata_str)[0]
    # Saving state of incorporation
    company_metadata['incorporation_state'] = incorp_match.strip()

    # RegEx for extracting end of fiscal year
    fiscal_year_re = re.compile(r'Fiscal Year End:.+?(\d{4})')
    # Getting end of fiscal year
    fiscal_year_match = fiscal_year_re.findall(metadata_str)[0]
    # Saving end of fiscal year (in mm-dd format)
    fy_formatted = fiscal_year_match[0:2] + '-' + fiscal_year_match[2:]
    company_metadata['fiscal_year_end'] = fy_formatted

    return company_metadata
