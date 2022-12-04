from django.shortcuts import render

from pet_app.views.helper import delegate, user_pets
from pet_app.models import Vet


def choose_action(request):
    return delegate(
        request,
        get=get,
    )


def get(request):
    return render(request, 'pet_app/vets.html', {'vets': get_vets_dict(), 'user_pets': user_pets(request)})


def get_vets_dict():
    return [vet.dict() for vet in Vet.objects.all()[0::2]]
