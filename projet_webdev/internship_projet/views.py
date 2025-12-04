from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Offre
from .forms import OffreCreationForm, OffreModificationForm # Assure-toi d'avoir ces forms

# --- Tests de Rôles ---
def is_prof_or_admin(user):
    return user.is_superuser or user.groups.filter(name='Profs').exists()

# --- VUES ---

# 1. DÉPÔT D'OFFRE (PUBLIC - Pas de login requis)
def creer_offre(request):
    if request.method == 'POST':
        form = OffreCreationForm(request.POST)
        if form.is_valid():
            form.save() # On sauvegarde directement (Etat = "En attente" par défaut)
            return render(request, 'internship_projet/confirmation_creation.html')
    else:
        form = OffreCreationForm()
    return render(request, 'internship_projet/formulaire_creation_offre.html', {'form': form})


# 2. LISTE DES OFFRES (LOGIN REQUIS)
@login_required
def liste_offres(request):
    search_query = request.GET.get('query')
    
    # Logique de filtrage selon le rôle
    if is_prof_or_admin(request.user):
        # Le Prof voit TOUT (pour pouvoir valider les "En attente")
        lesOffres = Offre.objects.all().order_by('-DateDepot')
    else:
        # L'Étudiant ne voit que les VALIDÉES
        lesOffres = Offre.objects.filter(Etat='Validée').order_by('-DateDepot')

    # Barre de recherche (filtre commun)
    if search_query:
        lesOffres = lesOffres.filter(Titre__icontains=search_query)

    return render(request, 'internship_projet/liste_offres.html', {
        'offres': lesOffres,
        'search_query': search_query,
        'is_prof': is_prof_or_admin(request.user) # Pour afficher les boutons d'édition dans le template
    })


# 3. MODIFICATION (RÉSERVÉ PROFS/ADMIN)
@login_required
@user_passes_test(is_prof_or_admin) # Bloque l'accès si pas prof
def modifier_offre(request, offre_id):
    offre = get_object_or_404(Offre, IDOffre=offre_id)
    
    if request.method == 'POST':
        # Utiliser un formulaire qui inclut le champ 'Etat'
        form = OffreModificationForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            return redirect('liste_offres')
    else:
        form = OffreModificationForm(instance=offre)

    return render(request, 'internship_projet/formulaire_modification_offre.html', {'form': form, 'offre': offre})


# 4. DÉTAIL (LOGIN REQUIS)
@login_required
def detail_offre(request, offre_id):
    offre = get_object_or_404(Offre, IDOffre=offre_id)
    return render(request, 'internship_projet/detail_offre.html', {
        'offre': offre,
        'is_prof': is_prof_or_admin(request.user)
    })

# 5. SUPPRESSION (RÉSERVÉ PROFS/ADMIN)
@login_required
@user_passes_test(is_prof_or_admin)
def supprimer_offre(request, offre_id):
    offre = get_object_or_404(Offre, IDOffre=offre_id)
    offre.delete()
    return redirect('liste_offres')