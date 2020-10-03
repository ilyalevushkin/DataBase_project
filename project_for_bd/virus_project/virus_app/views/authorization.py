from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from ..forms import RegisterForm
from .favourite import Favourites
from django.shortcuts import redirect


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)

            favourite = Favourites()
            new_user.profile.favourite = favourite
            favourite.save()


            # Set the chosen password
            new_user.set_password(form.cleaned_data['password1'])
            new_user.profile.phone = request.POST['select-pref'] + form.cleaned_data['phone']
            # Save the User object
            new_user.save()
            username = form.cleaned_data["username"]
            messages.success(request, f'Аккаунт создан для { username }!')
            return render(request, 'virus_app/register_done.html', {
                'new_user': new_user,
            })
        else:
            messages.error(request, 'Неверно заполнена форма регистрации')
            return render(request, 'virus_app/register_lose.html')
    else:
        form = RegisterForm()
    return render(request, 'virus_app/register.html', {'form': form})