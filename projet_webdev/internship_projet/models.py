from django.db import models
from django.utils import timezone

class Offre(models.Model):
    # Choix pour l'état de l'offre défini dans le PDF
    ETAT_CHOICES = [
        ('En attente', 'En attente validation'),
        ('Validée', 'Validée'),
        ('Refusée', 'Refusée'),
        ('Clôturée', 'Clôturée'),
    ]

    IDOffre = models.AutoField(primary_key=True)
    
    # Informations de l'entreprise (dépôt sans compte utilisateur)
    Organisme = models.CharField(max_length=100, verbose_name="Nom de l'organisme")
    NomContact = models.CharField(max_length=100, verbose_name="Nom et prénom du contact")
    EmailContact = models.EmailField(verbose_name="Email du contact")
    
    # Détails du stage
    Titre = models.CharField(max_length=100, verbose_name="Titre du stage")
    Detail = models.TextField(verbose_name="Détail du stage")
    
    # Gestion des dates et états
    DateDepot = models.DateTimeField(default=timezone.now, verbose_name="Date de dépôt")
    Etat = models.CharField(max_length=30, choices=ETAT_CHOICES, default='En attente')

    def __str__(self):
        return f"{self.Titre} ({self.Organisme})"