from requests import exceptions, get
import logging

def __downloadInfoPage(cik: str) -> str:
    """Function to download listings page from EDGAR, given a target CIK.
    
    Arguments:
        cik {str} -- CIK of target company.
    
    Raises:
        exceptions.RequestException -- Raised if page load fails.
    
    Returns:
        str -- Page HTML.
    """

    base_url = 'https://sec.gov/cgi-bin/browse-edgar'

    # Building request parameters
    # Note: Order of parameters here is important
    params = {
        'CIK': cik,
        'owner': 'exclude',
        'action': 'getcompany'
    }

    # Making request
    r = get(url=base_url, params=params)

    # Handling failed request
    if not r.ok:
        logging.warn('Request failed: Information lookup for CIK {0}, error {1}'
            .format(cik, r.status_code))
        raise exceptions.RequestException('Request Failed')

    return r.text
