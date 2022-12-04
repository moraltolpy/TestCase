from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from pet_app.forms.pet_forms import PetForm
from pet_app.forms.user_update_forms import UserUpdateForm
from pet_app.views.helper import delegate, user_pets


@login_required
def choose_action(request):
    return delegate(
        request,
        get=get,
        post=post,
    )


def get(request):
    return render(request, 'pet_app/profile.html', {
        'pets': user_pets(request),
        'pet_form': PetForm(),
        'user_form': UserUpdateForm(request.user),
    })


def post(request):
    pet_form = PetForm(request.POST)
    user_update_form = UserUpdateForm(request.user, data=request.POST)
    if pet_form.is_valid():
        pet = pet_form.save(commit=False)
        pet.owner = request.user
        pet.save()
        name, pet_type = pet_form.cleaned_data.get('name'), pet_form.cleaned_data.get('pet_type')
        messages.success(request, '<i class="fas fa-check"></i> Successfully saved your gorgeous %s - %s!' % (pet_type, name))
    elif user_update_form.is_valid():
        data = user_update_form.cleaned_data
        request.user.first_name = data['first_name']
        request.user.last_name = data['last_name']
        request.user.email = data['email']
        request.user.save()
        messages.success(request, '<i class="fas fa-check"></i> Your data is updated.')
    return render(request, 'pet_app/profile.html', {
        'pets': user_pets(request),
        'pet_form': PetForm(),
        'user_form': UserUpdateForm(request.user),
    })
