from context import PyEDGAR

import unittest

class TestEdgarCompany(unittest.TestCase):

    def test_companyAddress(self):
        """Test company address retrieval from `getInfo` in the
        `company` module.
        
        Test case uses ticker 'AAPL', with corresponding CIK
        '0000320193'. Verifies that the address contains both a 'Business'
        and a 'Mailing' address.
        """

        # Test variables
        candidate_ticker = 'AAPL'
        candidate_cik = PyEDGAR.util.getCIK(ticker=candidate_ticker)

        # Getting company info
        info = PyEDGAR.company.getInfo(cik=candidate_cik)

        # Expected results
        expected_types = ['Mailing Address', 'Business Address']
        candidate_types = [i['type'] for i in info['addresses']]

        self.assertTrue(sorted(expected_types) == sorted(candidate_types))
