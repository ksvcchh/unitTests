import unittest
from parameterized import parameterized

from ..Account import Account

class TestTransferMoney(unittest.TestCase):
    def setUp(self):
        self.insufficient_funds_msg = "Outgoing transfers don't work properly while not enough money!"
        self.sufficient_funds_msg = "Outgoing transfers don't work properly while enough money!"
        self.incoming_msg = "Incoming transfers don't work properly!"

    @parameterized.expand([
        ("single_scenario", 100, 60, 60, 100, 40, 40),
    ])
    def test_transfers(self, _, incoming_amt, first_outgoing, second_outgoing, exp_after_incoming, exp_after_first_out, exp_final):
        account = Account("Acum", "Curr", "02211118664")
        account.incomingTransfer(incoming_amt)
        self.assertEqual(account.saldo, exp_after_incoming, self.incoming_msg)

        account.outgoingTransfer(first_outgoing)
        self.assertEqual(account.saldo, exp_after_first_out, self.sufficient_funds_msg)

        account.outgoingTransfer(second_outgoing)
        self.assertEqual(account.saldo, exp_final, self.insufficient_funds_msg)
