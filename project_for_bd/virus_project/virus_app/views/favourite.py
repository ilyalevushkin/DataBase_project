from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .tools import *
from ..models import *
import re
import json

def favourite(request):
    if request.method == 'POST':
        items = request.POST.items()
        delete_from_fav_virus_str = 'delete_from_fav_virus'
        delete_from_fav_epidemic_str = 'delete_from_fav_epidemic'
        delete_from_fav_region_str = 'delete_from_fav_region'
        delete_from_fav_country_str = 'delete_from_fav_country'
        delete_from_fav_town_str = 'delete_from_fav_town'
        option_region_str = 'option_region'
        option_country_str = 'option_country'
        option_town_str = 'option_town'
        graphics = [[], [], []]
        flag = False
        for item in items:
            if item[0].startswith(delete_from_fav_virus_str):
                res = re.match(r'delete_from_fav_virus_(.+)', item[0])
                virus_pk = str(res.group(1))
                virus = Virus.objects.current_virus(virus_pk)
                # удаление вируса из избранного
                request.user.profile.favourite.virus.remove(virus)
                flag = False
                break
            elif item[0].startswith(delete_from_fav_epidemic_str):
                res = re.match(r'delete_from_fav_epidemic_(.+)', item[0])
                epidemic_pk = str(res.group(1))
                epidemic = Epidemic.objects.current_epidemic(epidemic_pk)
                # удаление эпидемии из избранного
                request.user.profile.favourite.epidemic.remove(epidemic)
                flag = False
                break
            elif item[0].startswith(delete_from_fav_region_str):
                res = re.match(r'delete_from_fav_region_(.+)__(.+)', item[0])
                epidemic_pk = str(res.group(1))
                region_name = str(res.group(2))
                Favourites.objects.delete_region(epidemic_pk, region_name, request.user.username)
                flag = False
                break
            elif item[0].startswith(delete_from_fav_country_str):
                res = re.match(r'delete_from_fav_country_(.+)__(.+)__(.+)', item[0])
                epidemic_pk = str(res.group(1))
                region_name = str(res.group(2))
                country_name = str(res.group(3))
                Favourites.objects.delete_country(epidemic_pk, region_name, country_name, request.user.username)
                flag = False
                break
            elif item[0].startswith(delete_from_fav_town_str):
                res = re.match(r'delete_from_fav_town_(.+)__(.+)__(.+)__(.+)', item[0])
                epidemic_pk = str(res.group(1))
                region_name = str(res.group(2))
                country_name = str(res.group(3))
                town_name = str(res.group(4))
                Favourites.objects.delete_town(epidemic_pk, region_name, country_name, town_name, request.user.username)
            elif item[0].startswith(option_region_str):
                res = re.match(r'option_region_(.+)__(.+)', item[0])
                epidemic_pk = str(res.group(1))
                region_name = str(res.group(2))
                graphics[0].append([epidemic_pk, region_name])
                flag = True
            elif item[0].startswith(option_country_str):
                res = re.match(r'option_country_(.+)__(.+)__(.+)', item[0])
                epidemic_pk = str(res.group(1))
                region_name = str(res.group(2))
                country_name = str(res.group(3))
                graphics[1].append([epidemic_pk, region_name, country_name])
                flag = True
            elif item[0].startswith(option_town_str):
                res = re.match(r'option_town_(.+)__(.+)__(.+)__(.+)', item[0])
                epidemic_pk = str(res.group(1))
                region_name = str(res.group(2))
                country_name = str(res.group(3))
                town_name = str(res.group(4))
                graphics[2].append([epidemic_pk, region_name, country_name, town_name])
                flag = True
        if (flag == True):
            return print_graphics(request, graphics=graphics)

    viruses = Favourites.objects.get_all_viruses_by_username(request.user)
    epidemics = Favourites.objects.get_all_epidemics_by_username(request.user)
    regions = Favourites.objects.get_all_regions_by_username(request.user)
    countries = Favourites.objects.get_all_countries_by_username(request.user)
    towns = Favourites.objects.get_all_towns_by_username(request.user)

    two_viruses_in_row = create_two_elems_in_row(viruses)
    two_epidemics_in_row = create_two_elems_in_row(epidemics)
    two_regions_in_row = create_two_elems_in_row(regions)
    two_countries_in_row = create_two_elems_in_row(countries)
    two_towns_in_row = create_two_elems_in_row(towns)

    return render(request, 'virus_app/favourite.html', {'two_viruses_in_row' : two_viruses_in_row,
                                                        'two_epidemics_in_row' : two_epidemics_in_row,
                                                        'two_regions_in_row' : two_regions_in_row,
                                                        'two_countries_in_row' : two_countries_in_row,
                                                        'two_towns_in_row' : two_towns_in_row})




def print_graphics(request, graphics):
    region_data, date_region_data = [[], [], []], [[], [], []]
    country_data, date_country_data = [[], [], []], [[], [], []]
    town_data, date_town_data = [[], [], []], [[], [], []]
    if (len(graphics[0]) != 0):
        region_data, date_region_data = Favourites.objects.get_region_graphics_data(graphics[0])
    if (len(graphics[1]) != 0):
        country_data, date_country_data = Favourites.objects.get_country_graphics_data(graphics[1])
    if (len(graphics[2]) != 0):
        town_data, date_town_data = Favourites.objects.get_town_graphics_data(graphics[2])


    return render(request, 'virus_app/print_graphics.html', {'date_region_infected_data' : json.dumps(date_region_data[0]),
                                                             'region_infected_data': json.dumps(region_data[0]),
                                                             'date_region_recovered_data': json.dumps(date_region_data[1]),
                                                             'region_recovered_data': json.dumps(region_data[1]),
                                                             'date_region_dead_data': json.dumps(date_region_data[2]),
                                                             'region_dead_data': json.dumps(region_data[2]),
                                                             'date_country_infected_data' : json.dumps(date_country_data[0]),
                                                             'country_infected_data': json.dumps(country_data[0]),
                                                             'date_country_recovered_data': json.dumps(date_country_data[1]),
                                                             'country_recovered_data': json.dumps(country_data[1]),
                                                             'date_country_dead_data': json.dumps(date_country_data[2]),
                                                             'country_dead_data': json.dumps(country_data[2]),
                                                             'date_town_infected_data': json.dumps(date_town_data[0]),
                                                             'town_infected_data': json.dumps(town_data[0]),
                                                             'date_town_recovered_data': json.dumps(date_town_data[1]),
                                                             'town_recovered_data': json.dumps(town_data[1]),
                                                             'date_town_dead_data': json.dumps(date_town_data[2]),
                                                             'town_dead_data': json.dumps(town_data[2])})