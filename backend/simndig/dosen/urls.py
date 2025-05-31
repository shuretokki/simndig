from django.urls import path
from . import views

app_name = 'dosen'
urlpatterns = [
    path('', views.home, name='dosen_home'),
    path('kelas/<int:kelas_id>/', views.detail_kelas, name='detail_kelas')
]