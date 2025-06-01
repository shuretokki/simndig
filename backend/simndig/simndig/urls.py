"""
URL configuration for simndig project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from authenticate import views as auth_views  # Use alias to avoid confusion
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Authentication-related views
    path('accounts/login/', auth_views.login_user, name='login'),
    path('accounts/logout/', auth_views.logout_user, name='logout'),
    path('accounts/register/', auth_views.register_user, name='register'),

    # Home redirect based on user role
    path('home/', auth_views.home_view, name='home'),

    # App-specific dashboards
    path('mahasiswa/', include('mahasiswa.urls')),
    path('dosen/', include('dosen.urls')),
    path('atmin/', include('atmin.urls')),  # Your custom admin app
    path('matakuliah/', include('matakuliah.urls')),  # Add this if available

    # Other authentication URLs (if any)
    # Keep this last to avoid conflicts
    path('', include('authenticate.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
