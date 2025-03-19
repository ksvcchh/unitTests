class Account:
    def __init__(self, name, surname, pesel, kodRabatowy=None):
        self.name = name
        self.surname = surname
        self.saldo = 0
        self.fee = 1
        self.history = []
        if len(pesel) != 11:
            self.pesel = "Niepoprawny pesel!"
        else:
            self.pesel = pesel

        if self.czyPasujeRokUrodzenia(pesel) and kodRabatowy and kodRabatowy[0:5] == "PROM_" and len(kodRabatowy) == 8:
            self.kodRabatowy = kodRabatowy
            self.saldo += 50
        else:
            self.kodRabatowy = "Nie możesz użyć tego kodu rabatowego!"

    def czyPasujeRokUrodzenia(self, pesel):
        if (int(pesel[2:4]) > 20) or (int(pesel[0:2]) > 60): #int(pesel[2:4]) > 20 dla osob 21 stólecia; int(pesel[0:2]) > 60 dla osób 20 stólecia
            return True
        return False

    def incomingTransfer(self, quant):
        self.saldo += quant
        self.history.append(quant)

    def outgoingTransfer(self, quant):
        if (self.saldo >= quant):
            self.saldo -= quant
            self.history.append(-quant)

    def expressTransfer(self, quant):
        checkSaldo = self.saldo - (quant + self.fee)
        if (checkSaldo >= -self.fee):
            self.saldo = checkSaldo
            self.history.append(-quant)
            self.history.append(-self.fee)

    def getLoan(self, loanQuant):
        firstCond = all(el > 0 for el in self.history[-3:])
        secondCond = len(self.history) >= 5 and sum(self.history[-5:]) > loanQuant
        if firstCond or secondCond:
            self.saldo += loanQuant
            self.history.append(loanQuant)
            return True
        return False


class FirmAccount(Account):
    def __init__(self, name, surname, pesel, firm_name, nip):
        super().__init__(name, surname, pesel)
        self.firm_name = firm_name
        self.fee = 5
        if (len(nip) != 11):
            self.nip = "Niepoprawny NIP!"
        else:
            self.nip = nip

    def getLoan(self, loanQuant):
        firstCond = self.saldo > 2 * loanQuant
        secondCond = any(elem == -1775 for elem in self.history)
        if firstCond and secondCond:
            self.saldo += loanQuant
            self.history.append(loanQuant)
            return True
        return False

class AccountsRegistry:
    _accounts = []

    @classmethod
    def add_account(cls, account):
        cls._accounts.append(account)

    @classmethod
    def find_account_by_pesel(cls, pesel):
        for account in cls._accounts:
            if account.pesel == pesel:
                return account
        return None

    @classmethod
    def get_account_ammount(cls):
        return len(cls._accounts)

    @classmethod
    def get_all_accounts(cls):
        return cls._accounts
