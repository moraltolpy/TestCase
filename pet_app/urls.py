from django.urls import path
from pet_app.views import (
    index_views,
    vet_views,
    visit_views,
    auth_views,
    profile_views,
)

urlpatterns = [
    path('', index_views.index, name='app_index'),
    path('vets', vet_views.choose_action, name='vet_view'),
    path('visit', visit_views.choose_action, name='visit_view'),
    path('visit/<slug:vet_id>/<slug:pet_id>', visit_views.choose_new_action_id, name='book_visit'),
    path('visit/<slug:visit_id>', visit_views.choose_update_action_id, name='update_visit'),
    path('register', auth_views.choose_action, name='register'),
    path('profile', profile_views.choose_action, name='profile'),
]
