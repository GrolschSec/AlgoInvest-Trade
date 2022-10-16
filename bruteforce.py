from random import randint
from sys import argv, exit
from pandas import read_csv, DataFrame


def arg():
    if len(argv) != 2:
        print("Usage: ./bruteforce.py <file.csv>")
        exit(0)


# Creer un algorithm de bruteforce.
# On doit lire un fichier csv.
# Ensuite generer des combinaisons d'achats d'actions.
# on stocke les combinaisons et ensuite on verifie a chaque combinaisons generer qu'elle n'est pas dupliquer.

# Cree une combinaison
# On a un wallet de 500
# On selectionne des actions
# On verifie que les la listes n'a pas de copie similaires dans les actions proposee
#  Si on trouve une copie similaire on efface le dernier de la liste et on en selectionne un autre dans l'ordre des prix
# et on reverifie si l'on a les moyens si ils n'y a plus de combinaisons disponible.
#


def gen_share_list(data):
    wallet = float(500)
    share_list = []
    is_done = False
    while not is_done:
        result = select_share(data, wallet, share_list)
        if result is None:
            is_done = True
        else:
            share_list.append(result[0])
            wallet -= result[1]
    share_list.sort()
    return share_list


def select_share(data, wallet, share_list):
    size = len(data)
    share = None
    i = 0
    while share is None:
        num = randint(0, size - 1)
        price = float(data["price"][num])
        if num not in share_list and (wallet - price) > 0:
            share = num
            return [share, price]
        if i >= size or wallet <= 0:
            break
        i += 1
    return None


def compare(share_list, big_list):
    if share_list in big_list:
        return True
    return False


def investment_to_csv(data, share_list):
    pd = DataFrame(columns=["Share", "Invested", "Profit after two years (Percent)", "Profit after two years (value)"])
    total_profit = 0
    total_invested = 0
    for share in share_list:
        profit = data["price"][share] * (int(data['profit'][share]) / 100)
        total_profit += profit
        total_invested += data["price"][share]
        pd.loc[len(pd)] = [data["name"][share], data["price"][share], data['profit'][share], profit]
    pd.loc[len(pd)] = ["Total invested", total_invested, "Total profit", total_profit]
    pd.to_csv("best-investment.csv", index=False)


def gen_big_list(data):
    i = 0
    big_list = []
    while i < len(data) * len(data):
        share_list = gen_share_list(data)
        comp = compare(share_list, big_list)
        if not comp:
            big_list.append(share_list)
            i += 1
    return big_list


# for lists in big_list:
#    wallet = 0
#    for item in lists:
#        wallet += data['price'][item]
#    print(wallet)


def main():
    arg()
    data = read_csv(argv[1])
    investment_to_csv(data, gen_share_list(data))
    # big_list = gen_big_list(data)
    # print(len(big_list))
    # for lists in big_list:
    #    wallet = 0
    #    for item in lists:
    #        wallet += data['price'][item]
    #    print(wallet)


main()
