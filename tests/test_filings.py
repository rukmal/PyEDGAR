from context import PyEDGAR

import unittest


class TestEdgarFilings(unittest.TestCase):
    """Test the `filings` in the `edgar` module.
    """

    def test_getFilingsIndex(self):
        """Test getting filings index from EDGAR.

        This test uses the ticker 'AAPL'.
        """

        # Test variables
        candidate_ticker = 'AAPL'
        candidate_cik = PyEDGAR.util.getCIK(ticker=candidate_ticker)

        # Getting filings (temporary)
        PyEDGAR.filings.getAllFilings(cik=candidate_cik)
