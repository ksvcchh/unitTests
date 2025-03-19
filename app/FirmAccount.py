from .Account import Account
from datetime import date
import requests

class FirmAccount(Account): # pragma: no cover
    def __init__(self, name, surname, pesel, firm_name, nip):
        super().__init__(name, surname, pesel)
        self.firm_name = firm_name
        self.fee = 5
        self.messageContent = "Historia konta Twojej firmy to"
        if (len(nip) != 11):
            self.nip = "Niepoprawny NIP!"
        else:
            self.nip = nip

    def selfValidate(self, nip):
        dateToday = date.today().isoformat()
        endpoint = f"https://wl-test.mf.gov.pl/api/search/{nip}?date={dateToday}"
        try:
            response = requests.get(endpoint)
            print(f"Walidacja NIP {nip}. response code: {response.status_code}. response: {response.text}")
            return response.status_code == 200
        except Exception as e:
            print(f"Błąd podczas walidacji NIP: {e}")
            return False

    def getLoan(self, loanQuant):
        firstCond = self.saldo > 2 * loanQuant
        secondCond = any(elem == -1775 for elem in self.history)
        if firstCond and secondCond:
            self.saldo += loanQuant
            self.history.append(loanQuant)
            return True
        return False
