"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
from django.urls import path
from myapp import views

admin.site.site_url = settings.SITE_URL or '/'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('admin/', admin.site.urls),
    path('api/dashboard/', views.dashboard_data, name='dashboard_data'),
    path('api/control/', views.send_control_command, name='send_control_command'),
    path('api/n8n/relay-control/', views.n8n_relay_control, name='n8n_relay_control'),
    path('api/telemetry-history/', views.telemetry_history, name='telemetry_history'),
]
