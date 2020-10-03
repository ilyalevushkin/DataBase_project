from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from ..models.virus import *
from ..models.favourites import *
from ..models.placedemography import *
from .tools import *
import re

from django.contrib.auth.decorators import login_required

def base_info(request):
    if request.method == 'POST':
        items = request.POST.items()
        delete_from_fav_str = 'delete_from_fav'
        put_in_fav_str = 'put_in_fav'
        show_epidemics = 'show_epidemics'

        for item in items:
            if item[0].startswith(delete_from_fav_str):
                res = re.match(r'delete_from_fav_(\d+)', item[0])
                virus_pk = int(res.group(1))
                virus = Virus.objects.current_virus(virus_pk)
                #удаление вируса из избранного
                request.user.profile.favourite.virus.remove(virus)
                pass
            elif item[0].startswith(put_in_fav_str):
                res = re.match(r'put_in_fav_(\d+)', item[0])
                virus_pk = int(res.group(1))
                virus = Virus.objects.current_virus(virus_pk)
                #добавление вируса в избранное
                request.user.profile.favourite.virus.add(virus)
            elif item[0].startswith(show_epidemics):
                res = re.match(r'show_epidemics_(\d+)', item[0])
                virus_pk = int(res.group(1))
                virus = Virus.objects.current_virus(virus_pk)
                epidemiology_pk = virus.epidemiology.pk
                return redirect('scroll_epidemic',
                                epidemiology_pk=epidemiology_pk)

    viruses = Virus.objects.base_information()
    two_viruses_in_row = create_two_elems_in_row(viruses)
    fav_viruses = Favourites.objects.get_all_viruses_by_username(
        request.user)
    return render(request, 'virus_app/virus/scroll_virus.html',
                  {'two_viruses_in_row' : two_viruses_in_row,
                   'fav_viruses' : fav_viruses})


def edit_virus_info(request, pk):
    virus = Virus.objects.current_virus(pk)
    if request.method == 'POST':
        Epidemiology.objects.post_changes_in_epidemiology(
            virus.epidemiology.pk, request.POST)
        try:
            virus.photo = request.FILES['photo']
        except:
            pass
        virus.save()
        return redirect('more_virus_info', pk=pk)

    epidemiology, other_epidemiology = Epidemiology.objects.\
        get_edit_data(virus.epidemiology.pk)

    return render(request, 'virus_app/virus/edit_virus_info.html',
                  {'virus' : virus,
                   'epidemiology' : epidemiology,
                   'other_epidemiology' : other_epidemiology})

def more_virus_info(request, pk):
    virus = Virus.objects.current_virus(pk)
    if request.method == 'POST':
        return redirect('edit_virus_info', pk=pk)

    epidemiology = Epidemiology.objects.get_printable_data(
        virus.epidemiology.pk)

    return render(request, 'virus_app/virus/more_virus_info.html',
                  {'virus' : virus,
                   'epidemiology' : epidemiology})