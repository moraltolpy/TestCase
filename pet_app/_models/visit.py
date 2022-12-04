from pet_app.models import BaseModel

from django.db import models


class Visit(BaseModel):

    visit_date = models.DateTimeField()
    vet = models.ForeignKey('Vet', blank=True, null=True, on_delete=models.DO_NOTHING)
    pet = models.ForeignKey('Pet', blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s\'s %s -> %s at %s' % (self.pet.owner, self.pet, self.vet, self.visit_date)

    def dict(self):
        base_dict = BaseModel.dict(self)
        base_dict.update({
            'date': self.visit_date,
            'vet': self.vet.dict(),
        })
        return base_dict
