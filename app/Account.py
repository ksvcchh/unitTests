from datetime import date

class Account:
    def __init__(self, name, surname, pesel, kodRabatowy=None):
        self.name = name
        self.surname = surname
        self.saldo = 0
        self.fee = 1
        self.history = []
        self.messageContent = "Twoja historia konta to"
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

    def sendHistoryToEmail(self, receiver, client):
        dateToday = date.today().isoformat()
        subject = f"Wyciąg z dnia {dateToday}"
        message = (f"{self.messageContent}: {self.history}")
        return client.send(receiver, subject, message)
