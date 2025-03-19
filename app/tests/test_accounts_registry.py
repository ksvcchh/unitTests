import unittest
from parameterized import parameterized

from ..Account import Account
from ..AccountsRegistry import AccountsRegistry

class TestAccountsRegistry(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        AccountsRegistry._accounts = []

    def setUp(self):
        AccountsRegistry._accounts = []

    @parameterized.expand([
        ("Jan", "Kowalski", "14590823167", 1, "Account was not added correctly."),
        ("Anna", "Nowak", "1086451729", 1, "Single account addition failed."),
    ])

    def test_add_account_single(self, name, surname, pesel, expected_length, failure_message):
        account = Account(name, surname, pesel)
        AccountsRegistry.add_account(account)
        self.assertEqual(len(AccountsRegistry.get_all_accounts()), expected_length, failure_message)

    @parameterized.expand([
        (
            ("Jan", "Kowalski", "12345678901"),
            ("Anna", "Nowak", "10987654321"),
            ("Piotr", "Zieliński", "11223344556"),
            3,
            "Multiple accounts were not added correctly."
        ),
        (
            ("Maria", "Wiśniewska", "99887766554"),
            ("Tomasz", "Lewandowski", "55443322110"),
            ("Ewa", "Wójcik", "66778899001"),
            3,
            "Failed to add multiple accounts."
        ),
    ])
    def test_add_account_multiple(self, acc1, acc2, acc3, expected_length, failure_message):
        accounts = [
            Account(*acc1),
            Account(*acc2),
            Account(*acc3)
        ]
        for acc in accounts:
            AccountsRegistry.add_account(acc)
        self.assertEqual(AccountsRegistry.get_account_ammount(), expected_length, failure_message)

    @parameterized.expand([
        (
            [("Jan", "Kowalski", "12345678901"),
             ("Anna", "Nowak", "10987654321")],
            "12345678901",
            True,
            "Failed to find an existing account by pesel."
        ),
        (
            [("Jan", "Kowalski", "12345678901"),
             ("Anna", "Nowak", "10987654321")],
            "00000000000",
            False,
            "Incorrectly found a non-existent account."
        ),
    ])
    def test_search_account(self, accounts, search_pesel, expected_result, failure_message):
        for acc in accounts:
            AccountsRegistry.add_account(Account(*acc))
        account = AccountsRegistry.find_account_by_pesel(search_pesel)
        if expected_result:
            self.assertIsNotNone(account, failure_message)
            if account is not None:
                self.assertEqual(account.pesel, search_pesel, "Found account has incorrect pesel.")
        else:
            self.assertIsNone(account, failure_message)

    @parameterized.expand([
        (
            [("Jan", "Kowalski", "12345678901"),
             ("Anna", "Nowak", "10987654321"),
             ("Piotr", "Zieliński", "11223344556")],
            3,
            "Account count mismatch after additions."
        ),
        (
            [("Maria", "Wiśniewska", "99887766554")],
            1,
            "Account count mismatch after adding one account."
        ),
        (
            [],
            0,
            "Account count should be zero when no accounts are added."
        ),
    ])
    def test_count_accounts(self, accounts, expected_count, failure_message):
        for acc in accounts:
            AccountsRegistry.add_account(Account(*acc))
        count = AccountsRegistry.get_account_ammount()
        self.assertEqual(count, expected_count, failure_message)

    def tearDown(self):
        AccountsRegistry._accounts = []

    @classmethod
    def tearDownClass(cls):
        AccountsRegistry._accounts = []
