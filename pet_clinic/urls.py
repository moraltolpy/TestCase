from django.contrib import admin
from django.contrib.auth import views as session_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', session_views.LoginView.as_view(template_name='pet_app/login.html'), name='login'),
    path('logout/', session_views.LogoutView.as_view(), name='logout'),
    path('', include('pet_app.urls'))
]
