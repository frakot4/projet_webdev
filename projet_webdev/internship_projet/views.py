from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Offre
from .forms import OffreCreationForm
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.contrib.admin.views.decorators import staff_member_required
from .models import Offre, Candidature 
from django.db.models import Q
from django.contrib import messages

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
    # 1. On part de la liste de base : Offres validées
    lesOffres = Offre.objects.filter(Etat='Validée').order_by('-DateDepot')
    
    # 2. Récupération du terme de recherche depuis l'URL (ex: ?q=python)
    search_query = request.GET.get('q')
    
    # 3. Filtrage si une recherche est faite
    if search_query:
        # On filtre sur le Titre OU l'Organisme (icontains = insensible à la casse)
        lesOffres = lesOffres.filter(
            Q(Titre__icontains=search_query) | 
            Q(Organisme__icontains=search_query)
        )

    # 4. On renvoie les offres ET le terme recherché (pour le réafficher dans la barre)
    return render(request, 'internship_projet/liste_offres.html', {
        'offres': lesOffres,
        'search_query': search_query
    })


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


# --- VUE STATISTIQUES (ADMIN) ---
@staff_member_required
def admin_stats_dashboard(request):
    # 1. Chiffres clés
    total_offres = Offre.objects.count()
    offres_actives = Offre.objects.filter(Etat='Validée').count()
    total_candidatures = Candidature.objects.count()
    
    # 2. Données pour le graphique (Candidatures par mois sur les 12 derniers mois)
    # Note : Si tu n'as pas encore de candidatures, ce graphique sera vide, c'est normal.
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
        'total_candidatures': total_candidatures,
        'chart_data': candidatures_par_mois,
    }
    
    return render(request, 'internship_projet/admin_stats.html', context)



# --- MODIFICATION DE LA VUE DÉTAIL ---
@login_required
def detail_offre(request, offre_id):
    offre = get_object_or_404(Offre, IDOffre=offre_id)
    
    # Vérifier si l'étudiant a déjà postulé pour afficher/masquer le bouton
    a_deja_postule = False
    if request.user.is_authenticated:
        a_deja_postule = Candidature.objects.filter(Offre=offre, Etudiant=request.user).exists()

    return render(request, 'internship_projet/detail_offre.html', {
        'offre': offre,
        'a_deja_postule': a_deja_postule
    })

# --- NOUVELLE VUE : ACTION CANDIDATER ---
@login_required
def candidater(request, offre_id):
    offre = get_object_or_404(Offre, IDOffre=offre_id)
    etudiant = request.user

    # 1. Vérification : Est-ce déjà complet ?
    if offre.NbCandidats >= 5:
        messages.error(request, "Désolé, cette offre a déjà atteint le quota de 5 candidats.")
        return redirect('detail_offre', offre_id=offre.IDOffre)

    # 2. Vérification : A-t-il déjà postulé ?
    if Candidature.objects.filter(Offre=offre, Etudiant=etudiant).exists():
        messages.warning(request, "Vous avez déjà candidaté à cette offre.")
        return redirect('detail_offre', offre_id=offre.IDOffre)

    # 3. ENREGISTREMENT (Nom étudiant + Date/Heure)
    # Note: La date est auto_now_add=True dans votre modèle Candidature
    Candidature.objects.create(Offre=offre, Etudiant=etudiant)

    # 4. INCRÉMENTATION DU COMPTEUR
    offre.NbCandidats += 1
    
    # 5. LOGIQUE MÉTIER : Si on arrive à 5, on clôture l'offre
    if offre.NbCandidats >= 5:
        offre.Etat = 'Clôturée'
    
    offre.save()

    messages.success(request, "Votre candidature a été enregistrée avec succès !")
    return redirect('liste_offres')