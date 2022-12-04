import datetime

from django.db import models
from django.conf import settings

from pet_app.models import BaseModel


class Pet(BaseModel):

    PET_TYPE_DOG = 'dog'
    PET_TYPE_CAT = 'cat'
    PET_TYPE_BIRD = 'bird'
    PET_TYPE_REPTILE = 'reptile'
    PET_TYPE_RODENT = 'rodent'

    VALID_PET_TYPES = (
        PET_TYPE_DOG,
        PET_TYPE_CAT,
        PET_TYPE_BIRD,
        PET_TYPE_REPTILE,
        PET_TYPE_RODENT,
    )

    PET_TYPE_CHOICES = tuple((type_of_pet, type_of_pet.title()) for type_of_pet in VALID_PET_TYPES)

    name = models.CharField(max_length=64, blank=True, null=True)
    pet_type = models.CharField(choices=PET_TYPE_CHOICES, max_length=32, default=PET_TYPE_DOG)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.DO_NOTHING)
    vet = models.ForeignKey('Vet', blank=True, null=True, on_delete=models.DO_NOTHING)

    def dict(self):
        base_dict = BaseModel.dict(self)
        base_dict.update({
            'name': self.name,
            'type': self.pet_type,
            'visits': self._get_visits(),
        })
        return base_dict

    def __str__(self):
        return '%s, %s' % (self.name, self.pet_type)

    def _get_visits(self):
        visits = self.visit_set.filter(visit_date__gt=datetime.datetime.utcnow())
        return [visit.dict() for visit in visits]
