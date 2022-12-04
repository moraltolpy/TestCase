from pet_app.models import BaseModel

from django.db import models


class Vet(BaseModel):

    name = models.CharField(max_length=128, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    education = models.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super(Vet, self).__init__(*args, **kwargs)

    def dict(self):
        base_dict = BaseModel.dict(self)
        base_dict.update({
            'name': self.name,
            'age': self.age,
            'education': self.education,
        })
        return base_dict

    def __str__(self):
        return '%s' % self.name
