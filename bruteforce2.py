from pandas import DataFrame, read_csv
from copy import copy
from sys import argv, exit, setrecursionlimit


class Bruteforce:
    def __init__(self, file_csv, wallet=500):
        self.data = None
        self.pre_data_treatment(file_csv)
        self.wallet = wallet
        self.best_solution = None

    def pre_data_treatment(self, file_csv):
        """
        Read a csv file and create a new dataframe containing same data as the csv,
        only the profit column change from percent to value.
        Args:
            file_csv: the csv file to read.
        """
        brute_datas = read_csv(
            file_csv, names=["Share Name", "Price", "Profit"], header=0
        )
        df = DataFrame(columns=["Share Name", "Price", "Profit"])
        for i in range(0, len(brute_datas)):
            df.loc[len(df)] = [
                brute_datas.iloc[i].loc["Share Name"],
                brute_datas.iloc[i].loc["Price"],
                round(
                    brute_datas.iloc[i].loc["Price"]
                    * float(brute_datas.iloc[i].loc["Profit"])
                    / 100,
                    2,
                ),
            ]
        self.data = df

    def knapsack(self, solution, currentIndex, wallet):
        """
        The Recursive way of solving the knapsack problem.
        Args:
            solution: an array containing the indexes that respect the constraint.
            currentIndex: the current index.
            wallet: the money available on the wallet.
        """
        if currentIndex < 0 or wallet == 0:
            return solution
        # res1 = self.knapsack(solution, currentIndex - 1, wallet)
        # res2 = None
        if self.data.iloc[currentIndex].loc["Price"] > wallet:
            return self.knapsack(solution, currentIndex - 1, wallet)
        else:
            res_1 = self.knapsack(solution, currentIndex - 1, wallet)
            nl = copy(solution)
            nl.append(currentIndex)
            return self.find_best(
                res_1,
                self.knapsack(
                    nl,
                    currentIndex - 1,
                    wallet - self.data.iloc[currentIndex].loc["Price"],
                ),
            )

    # Si le current index est egale ou depasse la len(dataset)
    # On retourne la solution
    # On appelle a nouveau la fonction avec l'index i + 1 et on enregistre le resultat dans une variable
    # Si le cost + le prix du share a currentIndex ne depasse pas la contrainte
    # Alors on ajoute a solution le current index
    # On appelle a nouveau la fonction avec le cost = cost + price de currentIndex,
    # currentIndex + 1 on stocke le resultat
    # return appelle a une fonction find best avec res1 res2

    def find_best(self, res1, res2):
        """
        Compare the best profit between two solutions.
        Args:
            res1: the first solution
            res2: the second solution

        Returns:
            the best solution based on the profit
        """
        if res2 is None:
            return res1
        profit1 = 0
        profit2 = 0
        for elm in res1:
            profit1 += self.data.iloc[elm].loc["Profit"]
        for elm in res2:
            profit2 += self.data.iloc[elm].loc["Profit"]
        res = max(profit1, profit2)
        if res == profit1:
            return res1
        return res2

    def print_solution(self):
        """
        Print the best solution found.
        """
        cost = 0
        profit = 0
        for elm in self.best_solution:
            cost += self.data.iloc[elm].loc["Price"]
            profit += self.data.iloc[elm].loc["Profit"]
            print(
                f"{self.data.iloc[elm].loc['Share Name']}:"
                f" {self.data.iloc[elm].loc['Price']} | "
                f"{self.data.iloc[elm].loc['Profit']}"
            )
        print(f"Total cost: {cost} | Total profit: {profit}")

    def force(self):
        """
        The main execution of the program.
        Returns:

        """
        self.best_solution = self.knapsack([], len(self.data) - 1, self.wallet)
        self.print_solution()


if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: python3 bruteforce2.py <csv_file>")
        exit(0)
    brute = Bruteforce(argv[1], 500)
    brute.force()
