import unittest
from parameterized import parameterized

from ..Account import Account

class TestCreateBankAccount(unittest.TestCase):
    @parameterized.expand([
        ("valid_account", "Dariusz", "Januszewski", "02211118665", None, "Dariusz", "Januszewski", "02211118665", 0, "Nie możesz użyć tego kodu rabatowego!"),
        ("invalid_pesel_account", "Marian", "Nowacki", "1233331", None, "Marian", "Nowacki", "Niepoprawny pesel!", 0, "Nie możesz użyć tego kodu rabatowego!")
    ])

    def test_account_creating(self, _, given_name, given_surname, given_pesel, given_code, exp_name, exp_surname, exp_pesel, exp_saldo, exp_code):
        account = Account(given_name, given_surname, given_pesel)
        self.assertEqual(account.name, exp_name, "Name not saved correctly!")
        self.assertEqual(account.surname, exp_surname, "Surname not saved correctly!")
        self.assertEqual(account.pesel, exp_pesel, "PESEL not saved or validated correctly!")
        self.assertEqual(account.saldo, exp_saldo, "Balance incorrect for given setup!")
        self.assertEqual(account.kodRabatowy, exp_code, "Discount code validation incorrect!")

    @parameterized.expand([
        ("valid_discount_code", "Dariusz", "Januszewski", "02211118664", "PROM_367", "Dariusz", "Januszewski", "02211118664", 50, "PROM_367"),
        ("invalid_discount_code", "Dariusz", "Januszewski", "02211118664", "PROM_67", "Dariusz", "Januszewski", "02211118664", 0, "Nie możesz użyć tego kodu rabatowego!"),
        ("no_discount_code_provided", "Hell", "Nah", "02211118665", None, "Hell", "Nah", "02211118665", 0, "Nie możesz użyć tego kodu rabatowego!"),
        ("elder_code_invalid", "Oma", "Gad", "55111118664", "PROM_DAS", "Oma", "Gad", "55111118664", 0, "Nie możesz użyć tego kodu rabatowego!")
    ])

    def test_discount_codes(self, _, given_name, given_surname, given_pesel, given_code, exp_name, exp_surname, exp_pesel, exp_saldo, exp_code):
        if given_code:
            account = Account(given_name, given_surname, given_pesel, given_code)
        else:
            account = Account(given_name, given_surname, given_pesel)
        self.assertEqual(account.name, exp_name, "Name not saved correctly!")
        self.assertEqual(account.surname, exp_surname, "Surname not saved correctly!")
        self.assertEqual(account.pesel, exp_pesel, "PESEL not saved or validated correctly!")
        self.assertEqual(account.saldo, exp_saldo, "Balance incorrect after applying code!")
        self.assertEqual(account.kodRabatowy, exp_code, "Discount code validation incorrect!")
