from django.urls import path
from . import views

urlpatterns = [
    # Accueil de l'app (Liste des offres) -> URL : /offres/
    path('', views.liste_offres, name='liste_offres'), 
    
    # Détail d'une offre -> URL : /offres/9/
    path('<int:offre_id>/', views.detail_offre, name='detail_offre'),
    
    # Action de candidature -> URL : /offres/9/candidater/
    path('<int:offre_id>/candidater/', views.candidater, name='candidater_offre'),
    
    # Création d'offre (Entreprise) -> URL : /offres/create/
    path('create/', views.creer_offre, name='creer_offre'),

    # Statistiques Admin -> URL : /offres/admin-stats/
    path('admin-stats/', views.admin_stats_dashboard, name='admin_stats'),
]