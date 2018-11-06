from context import PyEDGAR

import unittest

class TestCIKTools(unittest.TestCase):
    """Test the `cik_tools` in the `util` module.
    """

    def test_CIKMatch(self):
        """Test a unique match of the CIK.

        This test uses the ticker 'AAPL', with the expected match returning
        a CIK '0000320193'.
        """

        # Test variables
        candidate_ticker = 'AAPL'
        expected_cik = '0000320193'

        # Getting candidate CIK
        candidate_cik = PyEDGAR.util.getCIK(ticker=candidate_ticker)

        # Asserting equal
        self.assertEqual(candidate_cik, expected_cik)
