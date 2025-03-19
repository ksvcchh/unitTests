import unittest
from parameterized import parameterized

from ..FirmAccount import FirmAccount

class TestLoanFirmFeature(unittest.TestCase):

    def setUp(self):
        self.account = FirmAccount("User", "SupUser", "44223031015", "Cocoa INC.", "09876543217")

    @parameterized.expand([
        (1000, 2000, -1775, 3000, 900, True, "Two of the conditions are fullfiled"),
        (2000, 100, -1775, 300, 2000, False, "Loan ammount is bigger than 2 times the firm money"),
        (2000, 1000, -1750, 400, 200, False, "There is no transers to ZUS in account's history"),
        (2000, 1000, -1750, 400, 2000, False, "Both conditions are not fullfiled"),
    ])

    def test_loan(self, *loan_params):
        loan_ammount = loan_params[-3]
        expectation = loan_params[-2]
        for transfer in loan_params[:-3]:
            self.account.incomingTransfer(transfer) if transfer > 0 else self.account.outgoingTransfer(-transfer)
        result = self.account.getLoan(loan_ammount)
        self.assertEqual(expectation, result, loan_params[-1])
