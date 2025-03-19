import unittest
import requests

class TestAccountCrud(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.reset_url = "http://127.0.0.1:5000/api/test/reset"
        cls.base_url = "http://127.0.0.1:5000/api/accounts"

    def setUp(self):
        requests.post(self.reset_url)
        self.test_pesel = "03210912224"
        requests.delete(f"{self.base_url}/{self.test_pesel}")

    def test_create_account(self):
        payload = {
            "name": "James",
            "surname": "Hetfield",
            "pesel": self.test_pesel
        }
        response = requests.post(self.base_url, json=payload)
        self.assertEqual(response.status_code, 201, "Powinien zwrócić 201 CREATED")
        self.assertIn("Account created", response.text, "Brak spodziewanego komunikatu w odpowiedzi")

    def test_get_account_ok(self):
        requests.post(self.base_url, json={
            "name": "James",
            "surname": "Hetfield",
            "pesel": self.test_pesel
        })

        response = requests.get(f"{self.base_url}/{self.test_pesel}")
        self.assertEqual(response.status_code, 200, "Powinien zwrócić 200 OK przy istniejącym koncie")

        data = response.json()
        self.assertEqual(data["name"], "James", "Pole 'name' nie zgadza się z tym co wysłaliśmy")
        self.assertEqual(data["surname"], "Hetfield", "Pole 'surname' nie zgadza się")
        self.assertEqual(data["pesel"], self.test_pesel, "Pole 'pesel' nie zgadza się")

    def test_get_account_not_found(self):
        response = requests.get(f"{self.base_url}/{self.test_pesel}")
        self.assertEqual(response.status_code, 404, "Powinien zwrócić 404 NOT FOUND przy nieistniejącym koncie")
        self.assertIn("Account not found", response.text, "Brak spodziewanego komunikatu w odpowiedzi 404")

    def test_update_account(self):
        requests.post(self.base_url, json={
            "name": "James",
            "surname": "Hetfield",
            "pesel": self.test_pesel
        })

        patch_data = {"name": "Lars"}
        patch_response = requests.patch(f"{self.base_url}/{self.test_pesel}", json=patch_data)
        self.assertEqual(patch_response.status_code, 200, "Patch powinien się udać z kodem 200")

        get_response = requests.get(f"{self.base_url}/{self.test_pesel}")
        self.assertEqual(get_response.status_code, 200, "Powinien zwrócić 200 po patchu")

        data = get_response.json()
        self.assertEqual(data["name"], "Lars", "Nie zaktualizowano pola 'name' po patchu")
        self.assertEqual(data["surname"], "Hetfield", "Pole 'surname' nie powinno się zmienić")

    def test_delete_account(self):
        requests.post(self.base_url, json={
            "name": "James",
            "surname": "Hetfield",
            "pesel": self.test_pesel
        })

        delete_response = requests.delete(f"{self.base_url}/{self.test_pesel}")
        self.assertEqual(delete_response.status_code, 200, "Powinien zwrócić 200 OK przy poprawnym usuwaniu")
        self.assertIn("Account deleted", delete_response.text, "Brak spodziewanego komunikatu o usunięciu")

        get_response = requests.get(f"{self.base_url}/{self.test_pesel}")
        self.assertEqual(get_response.status_code, 404, "Konto powinno zostać usunięte, więc GET powinien zwrócić 404")

    def test_get_accounts_count(self):
        requests.post(self.reset_url)

        requests.post(self.base_url, json={
            "name": "A",
            "surname": "AA",
            "pesel": "11111111111"
        })
        requests.post(self.base_url, json={
            "name": "B",
            "surname": "BB",
            "pesel": "22222222222"
        })

        count_url = "http://127.0.0.1:5000/api/accounts/count"
        response = requests.get(count_url)
        self.assertEqual(response.status_code, 200, "Powinien zwrócić 200 OK przy sprawdzaniu liczby kont")

        data = response.json()
        self.assertIn("count", data, "W odpowiedzi powinno znaleźć się pole 'count'")
        self.assertGreaterEqual(data["count"], 2, "Liczba kont powinna być co najmniej 2")

    def test_create_account_on_used_pesel(self):
        firstPayload = {
            "name": "George",
            "surname": "Mendes",
            "pesel": self.test_pesel
        }
        secondPayload = {
            "name": "Jorje",
            "surname": "Sanchez",
            "pesel": self.test_pesel
        }
        requests.post(self.base_url, json=firstPayload)
        response2 = requests.post(self.base_url, json=secondPayload)
        self.assertEqual(response2.status_code, 409, "Przy próbie stworzenia konta na użyty pesel powinno zwrócić 409")
        self.assertIn("Account on that pesel has already been created",response2.text, "Brak odpowiedniej wiadomości o wykorzystanym numerze PESEL")

if __name__ == '__main__':
    unittest.main()
