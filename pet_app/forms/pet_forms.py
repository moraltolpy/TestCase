from django.forms import ModelForm, CharField, TextInput

from pet_app.models import Pet


class PetForm(ModelForm):
    name = CharField(required=True, widget=TextInput(attrs={
        'title': 'Only characters are allowed',
    }))

    class Meta:
        model = Pet
        fields = ['name', 'pet_type']
