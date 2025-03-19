import unittest
from parameterized import parameterized

from ..Account import Account

class TestLoanUserFeature(unittest.TestCase):

    def setUp(self):
        self.account = Account("User", "SurUser", "00112233445")

    @parameterized.expand([
        (100, 200, 300, 900, True, "Last 3 transactions were incoming transfers"),
        (1000, -800, -100, 200, 300, 900, False,
            "Neither last 3 transactions were incoming nor sum of last 5 transactions was bigger than loan amount(main)"),
        (300, -200, 100, 300, -200, 100, 900, False,
            "Neither last 3 transactions were incoming(main) nor sum of last 5 transactions was bigger than loan amount"),
        (250, -50, 300, -50, 300, 700, True, "Sum of last 5 transactions exceeds loan amount"),
    ])

    def test_loan(self, *loan_params):
        loan_ammount = loan_params[-3]
        expectation = loan_params[-2]
        for transfer in loan_params[:-3]:
            self.account.incomingTransfer(transfer) if transfer > 0 else self.account.outgoingTransfer(-transfer)
        result = self.account.getLoan(loan_ammount)
        self.assertEqual(expectation, result, loan_params[-1])
