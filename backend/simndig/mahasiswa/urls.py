from django.urls import path
from . import views

app_name = 'mahasiswa'

urlpatterns = [
    path('', views.mahasiswa_home, name='mahasiswa_home'),
    path('lengkapi-profil/', views.complete_profile, name='complete_profile'),
    path('kelas/<int:kelas_id>/', views.detail_kelas, name='detail_kelas'),
]
