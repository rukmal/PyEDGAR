from context import PyEDGAR

import unittest

class TestEdgarCompany(unittest.TestCase):
    """Test the `company` module.
    """


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
        """Test the phone (in address) retrieval from `getInfo` in the
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


    def test_companyName(self):
        """Test company name retrieval system from `getInfo` in the
        `company` module.

        Test case uses ticker 'GE', with the corresponding CIK '0000040545'.
        Verifies that the company name is 'GENERAL ELECTRIC CO'.
        """

        # Test variables
        test_cik = '0000040545'

        # Getting company info
        info = PyEDGAR.company.getInfo(cik=test_cik)

        # Expected result
        expected_name = 'GENERAL ELECTRIC CO'
        # Candidate result
        candidate_name = info['name']

        # Check for equality
        self.assertEqual(candidate_name, expected_name)


    def test_formerCompanyName(self):
        """Test the former name retrieval from `getInfo` in the
        `company` module.

        Test case uses ticker 'XOM', with the corresponding CIK '0000034088'.
        Verifies that the former company name is 'EXXON CORP' with filings
        through date of '1991-11-30'.
        """

        # Test variables
        test_cik = '0000034088'

        # Getting company info
        info = PyEDGAR.company.getInfo(cik=test_cik)

        # Expected result
        expected_former = {'former_name': 'EXXON CORP',
                           'filings_through': '1999-11-30'}
        # Candidate result
        candidate_former = info['former_names'][0]

        # Building equivalence check
        check_equal = [candidate_former[i] == expected_former[i]
                       for i in expected_former.keys()]

        # Check for equality
        self.assertTrue(all(check_equal))


    def test_companyMetadata(self):
        """Test the company metadata retrieval from `getInfo` in the
        `company` module.

        Test case uses ticker 'AMZN', with the corresponding CIK '0001018724'.
        Verifies that the sic is '5961', sic_type is 'RETAIL-CATALOG &
        MAIL-ORDER HOUSES', location is 'WA', incorporation_state is 'DE',
        and fiscal_year_end is '12-31'.
        """

        # Test variables
        test_cik = '0001018724'

        # Getting company info
        info = PyEDGAR.company.getInfo(cik=test_cik)

        # Expected result
        expected_metadata = {'sic': '5961',
                             'sic_type': 'RETAIL-CATALOG & MAIL-ORDER HOUSES',
                             'location': 'WA',
                             'incorporation_state': 'DE',
                             'fiscal_year_end': '12-31'}
        # Candidate result
        candidate_metadata = info['metadata']

        # Checking equality
        check_equal = [candidate_metadata[i] == expected_metadata[i]
                        for i in expected_metadata.keys()]

        # Check for equality
        self.assertTrue(all(check_equal))
