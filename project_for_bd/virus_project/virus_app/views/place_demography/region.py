from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from ...models.placedemography import *
from ..favourite import *
import re
from ..tools import *

def scroll_region(request, epidemiology_pk, epidemic_pk):
    if request.method == 'POST':
        items = request.POST.items()
        delete_from_fav_str = 'delete_from_fav'
        put_in_fav_str = 'put_in_fav'
        show_country = 'show_country'
        for item in items:
            if item[0].startswith(delete_from_fav_str):
                res = re.match(r'delete_from_fav_(.+)', item[0])
                region_name = str(res.group(1))
                # удаление места поражения из избранного
                Favourites.objects.delete_region(epidemic_pk, region_name, request.user.username)
            elif item[0].startswith(put_in_fav_str):
                res = re.match(r'put_in_fav_(.+)', item[0])
                region_name = str(res.group(1))
                # добавление места поражения в избранное
                Favourites.objects.add_region(epidemic_pk, region_name, request.user)
            elif item[0].startswith(show_country):
                res = re.match(r'show_country_(.+)', item[0])
                region_name = str(res.group(1))
                return redirect('scroll_country', epidemiology_pk=epidemiology_pk,
                                epidemic_pk=epidemic_pk,
                                region_name=region_name)

    # получаем все места поражения по id эпидемии
    region = PlaceDemography.objects.get_regions_by_epidemic_pk(epidemic_pk)
    two_regions_in_row = create_two_elems_in_row(region)
    fav_regions = []
    if request.user.is_active:
        fav_regions = Favourites.objects.get_all_regions_by_username(request.user)
    return render(request, 'virus_app/place_demography/region/scroll_region.html', {'two_regions_in_row': two_regions_in_row,
                                                                                    'epidemiology_pk' : epidemiology_pk,
                                                                                    'epidemic_pk' : epidemic_pk,
                                                                                    'fav_regions' : fav_regions})
