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
