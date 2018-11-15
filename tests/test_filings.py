from context import PyEDGAR

import unittest


class TestEdgarFilings(unittest.TestCase):
    """Test the `filings` module.
    """

    def test_getFilingsList(self):
        """Test getting filings index from EDGAR.

        This test case uses the ticker 'AAPL', with corresponding CIK
        '0000320193'. Verifies that over 550 filings are retrieved.
        """

        # Test variables
        candidate_cik = '0000320193'

        # Getting filings
        candidate_filings = PyEDGAR.filings.getAllFilings(cik=candidate_cik)

        # Verifying over 550 filings were retrieved
        self.assertGreater(len(candidate_filings), 550)
