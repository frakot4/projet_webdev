from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # <-- Importe les vues du dossier courant (internship_projet_comptes)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='internship_projet_comptes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dispatch/', views.dispatch_login, name='dispatch_login'),
]