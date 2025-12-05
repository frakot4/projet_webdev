from django.urls import path
from . import views

urlpatterns = [
    # L'URL racine ici correspond déjà à /offres/ (grâce au include du projet principal)
    path('', views.liste_offres, name='liste_offres'), 
    
    # On enlève 'offres/' ici car il est déjà inclus avant. 
    # Cela donnera : /offres/9/
    path('<int:offre_id>/', views.detail_offre, name='detail_offre'),
    
    # Cela donnera : /offres/create/
    path('create/', views.creer_offre, name='creer_offre'),

    path('admin-stats/', views.admin_stats_dashboard, name='admin_stats'),
]