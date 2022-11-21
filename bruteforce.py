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
        """
        Generate all the permutations from 1 to len(data).
        """
        i = 1
        while i != len(self.data) + 1:
            perm = list(permutations(self.data.index, i))
            self.remove_duplicates(perm)
            print(f"Generated {len(self.list)} Combination !")
            i += 1

    def migrate_list_elements(self, res):
        """
        Migrate the sorted permutations to self.list.
        Args:
            res: the element to migrate.
        """
        for elm in res:
            self.list.append(elm)

    def remove_duplicates(self, perm):
        """
        Sort the list of permutations and remove duplicate.
        Args:
            perm: the permutations list.
        """
        new_list = []
        for elm in perm:
            new_list.append(list(elm))
        for elm in new_list:
            elm.sort()
        res = []
        [res.append(x) for x in new_list if x not in res]
        self.migrate_list_elements(res)

    def get_money_invested(self, shares):
        """
        Calculate how much money costed a list of share.
        Args:
            shares: the list of share

        Returns:
            the cost of the list of share
        """
        price = 0
        for elm in shares:
            price += int(self.data["Price"][elm])
        return price

    def remove_constraint_overflow(self):
        """
        Check if the cost is less than 500 and add the index of the list and the cost to a dictionary.
        """
        for elm in self.list:
            total_price = self.get_money_invested(elm)
            if total_price < self.wallet:
                self.dico.update({self.list.index(elm): [total_price]})

    def calculate_single_profit(self, elm):
        """
        Calculate the profit for a single share.
        Args:
            elm: the index of the share.
        Returns:
            the profit for that share
        """
        price = self.data["Price"].loc[elm]
        profit_percent = self.data["Profit"].loc[elm]
        profit = (price * ((profit_percent / 100) + 1)) - price
        return profit

    def calculate_total_profit(self, index):
        """
        Calculate the total profit for a list of share.
        Args:
            index: the index of the list of share.

        Returns:
            the total profit for the list of share.

        """
        total_profit = 0
        for elm in self.list[index]:
            profit = self.calculate_single_profit(elm)
            total_profit += profit
            self.update_dico(index, profit)
        self.update_dico(index, total_profit)
        return total_profit

    def update_dico(self, index, profit):
        """
        Update the dictionary.
        Args:
            index: the index of the list of share and at the same time the key of the dictionary.
            profit: The value to add to the dictionary.
        """
        new_list = self.dico[index]
        new_list.append(profit)
        self.dico.update({index: new_list})

    def find_best_investment(self):
        """
        Find the investment that make the better profit.
        """
        self.best_investment = None
        for key in self.dico.keys():
            profit = self.calculate_total_profit(key)
            if profit > self.best_profit:
                self.best_profit = profit
                self.best_investment = key

    def generate_report(self):
        """
        Generate a csv report with the details of the best investment to do.
        """
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
                round(other_data[i], 2),
            ]
            i += 1
        df.loc[len(df)] = [
            "Total cost",
            other_data[0],
            "Total profit",
            round(other_data[len(other_data) - 1], 2),
        ]
        df.to_csv("Best-Investment.csv", index=False)

    def force(self):
        """
        The main function that include all the step to bruteforce the best investment.
        """
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
