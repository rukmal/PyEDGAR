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
        test_cik = '0000320193'

        # Getting company info
        info = PyEDGAR.company.getInfo(cik=test_cik)

        # Expected result
        expected_types = ['Mailing Address', 'Business Address']
        # Candidate result
        candidate_types = [i['type'] for i in info['addresses']]

        # Check equality
        self.assertTrue(sorted(expected_types) == sorted(candidate_types))


    def test_companyPhone(self):
        """Test the company module address retrieval from `getInfo` in the
        `company` module.

        Test case uses ticker 'TSLA', with the corresponding CIK
        '0001318605'. Verifies that the Business address contains the phone
        number '6506815000'.
        """

        # Test variables
        test_cik = '0001318605'

        # Getting company info
        info = PyEDGAR.company.getInfo(cik=test_cik)

        # Expected result
        expected_phone = '6506815000'

        # Getting candidate result
        candidate_phone = ''
        for address in info['addresses']:
            if address['type'] == 'Business Address':
                candidate_phone = address['phone']
                break
        
        # Check numbers match
        self.assertEqual(candidate_phone, expected_phone)
