from django.urls import path
from . import views

app_name = 'dosen'
urlpatterns = [
    path('', views.home, name='dosen_home'),
]