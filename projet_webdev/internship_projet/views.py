from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Offre
from .forms import OffreCreationForm

# --- PARTIE PUBLIQUE (Entreprises) ---
def creer_offre(request):
    if request.method == 'POST':
        form = OffreCreationForm(request.POST)
        if form.is_valid():
            form.save() # Enregistré en "En attente" par défaut
            return render(request, 'internship_projet/confirmation_creation.html')
    else:
        form = OffreCreationForm()
    return render(request, 'internship_projet/formulaire_creation_offre.html', {'form': form})

# --- PARTIE ÉTUDIANT ---
@login_required
def liste_offres(request):
    # L'étudiant ne voit QUE les offres validées
    lesOffres = Offre.objects.filter(Etat='Validée').order_by('-DateDepot')
    
    search_query = request.GET.get('query')
    if search_query:
        lesOffres = lesOffres.filter(Titre__icontains=search_query)

    return render(request, 'internship_projet/liste_offres.html', {
        'offres': lesOffres,
        'search_query': search_query
    })

@login_required
def detail_offre(request, offre_id):
    offre = get_object_or_404(Offre, IDOffre=offre_id)
    return render(request, 'internship_projet/detail_offre.html', {'offre': offre})