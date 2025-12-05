from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Offre
from .forms import OffreCreationForm
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.contrib.admin.views.decorators import staff_member_required

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

# Cette vue est protégée : seul un Admin (staff) peut la voir
@staff_member_required
def admin_stats_dashboard(request):
    # 1. Nombre d'offres reçues (Total)
    total_offres = Offre.objects.count()
    
    # 2. Nombre d'offres en cours (Validée)
    offres_actives = Offre.objects.filter(Etat='Validée').count()
    
    # 3. Candidatures par mois (12 derniers mois)
    # Cela prépare les données pour le graphique
    candidatures_par_mois = (
        Candidature.objects
        .annotate(month=TruncMonth('DateCandidature'))
        .values('month')
        .annotate(count=Count('IDCandidature'))
        .order_by('month')
    )
    
    context = {
        'total_offres': total_offres,
        'offres_actives': offres_actives,
        'chart_data': candidatures_par_mois, # À passer au JS dans le template
    }
    
    return render(request, 'internship_projet/admin_stats.html', context)