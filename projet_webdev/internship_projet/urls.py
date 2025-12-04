from django.urls import path
from . import views

urlpatterns = [
    # Redirection racine vers la liste
    path('', views.liste_offres, name='liste_offres'), 
    
    # Vue Étudiant : Liste des offres
    path('offres/', views.liste_offres, name='liste_offres_alt'),
    
    # Vue Étudiant : Détail d'une offre
    path('offres/<int:offre_id>/', views.detail_offre, name='detail_offre'),
    
    # Vue Entreprise : Création d'offre
    path('offres/create/', views.creer_offre, name='creer_offre'),
    
    # SUPPRIMEZ ou COMMENTEZ les lignes suivantes car elles sont maintenant gérées par 'gestion_profs' :
    # path('offres/<int:offre_id>/update/', views.modifier_offre, name='modifier_offre'),
    # path('offres/<int:offre_id>/delete/', views.supprimer_offre, name='supprimer_offre'),
]