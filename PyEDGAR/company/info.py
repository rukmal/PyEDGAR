from .downloader import __downloadInfoPage

from bs4 import BeautifulSoup
from requests import exceptions, get
import logging


def getInfo(cik: str) -> dict:
    page_text = __downloadInfoPage(cik=cik)

    test = BeautifulSoup(page_text, features='html.parser')

    return test
