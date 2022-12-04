from django.core.management.base import BaseCommand

from pet_app.models import Vet


def seed_db():
    vets = [
        dict(
            name='Joosep Tamm',
            age=44,
            education='Tartu Maaülikool',
        ),
        dict(
            name='Madis Sade',
            age=37,
            education='Tartu Maaülikool',
        ),
        dict(
            name='Helina Kask',
            age=29,
            education='Järvamaa Kutseharidus Keskus',
        )
    ]
    for v in vets:
        Vet.objects.create(name=v['name'], age=v['age'], education=v['education'])


class Command(BaseCommand):
    def handle(self, **options):
        seed_db()
