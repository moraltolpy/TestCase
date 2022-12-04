from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from pet_app.forms.register_forms import UserRegisterForm
from pet_app.views.helper import delegate


def choose_action(request):
    return delegate(
        request,
        get=get_form,
        post=create_user
    )


def get_form(request):
    form = UserRegisterForm()
    return render(request, 'pet_app/register.html', {'form': form})


def create_user(request):
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        new_user = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)

        messages.success(request, '<i class="fas fa-check"></i> Welcome onboard %s!' % username)
        login(request, new_user)
        return redirect('app_index')
    return render(request, 'pet_app/register.html', {'form': form})
