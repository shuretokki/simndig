from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_mahasiswa, name='home_mahasiswa'),
]
