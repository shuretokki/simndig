from django.urls import path
from . import views

app_name = 'atmin'
urlpatterns = [
    path('', views.home, name='atmin_home'),
]
