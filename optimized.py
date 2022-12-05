from pandas import DataFrame, read_csv
from sys import exit, argv


class Optimized:
    def __init__(self, csv_file):
        self.datas = DataFrame(columns=["Share Name", "Price", "Profit", "Ratio"])
        self.csv_file = csv_file
        self.pre_data_treatment()
        self.wallet = 500
        self.solution = []

    def filecheck(self):
        """
        This function open the csv file and handle error if the file doesn't exist or isn't a csv
        Returns:
            The data contained in the csv file.
        """
        brute_datas = None
        try:
            brute_datas = read_csv(
                self.csv_file, header=0, names=["Share Name", "Price", "Profit"]
            )
        except FileNotFoundError:
            print(f"No such file or directory: {self.csv_file}")
            exit(1)
        except UnicodeError:
            print("File cannot be open, are you sure is it a csv file ?")
            exit(1)
        return brute_datas

    def pre_data_treatment(self):
        brute_datas = self.filecheck()
        for i in range(0, len(brute_datas)):
            if brute_datas.iloc[i].loc["Price"] <= 0:
                pass
            elif float(brute_datas.iloc[i].loc["Profit"]) <= 0:
                pass
            else:
                self.add_to_datas(
                    brute_datas.iloc[i].loc["Share Name"],
                    round(brute_datas.iloc[i].loc["Price"], 2),
                    round(brute_datas.iloc[i].loc["Profit"], 2),
                )
        self.datas = self.datas.sort_values(
            by=["Ratio"], ascending=False, ignore_index=True
        )

    def add_to_datas(self, share_name, price, profit):
        """
        Add the datas that passed the check before, and change the percentage profit to value profit.
        Args:
            share_name: The name of the share.
            price: The price of the share.
            profit: The profit of the share.
        """
        profit_val = round(float(price * profit / 100), 2)
        ratio = profit_val / price * 100
        self.datas.loc[len(self.datas)] = [share_name, price, profit_val, ratio]

    # See knapsack bottom-up problem to solve this problem
    # price = weight
    # profit = values
    # max_invest * 100 = capacity
    def knapsack(self):
        ks = [
            [0 for _ in range(self.wallet + 1)] for _ in range(len(self.datas) + 1)
        ]
        for row in range(len(self.datas + 1)):
            for col in range(self.wallet + 1):
                if row == 0 or col == 0:
                    ks[row][col] = 0
                elif col >= self.datas.iloc[row - 1].loc['Price']:
                    value = (self.datas.iloc[row - 1].loc['Profit'] - self.datas.iloc[row - 1].loc['Price']) / (100 * accuracy)
                    ks[row][col] = max(value + ks[row - 1][col - self.datas.iloc[row - 1].loc['Price']], ks[row][col])
                else:
                    ks[row][col] = ks[row - 1][col]



    def show_solution(self):
        total_cost = 0
        total_profit = 0
        for elm in self.solution:
            total_profit += self.datas.iloc[elm].loc["Profit"]
            total_cost += self.datas.iloc[elm].loc["Price"]
            print(
                f"Share Name: {self.datas.iloc[elm].loc['Share Name']} | "
                f"Price: {self.datas.iloc[elm].loc['Price']} | "
                f"Profit: {self.datas.iloc[elm].loc['Profit']}"
            )
        print(f"Total cost: {total_cost} | Total profit: {total_profit}")


if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: ./optimized.py <file.csv>")
        exit(1)
    else:
        optimized = Optimized(argv[1])
        optimized.knapsack()
        exit(0)
