from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from ...models.placedemography import *
import re
from ..tools import *
from ..favourite import *

def scroll_country(request, epidemiology_pk, epidemic_pk, region_name):
    if request.method == 'POST':
        items = request.POST.items()
        delete_from_fav_str = 'delete_from_fav'
        put_in_fav_str = 'put_in_fav'
        show_town = 'show_town'
        for item in items:
            if item[0].startswith(delete_from_fav_str):
                res = re.match(r'delete_from_fav_(.+)', item[0])
                country_name = str(res.group(1))
                # удаление страны из избранного
                Favourites.objects.delete_country(epidemic_pk, region_name, country_name, request.user.username)
            elif item[0].startswith(put_in_fav_str):
                res = re.match(r'put_in_fav_(.+)', item[0])
                country_name = str(res.group(1))
                # добавление страны в избранное
                Favourites.objects.add_country(epidemic_pk, region_name, country_name, request.user)
            elif item[0].startswith(show_town):
                res = re.match(r'show_town_(.+)', item[0])
                country_name = str(res.group(1))
                return redirect('scroll_town', epidemiology_pk=epidemiology_pk,
                                epidemic_pk=epidemic_pk,
                                region_name=region_name,
                                country_name=country_name)

    # получаем все места поражения по id эпидемии
    country = PlaceDemography.objects.get_countries_by_region_pk(epidemic_pk, region_name)
    two_countries_in_row = create_two_elems_in_row(country)
    fav_countries = []
    if request.user.is_active:
        fav_countries = Favourites.objects.get_all_countries_by_username(request.user)
    return render(request, 'virus_app/place_demography/country/scroll_country.html', {'two_countries_in_row': two_countries_in_row,
                                                                                      'epidemic_pk' : epidemic_pk,
                                                                                      'epidemiology_pk' : epidemiology_pk,
                                                                                      'region_name' : region_name,
                                                                                      'fav_countries' : fav_countries})