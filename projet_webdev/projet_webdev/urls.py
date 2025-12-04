"""
URL configuration for projet_webdev project.

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
from django.views.generic import RedirectView  # Import nécessaire

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Redirection de la racine (/) vers /comptes/login/
    path('', RedirectView.as_view(url='/comptes/login/', permanent=False)),

    # Vos autres inclusions d'URL
    path('offres/', include('internship_projet.urls')), # On déplace l'app étudiant vers /offres/
    path('comptes/', include('internship_projet_comptes.urls')),
    path('profs/', include('internship_projet_gestion_profs.urls')),
]