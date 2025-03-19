import unittest
from unittest.mock import MagicMock
from datetime import date

from ..Account import Account
from ..FirmAccount import FirmAccount
from ..SMTPClient import SMTPClient

class TestSendHistoryEmail(unittest.TestCase):

    def setUp(self):
        self.email = "jaknowalski@example.com"
        self.today = date.today().isoformat()
        self.smtp_client = SMTPClient()

    def test_send_history_email_personal_success(self):
        account = Account("Jan", "Kowalski", "12345678901")
        account.incomingTransfer(100)
        account.outgoingTransfer(50)
        expected_subject = f"Wyciąg z dnia {self.today}"
        expected_text = f"Twoja historia konta to: {account.history}"

        self.smtp_client.send = MagicMock(return_value=True)
        result = account.sendHistoryToEmail(self.email, self.smtp_client)
        self.assertTrue(result)
        self.smtp_client.send.assert_called_once_with(self.email, expected_subject, expected_text)

    def test_send_history_email_personal_failure(self):
        account = Account("Jan", "Kowalski", "12345678901")
        account.incomingTransfer(100)
        expected_subject = f"Wyciąg z dnia {self.today}"
        expected_text = f"Twoja historia konta to: {account.history}"

        self.smtp_client.send = MagicMock(return_value=False)
        result = account.sendHistoryToEmail(self.email, self.smtp_client)
        self.assertFalse(result)
        self.smtp_client.send.assert_called_once_with(self.email, expected_subject, expected_text)

    def test_send_history_email_firm_success(self):
        firm_account = FirmAccount("Jak", "Nowalski", "12345678901", "SPL Sp. z o.o.", "11111111111")
        firm_account.incomingTransfer(5000)
        firm_account.outgoingTransfer(1000)
        expected_subject = f"Wyciąg z dnia {self.today}"
        expected_text = f"Historia konta Twojej firmy to: {firm_account.history}"

        self.smtp_client.send = MagicMock(return_value=True)
        result = firm_account.sendHistoryToEmail(self.email, self.smtp_client)
        self.assertTrue(result)
        self.smtp_client.send.assert_called_once_with(self.email, expected_subject, expected_text)

    def test_send_history_email_firm_failure(self):
        firm_account = FirmAccount("Jak", "Nowalski", "12345678901", "SPL Sp. z o.o.", "11111111111")
        firm_account.incomingTransfer(5000)
        expected_subject = f"Wyciąg z dnia {self.today}"
        expected_text = f"Historia konta Twojej firmy to: {firm_account.history}"

        self.smtp_client.send = MagicMock(return_value=False)
        result = firm_account.sendHistoryToEmail(self.email, self.smtp_client)
        self.assertFalse(result)
        self.smtp_client.send.assert_called_once_with(self.email, expected_subject, expected_text)
