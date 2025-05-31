from django.urls import path
from . import views

app_name = 'dosen'

urlpatterns = [
    path('', views.dosen_home, name='dosen_home'),
    path('lengkapi-profil/', views.complete_profile, name='complete_profile'),
    path('kelas/<int:kelas_id>/', views.detail_kelas, name='detail_kelas'),
]
