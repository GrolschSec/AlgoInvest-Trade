from csv import reader
from sys import exit, argv
from magic import Magic


class Optimized:
    def __init__(self, csv_file, wallet=500):
        self.csv_file = csv_file
        self.datas = self.pre_data_treatment()
        self.wallet = wallet
        self.best_investment = []

    def open_csv(self):
        """
        Function that open a file and handle error like isADirectory and FileNotFound.
        """
        try:
            return open(self.csv_file)
        except FileNotFoundError:
            print(f"No such file or directory: '{self.csv_file}'")
            exit(1)
        except IsADirectoryError:
            print(f"Is a directory: '{self.csv_file}'")
            exit(1)

    def mimecheck(self):
        """
        Function that check if the mimetype of a file is csv or not and exit the program if not.
        """
        mime = Magic(mime=True)
        try:
            if mime.from_file(self.csv_file) != "text/csv":
                raise ValueError
        except ValueError:
            print("Invalid mimetype, the dataset should be a csv file.")
            exit(1)

    def pre_data_treatment(self):
        """
        This function is checking the datas in the csv file if there are correct like bigger than 0,
        and return the new datas without the bad information.
        Returns:
            datas: the new list of shares without error.
        """
        datas = []
        csv_file = self.open_csv()
        self.mimecheck()
        csv_reader = reader(csv_file)
        for row in csv_reader:
            if row[1].isalpha() is True and row[2].isalpha() is True:
                pass
            elif float(row[1]) <= 0 or float(row[2]) <= 0:
                pass
            else:
                datas.append(
                    {
                        'Share': row[0],
                        'Price': int(float(row[1]) * 100),
                        'Profit': float(float(row[1]) * float(row[2]) / 100),
                    }
                )
        return datas

    # See knapsack bottom-up problem to solve this problem
    # price = weight
    # profit = values
    # max_invest * 100 = capacity (* 100 to avoid float because we use it for index)
    def knapsack(self, n, w_max):
        matrix = [
            [-1 for _ in range(0, w_max + 1)] for _ in range(0, len(self.datas) + 1)
        ]
        for i in range(1, n + 1):
            for w in range(1, w_max + 1):
                if i == 0 or w == 0:
                    matrix[i][w] = 0
                elif float(self.datas[i - 1]['Price']) <= w:
                    matrix[i][w] = max(
                        self.datas[i - 1]['Profit']
                        + matrix[i - 1][w - self.datas[i - 1]['Price']],
                        matrix[i - 1][w],
                    )
                else:
                    matrix[i][w] = matrix[i - 1][w]

        while w_max >= 0 and n >= 0:
            if (
                matrix[n][w_max]
                == matrix[n - 1][w_max - self.datas[n - 1]['Price']]
                + self.datas[n - 1]['Profit']
            ):
                self.best_investment.append(n - 1)
                w_max -= self.datas[n - 1]['Price']
            n -= 1

    def show_result(self):
        total_cost = 0
        total_profit = 0
        print("Share Name | Price | Profit (after 2 years)")
        for elm in self.best_investment:
            total_cost += self.datas[elm]['Price'] / 100
            total_profit += self.datas[elm]['Profit']
            print(
                f"{self.datas[elm]['Share']}"
                f" | {round(self.datas[elm]['Price'] / 100, 2)} €"
                f" | {round(self.datas[elm]['Profit'], 2)} €"
            )
        print(
            f"Total Cost: {total_cost} € | Total Profit (after 2 years): {round(total_profit, 2)} €"
        )

    def solve(self):
        self.knapsack(len(self.datas), self.wallet * 100)
        self.show_result()


if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: ./optimized.py <file.csv>")
        exit(1)
    else:
        optimized = Optimized(argv[1])
        optimized.solve()
        exit(0)
