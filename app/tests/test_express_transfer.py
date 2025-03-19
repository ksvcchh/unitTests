import unittest
from parameterized import parameterized

from ..Account import Account
from ..FirmAccount import FirmAccount

class TestExpressTransfer(unittest.TestCase):
    @parameterized.expand([
        ("express_transfer_user_scenario",
            "Horje", "Morjo", "38069156311", 200, 200, 1, -1, [200, -200, -1]),
    ])
    def test_express_transfer_user(self, _, name, surname, pesel, incoming_amt, express_amt_success, express_amt_fail, exp_saldo, exp_history):
        account = Account(name, surname, pesel)
        account.incomingTransfer(incoming_amt)
        account.expressTransfer(express_amt_success)
        self.assertEqual(account.saldo, exp_saldo, "Incorrect amount of money left after express transfer")
        account.expressTransfer(express_amt_fail)
        self.assertEqual(account.saldo, exp_saldo, "Shouldn't be able to transfer money from account with overdraft")
        self.assertEqual(account.history, exp_history, "Incorrect account history after transfers")

    @parameterized.expand([
        ("express_transfer_firm_account_scenario",
        "Horje", "Morjo", "38069156311", "Sad Horje", "12332145691", 200, 200, 1, -5, [200, -200, -5]),
    ])
    def test_express_transfer_firm_account(self, _, name, surname, pesel, firm_name, nip,
                                            incoming_amt, express_amt_success, express_amt_fail, exp_saldo, exp_history):
        firm_account = FirmAccount(name, surname, pesel, firm_name, nip)
        firm_account.incomingTransfer(incoming_amt)
        firm_account.expressTransfer(express_amt_success)
        self.assertEqual(firm_account.saldo, exp_saldo, "Incorrect amount of money left after express transfer on firm account")
        firm_account.expressTransfer(express_amt_fail)
        self.assertEqual(firm_account.saldo, exp_saldo, "Shouldn't be able to transfer money from account with overdraft")
        self.assertEqual(firm_account.history, exp_history, "Incorrect firm account history after transfers")
