from bs4 import BeautifulSoup
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

    return company_info

def __getAddresses(parsed: BeautifulSoup) -> list:
    """Function to extract company addresses from the parsed HTML EDGAR page.
    
    Arguments:
        parsed {BeautifulSoup} -- Parsed HTML from company EDGAR filing.
    
    Returns:
        list -- List of addresses.
    """

    address_divs = parsed.find_all('div', class_='mailer')

    # Building RegEx for phone number
    phone_number_regex = re.compile(
        r'(\(\d{3}\) \d{3}-\d{4}|\d{3}-\d{3}-\d{4})')

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
