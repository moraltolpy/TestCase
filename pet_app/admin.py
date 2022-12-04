from django.contrib import admin

from pet_app.models import (
    Vet,
    Pet,
    Visit,
)


class VetAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'education',)
    ordering = ('-created_at',)
    search_fields = ('id', 'name', 'education')


class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'pet_type', 'owner_id', 'vet_id')
    ordering = ('-created_at',)
    search_fields = ('id', 'name', 'owner_id')


class VisitAdmin(admin.ModelAdmin):
    list_display = ('visit_date', 'pet_id', 'vet_id')
    ordering = ('-created_at',)
    search_fields = ('id', 'name', 'owner_id', 'pet_id', 'vet_id')


admin.site.register(Vet, VetAdmin)
admin.site.register(Pet, PetAdmin)
admin.site.register(Visit, VisitAdmin)
