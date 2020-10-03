from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    if request.method == 'POST':
        return redirect('edit_profile')
    return render(request, 'virus_app/account/profile.html', {'section': 'profile'})


def edit_profile(request):
    if request.method == 'POST':
        cur_user = request.user
        if 'photo' in request.FILES:
            cur_user.profile.photo = request.FILES['photo']
        cur_user.username = request.POST['name']
        cur_user.email = request.POST['email']
        cur_user.profile.phone = request.POST['phone']
        cur_user.profile.about = request.POST['about']
        cur_user.save()
        return redirect('profile')

    return render(request, 'virus_app/account/edit_profile.html')