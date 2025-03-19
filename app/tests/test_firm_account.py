import unittest
from unittest.mock import patch
from parameterized import parameterized

from ..FirmAccount import FirmAccount

class TestFirmAccount(unittest.TestCase):
    @parameterized.expand([
        (
            "valid_firm_account",
            "Whata", "Hell", "61113856390", "MegaLLODON", "66903138115",
            "Whata", "Hell", "61113856390", "MegaLLODON", "66903138115"
        ),
        (
            "invalid_nip_firm_account",
            "Whata", "Hell", "61113856390", "MegaLLODON", "669138115",
            "Whata", "Hell", "61113856390", "MegaLLODON", "Niepoprawny NIP!"
        ),
    ])
    def test_firm_account_creating(self, _, name, surname, pesel, firm_name, nip,
                                   exp_name, exp_surname, exp_pesel, exp_firm_name, exp_nip):
        firm_account = FirmAccount(name, surname, pesel, firm_name, nip)
        self.assertEqual(firm_account.name, exp_name, "Name is not filled in correctly!")
        self.assertEqual(firm_account.surname, exp_surname, "Surname is not filled in correctly!")
        self.assertEqual(firm_account.pesel, exp_pesel, "Pesel is not filled in correctly!")
        self.assertEqual(firm_account.firm_name, exp_firm_name, "Firm name is not filled in correctly!")
        self.assertEqual(firm_account.nip, exp_nip, "NIP validation is incorrect!")

    @parameterized.expand([
        ("invalid_nip_length", "Whata", "Hell", "12345678903", "MegaLLODON", "1234567")
    ])
    def test_firm_account_nip_wrong_length(self, condition, name, surname, pesel, firm_name, nip):
        with patch('app.FirmAccount.requests.get') as mock_get:
            firm_account = FirmAccount(name, surname, pesel, firm_name, nip)
            mock_get.assert_not_called()
            self.assertEqual(firm_account.nip, "Niepoprawny NIP!", "Incorrect handling of invalid NIP length")

    @parameterized.expand([
        ("valid_nip_and_registered", "Whata", "Hell", "12345678901", "MegaLLODON", "84616275634")
    ])
    def test_firm_account_valid_registered_nip(self, condition, name, surname, pesel, firm_name, nip):
        firm_account = FirmAccount(name, surname, pesel, firm_name, nip)

        with patch('app.FirmAccount.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            is_valid = firm_account.selfValidate(nip)
            self.assertTrue(is_valid, "NIP should be recognized as valid")
            self.assertEqual(firm_account.nip, nip, "NIP should be set correctly when valid and registered")

    @parameterized.expand([
        ("valid_nip_not_registered", "Whata", "Hell", "12345678902", "MegaLLODON", "84616275642")
    ])
    def test_firm_account_valid_not_registered_nip(self, condition, name, surname, pesel, firm_name, nip):
        firm_account = FirmAccount(name, surname, pesel, firm_name, nip)

        with patch('app.FirmAccount.requests.get') as mock_get:
            mock_get.return_value.status_code = 404
            is_valid = firm_account.selfValidate(nip)
            mock_get.assert_called_once()
            self.assertFalse(is_valid, "NIP should be recognized as invalid (not registered)")
            with self.assertRaises(ValueError) as context:
                if not is_valid:
                    raise ValueError("Company not registered!")
            self.assertEqual(str(context.exception), "Company not registered!")
