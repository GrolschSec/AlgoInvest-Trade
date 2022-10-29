from random import randint
from sys import argv, exit
from pandas import read_csv


class Bruteforce:
    def __init__(self, var):
        self.wallet = 500
        self.list = []
        self.data = read_csv(var)

    def compare(self, last_share_option):
        if last_share_option in self.list:
            return True
        return False

    def select_share(self, share_list):
        size = len(self.data)
        share = None
        i = 0
        while share is None:
            num = randint(0, size - 1)
            if num not in share_list:
                share = num
                return share
            if i >= size:
                break
            i += 1
        return None

    def gen_share_option(self):
        share_list = []
        is_done = False
        while not is_done:
            result = self.select_share(share_list)
            if result is None:
                is_done = True
            else:
                share_list.append(result)
        return share_list

    def gen_share_list(self):
        i = 0
        while True:
            share_option = self.gen_share_option()
            comp = self.compare(share_option)
            if not comp:
                self.list.append(share_option)
                i += 1
                break

    def remove_duplicates(self):
        pass

    def remove_constraint_overflow(self):
        pass

    def find_best_investment(self):
        pass

    def gen_report(self):
        pass

    def force(self):
        self.gen_share_list()
        self.remove_duplicates()
        self.remove_constraint_overflow()
        self.find_best_investment()
        self.gen_report()


if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: ./bruteforce.py <file.csv>")
        exit(1)
    else:
        brute = Bruteforce(argv[1])
        brute.force()
        exit(0)

# Creer une classe share list
# Ou une classe Wallet
# Calculer le nombre de permutations possible et les ajouter a une premiere liste
# Trier chaque permutations du plus petit au plus grand
# Supprimer les doublons
# Pour chaque permutations calculer si elle depasse les 500 du wallet
# Si la permutations depasse les 500 elle est supprimer de la liste.
# Sinon On calculera le revenu de la permutations.
#   Si le revenu est le plus grand recontrer on stockera son id.
