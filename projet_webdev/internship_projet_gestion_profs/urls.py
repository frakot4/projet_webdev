from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_profs, name='dashboard_profs'),
    path('offre/<int:offre_id>/edit/', views.valider_offre, name='valider_offre'),
    path('offre/<int:offre_id>/delete/', views.supprimer_offre_prof, name='supprimer_offre_prof'),
]