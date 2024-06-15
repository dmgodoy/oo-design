import datetime
import random


class Account:
    def __init__(self, id: int, cash: int = 0):
        self.id = id
        self.cash = cash
    def __str__(self):
        return f'{{ id : {self.id}, cash : {self.cash} }}'
class BankSystem:
    def __init__(self, accounts: dict[Account], transactions: list[str]):
        self.accounts = accounts
        self.transactions = transactions
    def __str__(self):
        return f'{{ accounts : {self.accounts} \ntransactions : {self.transactions}}}'
    def withdraw(self, teller: int, acc: Account, cash: int):
        if acc.id not in self.accounts:
            raise ValueError("Account does not exist")
        if acc.cash < cash:
            raise ValueError("Account does not have enough cash")
        acc.cash -= cash
        self.transactions.append(f'[{datetime.datetime.now()}][t:{teller}] withdraw {cash} from {acc.id}')
        
    def deposit(self, teller: int, acc: Account, cash: int):
        if acc.id not in self.accounts:
            raise ValueError("Account does not exist")
        acc.cash += cash
        self.transactions.append(f'[{datetime.datetime.now()}][t:{teller}] deposit {cash} in {acc.id}')

    def open_account(self, teller: int, cash: int) -> Account:
        acc = Account(len(self.accounts), cash)
        self.accounts[acc.id] = acc
        self.transactions.append(f'[{datetime.datetime.now()}][t:{teller}] open account {acc}')
        return acc

class Branch:
    def __init__(self, addr: str, system: BankSystem, tellers: list[int], cash: int):
        self.addr = addr
        self.tellers = tellers
        self.cash = cash
        self.system = system
    def open_account(self, cash: int) -> Account:
        teller = self.get_teller()
        return self.system.open_account(teller, cash)
    def deposit(self, acc: Account, amount: int):
        teller = self.get_teller() 
        self.system.deposit(teller, acc, amount)
        self.cash += amount
        return acc
    def withdraw(self, acc: Account, amount: int):
        if acc.cash < amount:
            raise ValueError("acc does not have enough cash")
        teller = self.get_teller() 
        self.system.withdraw(teller, acc, amount)
        self.cash -= amount
        return acc
    def get_teller(self) -> int:
        i = round(random.random() * len(self.tellers) - 1)
        return self.tellers[i]
class Bank:
    def __init__(self, bank_system: BankSystem, branches: list[Branch], cash: int):
        self.bank_system = bank_system
        self.branches = branches
        self.cash = cash
    def collect_cash(self, ratio: float):
        for b in self.branches:
            amount = b.cash * ratio
            self.cash += amount
            b.cash -= amount
    def print_accounts(self):
        print("Accounts: ")
        for id, acc in self.bank_system.accounts.items():
            print(f'{id} -> {acc}')
        
    def print_transactions(self):
        print("Transactions: ")
        for t in self.bank_system.transactions:
            print(t)


# teller id must be unique
tellers_branch1 = [0,1,3,4]
tellers_branch2 = [5,6,7]
tellers_branch3 = [8,9,10,11]

bank_system = BankSystem({}, []) # accounts, operations
branch1 = Branch('address 1', bank_system, tellers_branch1, 100_000)
branch2 = Branch('address 1', bank_system, tellers_branch2, 100_000)
branch3 = Branch('address 1', bank_system, tellers_branch3, 100_000)


bank = Bank(bank_system, [branch1, branch2, branch3], 1_000_000)
acc1 = branch1.open_account(10000)
print(branch2.withdraw(acc1, 9000))         # {id : 0, cash : 1000}
print(branch1.deposit(acc1, 10000))         # {id : 0, cash : 19000}
print(f'Bank HQ cash: {bank.cash}')         # Bank HQ cash: 1000000
print(f'branches cash: {[b.cash for b in bank.branches]}') # branches cash: [100000, 91000, 100000]
bank.collect_cash(0.1) # 10 % 
bank.print_accounts()
bank.print_transactions()
print(f'Bank HQ cash: {bank.cash}')
print(f'branches cash: {[b.cash for b in bank.branches]}')
