import arrow
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django import forms

from pet_app.models import Vet, Pet
from pet_app.helpers import available_range


class VisitForm(forms.Form):

    vet = forms.CharField(widget=forms.Select(choices=[]))
    pet = forms.CharField(widget=forms.Select(choices=[]))
    visit_date = forms.DateField(widget=DatePickerInput(options={
        'daysOfWeekDisabled': [0, 6],
        'useCurrent': False,
    }))
    visit_time = forms.TimeField(widget=TimePickerInput(options={
        'useCurrent': False,
        'enabledHours': list(range(8, 18)),
        'widgetPositioning': {'vertical': 'bottom'},
        'stepping': 10,
        'showTodayButton': False,
    }))

    def __init__(self, vet_id=None, pet_id=None, owner=None, visit_date=None, data=None):
        super(VisitForm, self).__init__(data=data)
        self.fields['pet'].widget.choices = [(pet.id, pet.name) for pet in Pet.objects.filter(owner=owner)]
        self.fields['pet'].disabled = len(self.fields['pet'].widget.choices) == 1
        self.initial['pet'] = Pet.objects.get(id=pet_id).id

        self.fields['vet'].widget.choices = [(vet.id, vet.name) for vet in Vet.objects.all()]
        if Vet.objects.count() > 2:
            self.initial['vet'] = Vet.objects.exclude(id=vet_id).order_by("?").first().id
        else:
            self.initial['vet'] = Vet.objects.get(id=vet_id).id

        if visit_date:
            self.initial['visit_date'] = visit_date
            self.initial['visit_time'] = visit_date

            self.fields['pet'].disabled = True
        else:
            now = arrow.utcnow()
            now = now.shift(days=1) if now.weekday() in list(range(0, 4)) else now.shift(weekday=0)
            _, available_ranges = available_range(now.datetime, vet_id)
            self.initial['visit_date'] = now.datetime
            self.initial['visit_time'] = available_ranges[0]['start']

    def clean_visit_date(self):
        data = self.cleaned_data['visit_date']
        date = arrow.get(data.year, data.month, data.day).datetime

        return data

    def clean_visit_time(self):
        data = self.cleaned_data['visit_time']

        if data.hour >= 19:
            raise forms.ValidationError('Only working hours (8.00 - 18.00) are allowed!')
        return data

    def clean(self):
        cleaned_data = super().clean()
        time = cleaned_data.get('visit_time')
        date = cleaned_data.get('visit_date')
        if not time or not date:
            return
        date = arrow.get(date.year, date.month, date.day, time.hour, time.minute).datetime
        if date < arrow.utcnow().datetime:
            raise forms.ValidationError('Cannot book a visit in the past.')
