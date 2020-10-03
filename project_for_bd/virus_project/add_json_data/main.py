
from load_json import load_info_to_json

def print_menu():
    print("Генерирование json-файла для базы данных вирус-проекта.")
    print("Выберите действие: ")
    print("1. Добавление информации к существующему json-файлу")
    print("0. Выход")
    return int(input())


def choose_action():
    print("Выберите, что вы хотите добавить:")
    print("1. Добавить virus")
    print("2. Добавить epidemiology")
    print("3. Добавить epidemic")
    print("4. Добавить period")
    print("5. Добавить place")
    print("6. Добавить placedemography")
    print("0. Выход")
    return int(input())



while True:
    choice = print_menu()
    if (choice == 1):
        while True:
            choice = choose_action()
            if (choice == 1):
                load_info_to_json("virus")
            elif (choice == 2):
                load_info_to_json("epidemiology")
            elif (choice == 3):
                load_info_to_json("epidemic")
            elif (choice == 4):
                load_info_to_json("period")
            elif (choice == 5):
                load_info_to_json("place")
            elif (choice == 6):
                load_info_to_json("placedemography")
            elif (choice == 0):
                break
    elif (choice == 0):
        break