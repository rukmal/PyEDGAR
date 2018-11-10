import logging
import requests

from .downloader import edgarDownload


def getAllFilings(cik: str) -> object:

    logging.debug('Getting filings from EDGAR for CIK {0}'.format(cik))
    edgarDownload(cik=cik)
