from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from ..models.placedemography import *
from .tools import *
import re
from ..models.favourites import *

from django.contrib.auth.decorators import login_required

def scroll_epidemic(request, epidemiology_pk):
    if request.method == 'POST':
        items = request.POST.items()
        delete_from_fav_str = 'delete_from_fav'
        put_in_fav_str = 'put_in_fav'
        show_region = 'show_region'
        for item in items:
            if item[0].startswith(delete_from_fav_str):
                res = re.match(r'delete_from_fav_(\d+)', item[0])
                epidemic_pk = int(res.group(1))
                epidemic = Epidemic.objects.current_epidemic(epidemic_pk)
                # удаление эпидемии из избранного
                request.user.profile.favourite.epidemic.remove(epidemic)
            elif item[0].startswith(put_in_fav_str):
                res = re.match(r'put_in_fav_(\d+)', item[0])
                epidemic_pk = int(res.group(1))
                epidemic = Epidemic.objects.current_epidemic(epidemic_pk)
                # добавление эпидемии в избранное
                request.user.profile.favourite.epidemic.add(epidemic)
            elif item[0].startswith(show_region):
                res = re.match(r'show_region_(\d+)', item[0])
                epidemic_pk = int(res.group(1))
                return redirect('scroll_region', epidemiology_pk=epidemiology_pk, epidemic_pk=epidemic_pk)

    #получаем все эпидемии по id эпидемиологии
    epidemics = Epidemic.objects.get_epidemics_by_epidemiology_pk(epidemiology_pk)
    #all_epidemics = [[epidemic, Epidemic.objects.get_printable_data(epidemic.pk)] for epidemic in epidemics]
    two_all_epidemics_in_row = create_two_elems_in_row(epidemics)
    fav_epidemics = []
    if request.user.is_active:
        fav_epidemics = Favourites.objects.get_all_epidemics_by_username(request.user)
    return render(request, 'virus_app/epidemic/scroll_epidemic.html', {'two_all_epidemics_in_row' : two_all_epidemics_in_row,
                                                                       'epidemiology_pk' : epidemiology_pk,
                                                                       'fav_epidemics' : fav_epidemics})

def edit_epidemic_info(request, epidemiology_pk, epidemic_pk):
    epidemic = Epidemic.objects.current_epidemic(epidemic_pk)
    if request.method == 'POST':
        Epidemic.objects.post_changes_in_epidemic(epidemic_pk, request)
        return redirect('more_epidemic_info', epidemiology_pk=epidemiology_pk, epidemic_pk=epidemic_pk)

    #epidemic, other_epidemic = Epidemic.objects.get_edit_data(epidemic_pk)

    return render(request, 'virus_app/epidemic/edit_epidemic_info.html', {'epidemic' : epidemic,
                                                                          'epidemiology_pk' : epidemiology_pk})

def more_epidemic_info(request, epidemiology_pk, epidemic_pk):
    epidemic = Epidemic.objects.current_epidemic(epidemic_pk)
    if request.method == 'POST':
        return redirect('edit_epidemic_info', epidemiology_pk=epidemiology_pk, epidemic_pk=epidemic_pk)


    print_epidemic = Epidemic.objects.get_printable_data(epidemic_pk)

    return render(request, 'virus_app/epidemic/more_epidemic_info.html', {'epidemic' : epidemic,
                                                                          'print_epidemic' : print_epidemic,
                                                                          'epidemiology_pk' : epidemiology_pk})
