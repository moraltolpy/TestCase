import arrow
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from pet_app.views.helper import delegate
from pet_app.forms.visit_forms import VisitForm
from pet_app.models import Visit, Pet, Vet
from pet_app.helpers import available_range


@login_required
def choose_action(request):
    return delegate(
        request,
        get=redirect_to_vets,
    )


@login_required
def choose_new_action_id(request, vet_id=None, pet_id=None):
    return delegate(
        request,
        vet_id=vet_id,
        pet_id=pet_id,
        get=get,
        post=post,
    )


@login_required
def choose_update_action_id(request, visit_id=None):
    return delegate(
        request,
        visit_id=visit_id,
        get=get_update,
        post=update_visit,
    )


def update_visit(request, visit_id=None):
    visit = Visit.objects.get(id=visit_id)
    form = VisitForm(data=request.POST, vet_id=visit.vet.id, pet_id=visit.pet.id, owner=request.user, visit_date=visit.visit_date)
    visit.delete()
    return _save_visit(request, form)


def get_update(request, visit_id=None):
    visit = Visit.objects.get(id=visit_id)
    form = VisitForm(vet_id=visit.vet.id, pet_id=visit.pet.id, owner=request.user, visit_date=visit.visit_date)
    messages.success(request, '<i class="fas fa-info-circle"></i> Here you can change visit details.')
    return render(request, 'pet_app/visit_form.html', {'form': form, 'is_update': True})


def get(request, vet_id=None, pet_id=None):
    form = VisitForm(vet_id=vet_id, pet_id=pet_id, owner=request.user)
    return render(request, 'pet_app/visit_form.html', {'form': form})


def post(request, vet_id=None, pet_id=None):
    form = VisitForm(data=request.POST, vet_id=vet_id, pet_id=pet_id, owner=request.user)
    return _save_visit(request, form)


def redirect_to_vets(request):
    return redirect('vet_view')


def _save_visit(request, form, redirect_to='vet_view'):
    if form.is_valid():
        data = form.cleaned_data
        visit_date, visit_time = data['visit_date'], data['visit_time']
        arrow_date = arrow.get(visit_date.year, visit_date.month, visit_date.day, visit_time.hour, visit_time.minute)
        pet = Pet.objects.get(id=data['pet'])
        vet = Vet.objects.get(id=data['vet'])
        if Visit.objects.filter(vet=vet, visit_date=arrow_date.datetime).count():
            available, _ = available_range(visit_date, vet)
            messages.warning(request, '<i class="fas fa-exclamation-circle"></i> %s already has a visit at this time. %s' % (vet.name, available))
            return render(request, 'pet_app/visit_form.html', {'form': form})
        else:
            Visit.objects.create(
                pet=pet,
                vet=vet,
                visit_date=arrow_date.datetime
            )
            messages.success(request, '<i class="fas fa-check"></i> Registered %s to visit %s %s.' %
                (pet.name, vet.name, arrow_date.humanize()))
            return redirect(redirect_to)
    return render(request, 'pet_app/visit_form.html', {'form': form})
