from django import forms
from django.forms import ModelForm
from internship_projet.models import Offre

# Formulaire pour les entreprises (Création uniquement)
class OffreCreationForm(ModelForm):
    class Meta:
        model = Offre
        # L'entreprise ne choisit pas l'état ni la date de dépôt
        fields = ['Organisme', 'NomContact', 'EmailContact', 'Titre', 'Detail']
        labels = {
            'Organisme': "Nom de votre entreprise",
            'Detail': "Description détaillée de l'offre",
        }
        widgets = {
            'Detail': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Décrivez les missions...'}),
        }

# Formulaire pour les responsables (Modification complète)
class OffreModificationForm(ModelForm):
    class Meta:
        model = Offre
        fields = ['Organisme', 'NomContact', 'EmailContact', 'Titre', 'Detail', 'Etat']