from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from ...models.placedemography import *
import re
from ..tools import *
from ..favourite import *

def scroll_town(request, epidemiology_pk, epidemic_pk, region_name, country_name):
    if request.method == 'POST':
        items = request.POST.items()
        delete_from_fav_str = 'delete_from_fav'
        put_in_fav_str = 'put_in_fav'
        for item in items:
            if item[0].startswith(delete_from_fav_str):
                res = re.match(r'delete_from_fav_(.+)', item[0])
                town_name = str(res.group(1))
                # удаление города из избранного
                Favourites.objects.delete_town(epidemic_pk, region_name, country_name, town_name, request.user.username)
            elif item[0].startswith(put_in_fav_str):
                res = re.match(r'put_in_fav_(.+)', item[0])
                town_name = str(res.group(1))
                # добавление города в избранное
                Favourites.objects.add_town(epidemic_pk, region_name, country_name, town_name, request.user)

    # получаем все места поражения по id эпидемии
    towns = PlaceDemography.objects.get_towns_by_country_pk(epidemic_pk, region_name, country_name)
    two_towns_in_row = create_two_elems_in_row(towns)
    fav_towns = []
    if request.user.is_active:
        fav_towns = Favourites.objects.get_all_towns_by_username(request.user)
    return render(request, 'virus_app/place_demography/town/scroll_town.html', {'two_towns_in_row': two_towns_in_row,
                                                                                'country_name' : country_name,
                                                                                'region_name' : region_name,
                                                                                'epidemic_pk' : epidemic_pk,
                                                                                'epidemiology_pk' : epidemiology_pk,
                                                                                'fav_towns' : fav_towns})