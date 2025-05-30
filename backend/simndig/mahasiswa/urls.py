from django.urls import path
from . import views

app_name = 'mahasiswa'
urlpatterns = [
    path('', views.home, name='mahasiswa_home'),
]
