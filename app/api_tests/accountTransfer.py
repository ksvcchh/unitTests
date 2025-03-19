import unittest
import requests
import time

class TestAccountTransfers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_accounts_url = "http://127.0.0.1:5000/api/accounts"
        cls.reset_url = "http://127.0.0.1:5000/api/test/reset"
        cls.transfer_url_template = "http://127.0.0.1:5000/api/accounts/{}/transfer"
        time.sleep(1)

    def setUp(self):
        requests.post(self.reset_url)
        self.test_pesel = "03210912224"
        payload = {
            "name": "Jorje",
            "surname": "Sanchez",
            "pesel": self.test_pesel
        }
        response = requests.post(self.base_accounts_url, json=payload)
        self.assertEqual(response.status_code, 201, "Konto testowe powinno zostać utworzone")
        incoming_payload = {"amount": 1000, "type": "incoming"}
        response_in = requests.post(self.transfer_url_template.format(self.test_pesel), json=incoming_payload)
        self.assertEqual(response_in.status_code, 200, "Przelew incoming powinien zadziałać")

    def tearDown(self):
        requests.delete(f"{self.base_accounts_url}/{self.test_pesel}")

    def test_incoming_transfer(self):
        payload = {"amount": 500, "type": "incoming"}
        response = requests.post(self.transfer_url_template.format(self.test_pesel), json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Zlecenie przyjęto do realizacji", response.json()["message"])

    def test_outgoing_transfer_success(self):
        payload = {"amount": 500, "type": "outgoing"}
        response = requests.post(self.transfer_url_template.format(self.test_pesel), json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Zlecenie przyjęto do realizacji", response.json()["message"])

    def test_outgoing_transfer_failure(self):
        payload = {"amount": 1500, "type": "outgoing"}
        response = requests.post(self.transfer_url_template.format(self.test_pesel), json=payload)
        self.assertEqual(response.status_code, 422)
        self.assertIn("Insufficient funds", response.json()["error"])

    def test_express_transfer_success(self):
        payload = {"amount": 500, "type": "express"}
        response = requests.post(self.transfer_url_template.format(self.test_pesel), json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Zlecenie przyjęto do realizacji", response.json()["message"])

    def test_express_transfer_failure(self):
        payload = {"amount": 1000, "type": "express"}
        response = requests.post(self.transfer_url_template.format(self.test_pesel), json=payload)
        self.assertEqual(response.status_code, 422)
        self.assertIn("Express transfer failed", response.json()["error"])

    def test_unknown_transfer_type(self):
        payload = {"amount": 100, "type": "fast"}
        response = requests.post(self.transfer_url_template.format(self.test_pesel), json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Unsupported transfer type", response.json()["error"])

    def test_transfer_account_not_found(self):
        payload = {"amount": 100, "type": "incoming"}
        nonexistent_pesel = "99999999999"
        response = requests.post(self.transfer_url_template.format(nonexistent_pesel), json=payload)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Account not found", response.json()["error"])

if __name__ == '__main__':
    unittest.main()
