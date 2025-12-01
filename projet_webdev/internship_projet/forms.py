# internship_projet/forms.py

from django import forms
from django.forms import ModelForm
from internship_projet.models import Offre

class OffreCreationForm(ModelForm):
    class Meta:
        model = Offre
        fields = ['Organisme', 'NomContact', 'EmailContact', 'Titre', 'Detail']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajout automatique de la classe Bootstrap
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': self.fields[field].label})

# Faites de même pour OffreModificationForm
class OffreModificationForm(ModelForm):
    class Meta:
        model = Offre
        fields = ['Organisme', 'NomContact', 'EmailContact', 'Titre', 'Detail', 'Etat']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})