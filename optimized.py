from pandas import DataFrame, read_csv
from sys import exit, argv
from mimetypes import read_mime_types, guess_type


class Optimized:
    def __init__(self, csv_file, wallet=500):
        self.datas = DataFrame(columns=["Share Name", "Price", "Profit"])
        self.csv_file = csv_file
        self.pre_data_treatment()
        self.wallet = wallet

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
            print("File doesn't exist.")
            exit(1)
        except UnicodeError:
            print("The file isn't a csv file.")
            exit(1)
        return brute_datas

    def pre_data_treatment(self):
        """
        Treat the datas given from a csv file to check if they are all good.
        """
        brute_datas = self.filecheck()
        for i in range(0, (len(brute_datas) - 1)):
            row = brute_datas.iloc[i]
            if float(row.loc["Price"]) <= 0 or float(row.loc["Profit"]) <= 0:
                pass
            else:
                self.add_to_datas(
                    row.loc["Share Name"],
                    float(row.loc["Price"]),
                    float(row.loc["Profit"]),
                )

    def add_to_datas(self, share_name, price, profit):
        """
        Add the datas that passed the check before, and change the percentage profit to value profit.
        Args:
            share_name: The name of the share.
            price: The price of the share.
            profit: The profit of the share.
        """
        self.datas.loc[len(self.datas)] = [
            share_name,
            price,
            round(float(price * profit / 100), 2)
        ]

    # See knapsack problem to solve this problem
    # price = weight
    # profit = values
    # max_invest * 100 = capacity


if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: ./optimized.py <file.csv>")
        exit(1)
    else:
        optimized = Optimized(argv[1])
        exit(0)
