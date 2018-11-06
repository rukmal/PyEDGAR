import logging
import re
import requests


def getCIK(ticker: str) -> str:
    """Function to get the Central Index Key (CIK) for a given ticker by
    querying the SEC EDGAR API.
    
    Arguments:
        ticker {str} -- Ticker to be matched.
    
    Raises:
        requests.exceptions.RequestException -- Thrown if the request fails.
        LookupError -- Thrown if a CIK match is not found, or if there is more
                       than one CIK corresponding to the candidate ticker.
    
    Returns:
        str -- Corresponding CIK of the ticker.
    """

    # Base URL for request
    base_url = 'http://www.sec.gov/cgi-bin/browse-edgar'

    # Building parameters for request with ticker
    # Note: Order of parameters here is important
    params = {
        'CIK': ticker,
        'Find': 'Search',
        'owner': 'exclude',
        'action': 'getcompany'
    }

    # Making request
    r = requests.get(url=base_url, params=params)

    # Handling failed request
    if not r.ok:
        logging.warn('Request failed: CIK lookup for ticker {0} with error {1}'
            .format(ticker, r.status_code))
        raise requests.exceptions.RequestException('Request failed')

    # RegEx for extracting ticker from response
    # Note: Solution adapted from:
    #           1. https://gist.github.com/ddd1600/3934032
    #           2. https://gist.github.com/dougvk/8499335
    ticker_regex = re.compile(r'.*CIK=(\d{10}).*')

    # Matching RegEx
    matches = ticker_regex.findall(string=r.text)

    # Checking if the CIK exists, and is unique
    matches_set_len = len(set(matches))

    if matches_set_len > 1:
        logging.warn('Unique CIK match not found for ticker {0}'.format(ticker))
        raise LookupError('Unique CIK match not found')
    elif matches_set_len == 0:
        logging.warn('No CIK match found for ticker {0}'.format(ticker))
        raise LookupError('CIK match not found')

    # No errors, return CIK
    return matches[0]
