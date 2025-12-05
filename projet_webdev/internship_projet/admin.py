from django.contrib import admin
from .models import Offre, Candidature

# Configuration pour les Offres
class OffreAdmin(admin.ModelAdmin):
    # 1. Obtenir la liste des offres (Colonnes affichées)
    list_display = ('Titre', 'Organisme', 'NomContact', 'DateDepot', 'Etat')
    
    # 2. Faire une recherche (Barre de recherche)
    search_fields = ('Titre', 'Organisme', 'Detail')
    
    # Filtres latéraux (Bonus ergonomie)
    list_filter = ('Etat', 'DateDepot')
    
    # 3. Consulter/Modifier le détail (y compris l'état)
    # Par défaut, cliquer sur une offre ouvre le formulaire de modification
    # Le champ 'Etat' sera modifiable ici, même si "Clôturée".
    fields = ('Organisme', 'NomContact', 'EmailContact', 'Titre', 'Detail', 'Etat', 'DateDepot')

# Configuration pour les Candidatures
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ('Etudiant', 'Offre', 'DateCandidature')
    list_filter = ('DateCandidature',)
    search_fields = ('Etudiant__username', 'Offre__Titre')

# Enregistrement des modèles
admin.site.register(Offre, OffreAdmin)
admin.site.register(Candidature, CandidatureAdmin)