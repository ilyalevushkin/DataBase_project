
from creator import placedemography_create


def print_menu():
    print("Выберите действие")
    print("1. Сгенерировать placedemography")
    print("0. Выход")
    return int(input())



while True:
    choice = print_menu()
    if (choice == 1):
        placedemography_create()
    elif (choice == 0):
        break