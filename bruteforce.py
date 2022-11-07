from itertools import permutations
from sys import argv, exit
from pandas import read_csv, DataFrame


class Bruteforce:
    def __init__(self, file_csv):
        self.wallet = 500
        self.list = []
        self.data = read_csv(file_csv, names=["Share", "Price", "Profit"], header=0)
        self.dico = {}
        self.best_profit = 0
        self.best_investment = 0

    def generate_bruteforce_list(self):
        i = 1
        while i != len(self.data):
            perm = list(permutations(self.data.index, i))
            self.remove_duplicates(perm)
            print(f"Generated {len(self.list)} Combination !")
            i += 1

    def migrate_list_elements(self, res):
        for elm in res:
            self.list.append(elm)

    def remove_duplicates(self, perm):
        new_list = []
        for elm in perm:
            new_list.append(list(elm))
        for elm in new_list:
            elm.sort()
        res = []
        [res.append(x) for x in new_list if x not in res]
        self.migrate_list_elements(res)

    def get_money_invested(self, shares):
        price = 0
        for elm in shares:
            price += int(self.data["Price"][elm])
        return price

    def remove_constraint_overflow(self):
        for elm in self.list:
            total_price = self.get_money_invested(elm)
            if total_price < 500:
                self.dico.update({self.list.index(elm): [total_price]})

    def calculate_single_profit(self, elm):
        price = self.data["Price"].loc[elm]
        profit_percent = self.data["Profit"].loc[elm]
        profit = (price * ((profit_percent / 100) + 1)) - price
        return profit

    def calculate_total_profit(self, index):
        total_profit = 0
        for elm in self.list[index]:
            profit = self.calculate_single_profit(elm)
            total_profit += profit
            self.update_dico(index, profit)
        self.update_dico(index, total_profit)
        return total_profit

    def update_dico(self, index, profit):
        new_list = self.dico[index]
        new_list.append(profit)
        self.dico.update({index: new_list})

    def find_best_investment(self):
        self.best_investment = None
        for key in self.dico.keys():
            profit = self.calculate_total_profit(key)
            if profit > self.best_profit:
                self.best_profit = profit
                self.best_investment = key

    def generate_report(self):
        shares_index = self.list[self.best_investment]
        other_data = self.dico[self.best_investment]
        df = DataFrame(
            columns=[
                "Share",
                "Price",
                "Profit after 2 years (percent)",
                "Profit after 2 years (values)",
            ]
        )
        i = 1
        for share in shares_index:
            df.loc[len(df)] = [
                self.data["Share"].iloc[share],
                self.data["Price"].iloc[share],
                self.data["Profit"].iloc[share],
                other_data[i],
            ]
            i += 1
        df.loc[len(df)] = [
            "Total cost",
            other_data[0],
            "Total profit",
            other_data[len(other_data) - 1],
        ]
        df.to_csv("Best-Investment.csv")

    def force(self):
        self.generate_bruteforce_list()
        self.remove_constraint_overflow()
        self.find_best_investment()
        self.generate_report()


if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: ./bruteforce.py <file.csv>")
        exit(1)
    else:
        brute = Bruteforce(argv[1])
        brute.force()
        exit(0)
