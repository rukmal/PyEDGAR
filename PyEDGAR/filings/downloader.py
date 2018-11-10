from requests import exceptions, get
import logging


def edgarDownload(cik: str) -> list:
    """Function to download the XML text of listings pages for a given CIK
    from the EDGAR database.
    
    Arguments:
        cik {str} -- Target CIK.
    
    Returns:
        list -- List of page XML, comprising full listing metadata for CIK.
    """

    idx = 0  # Current page index
    end = False  # Flags for loop
    count = 100  # Number of results per page (limited by SEC)

    # Text indicating next page exists
    next_page_text = 'rel="next" type="application/atom+xml" />'

    pages = []

    while not end:
        # Making request
        page_text = __makeRequest(cik=cik, start_idx=idx, count=count)
        end = (page_text.find(next_page_text) == -1)  # Update end flag
        idx += count  # Increment index for next page
        pages.append(page_text)  # Save page text

    return pages

def __makeRequest(cik: str, start_idx: int, count: int, retry: bool=False) \
    -> str:
    """Function to make a request to the EDGAR system to retrieve XML with
    listings for a given CIK.
    
    Arguments:
        cik {str} -- Target CIK.
        start_idx {int} -- Start index (for pagination).
        count {int} -- Count of results per page.
    
    Keyword Arguments:
        retry {bool} -- Flag for auto-retry (default: {False}).
    
    Raises:
        exceptions.RetryError -- Raised if the request retry fails.
    
    Returns:
        str -- Page text with XML listing metadata for the target CIK.
    """

    
    base_url = 'https://sec.gov/cgi-bin/browse-edgar'

    # Building parameters for request wit hticker
    # Note: Order of parameters here is important; null params are
    #       necessary cuz the SEC is silly
    params = {
        'action': 'getcompany',
        'CIK': cik,
        'type': '',
        'dateb': '',
        'owner': 'exclude',
        'start': start_idx,
        'count': count,
        'output': 'atom'
    }

    # Making request
    r = get(url=base_url, params=params)

    # Retry request if it fails; raise Exception if it still doesn't work
    if (not r.ok) and (not retry):
        logging.warn('Listings request failed for CIK {0}. Trying again...'
                     .format(cik))
        return __makeRequest(cik=cik, start_idx=start_idx, count=count,
                             retry=True)
    elif not r.ok:
        logging.error('Listings request failed for CIK {0}'.format(cik))
        raise exceptions.RetryError('Listings request retry failed for CIK {0}'
                                    .format(cik))

    return r.text
