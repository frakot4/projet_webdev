from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_offres, name='liste_offres'), # Accueil = liste
    path('offres/', views.liste_offres, name='liste_offres_alt'),
    path('offres/<int:offre_id>/', views.detail_offre, name='detail_offre'),
    path('offres/create/', views.creer_offre, name='creer_offre'),
    path('offres/<int:offre_id>/update/', views.modifier_offre, name='modifier_offre'),
    path('offres/<int:offre_id>/delete/', views.supprimer_offre, name='supprimer_offre'),
]