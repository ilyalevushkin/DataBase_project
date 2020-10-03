from datetime import datetime, date
from math import *

def get_region_name():
    return str(input("Введите название региона: "))

def get_country_name():
    return str(input("Введите название страны: "))

def get_country_population():
    return int(input("Введите популяцию страны: "))

def get_town_count():
    return int(input("Введите количество городов: "))

def get_date_range():
    date_str_from = input("Введите от какого периода (date):")
    date_str_to = input("Введите до какого периода (date):")
    date_from = datetime.strptime(date_str_from, '%m/%d/%Y').date()
    date_to = datetime.strptime(date_str_to, '%m/%d/%Y').date()
    return [date_from, date_to]

def get_epidemic_pk():
    return int(input("Введите pk эпидемии: "))


def get_periods_count():
    return int(input("Введите количество периодов в городе: "))

def get_last_pk(model_str):
    return int(input("Введите последний pk " + model_str + ": "))


def create_date_list(n, date_from_to):
    date_dif = date_from_to[1] - date_from_to[0]
    lst = []
    add_date = date_dif / n
    base_date = date_from_to[0]
    for i in range(n):
        lst.append(base_date)
        base_date += add_date
    return lst


def get_file_name(model_str):
    return str(input("Введите имя файла (csv), куда будет записываться " + model_str + ": "))


def add_path(path, file_name):
    return path + file_name


def write_list_in_file(lst, f):
    for i in range(len(lst) - 1):
        f.write(str(lst[i]) + '\,')
    f.write(str(lst[-1]) + '\n')

def period_create(date_from_to, period_file_name, n):
    date_list = create_date_list(n, date_from_to)

    last_period_pk = get_last_pk("period")
    period_list_pk = [(i + last_period_pk + 1) for i in range(len(date_list) - 1)]

    with open(period_file_name, "a") as write_file:
        for i in range(len(date_list) - 1):
            write_list_in_file([period_list_pk[i], date_list[i], date_list[i + 1]], write_file)



    return period_list_pk



def get_unique_town_name(id):
    return "Town_name" + str(id)


def place_create(country_name, town_count, region_name, town_population, place_file_name):
    last_place_pk = get_last_pk("place")
    place_list_pk = [(i + last_place_pk + 1) for i in range(town_count)]

    with open(place_file_name, "a") as write_file:
        for i in range(town_count):
            write_list_in_file([place_list_pk[i], country_name,
                                get_unique_town_name(place_list_pk[i]), region_name, town_population], write_file)

    return place_list_pk


def place_filling(country_name, town_count, region_name, town_population):
    place_file_name = add_path("../data/", get_file_name("place"))

    place_list_pk = place_create(country_name, town_count, region_name, town_population, place_file_name)
    return place_list_pk

def period_filling():
    period_file_name = add_path("../data/", get_file_name("period"))

    n = get_periods_count()
    date_from_to = get_date_range()
    period_list_pk = period_create(date_from_to, period_file_name, n)
    return period_list_pk



def logistic_equation(K, P_0, r, t):
    return (K * P_0 * exp(r * t))/ (K + P_0 *(exp(r * t) - 1))

def get_infected_count(place_pk, period_pk, town_population):

    #максимальный процент зараженных (плато)
    max_infected_percent = abs(sin(place_pk)) * 0.6
    K = max_infected_percent * town_population + 100

    #чем больше, тем больше зараженных с самого начала (y(0) = P_0) и тем раньше выйдет на плато
    #процент зараженных с самого начала
    start_infected_percent = abs(sin(place_pk + 0.7)) * 0.6
    P_0 = start_infected_percent * K

    #скорость роста графика
    r = 10 / K

    return logistic_equation(K, P_0, r, period_pk)



def get_dead_count(place_pk, period_pk, infected_count):
    #максимальный процент смертности среди зараженных
    max_death_percent = 0.6
    k = period_pk % 10
    death_percent = max_death_percent * abs(abs(sin(place_pk)) - 0.01 * k)
    return death_percent * infected_count


def get_recovered_count(place_pk, period_pk, infected_count):
    # максимальный процент выздоровевших среди зараженных
    max_recovered_percent = 0.6
    k = period_pk % 10
    recovered_percent = max_recovered_percent * abs(abs(sin(place_pk)) - 0.01 * k)
    return recovered_percent * infected_count

def placedemography_create():
    region_name = get_region_name()
    country_name = get_country_name()
    country_population = get_country_population()
    town_count = get_town_count()

    town_population = int(country_population / float(town_count))

    period_list_pk = period_filling()
    place_list_pk = place_filling(country_name, town_count, region_name, town_population)


    epidemic_pk = get_epidemic_pk()

    placedemography_file_name = add_path("../data/", get_file_name("placedemography"))

    last_placedemography_pk = get_last_pk("placedemography") + 1

    with open(placedemography_file_name, "a") as write_file:
        for place_pk in place_list_pk:
            for period_pk in period_list_pk:
                town_infected = get_infected_count(place_pk, period_pk, town_population)
                town_dead = get_dead_count(place_pk, period_pk, town_infected)
                town_recovered = get_recovered_count(place_pk, period_pk, town_infected)
                write_list_in_file([last_placedemography_pk,
                                    int(town_infected),
                                    int(town_recovered),
                                    int(town_dead),
                                    epidemic_pk, period_pk, place_pk], write_file)
                last_placedemography_pk += 1
