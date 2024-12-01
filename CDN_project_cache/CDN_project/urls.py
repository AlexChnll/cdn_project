"""
URL configuration for CDN_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from CDN_app import views
from django.http import HttpResponse

urlpatterns = [
    path('', views.index, name='index'),
    path('get_image/<str:image_name>', views.get_image, name='get_image'),
    path('favicon.ico', lambda request: HttpResponse(status=204)),  # Répond avec un statut vide
]