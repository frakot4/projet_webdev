from django.db import models
from django.contrib.auth.models import User

class Offre(models.Model):
    ETAT_CHOICES = [
        ('En attente', 'En attente validation'),
        ('Validée', 'Validée'),
        ('Refusée', 'Refusée'),
        ('Clôturée', 'Clôturée'),
    ]

    IDOffre = models.AutoField(primary_key=True)
    Organisme = models.CharField(max_length=100, verbose_name="Nom de l'organisme")
    NomContact = models.CharField(max_length=100, verbose_name="Nom et prénom du contact")
    EmailContact = models.EmailField(verbose_name="Email du contact")
    Titre = models.CharField(max_length=100, verbose_name="Titre du stage")
    Detail = models.TextField(verbose_name="Détail du stage")
    DateDepot = models.DateTimeField(default=timezone.now, verbose_name="Date de dépôt")
    Etat = models.CharField(max_length=30, choices=ETAT_CHOICES, default='En attente')

    def __str__(self):
        return f"{self.Titre} ({self.Organisme})"

# Ajoutez cette classe qui manquait dans votre fichier
class Candidature(models.Model):
    IDCandidature = models.AutoField(primary_key=True)
    Offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    Etudiant = models.ForeignKey(User, on_delete=models.CASCADE)
    DateCandidature = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("Offre", "Etudiant"),)