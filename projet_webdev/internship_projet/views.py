from django.shortcuts import render, get_object_or_404, redirect
from internship_projet.models import Offre
from internship_projet.forms import OffreCreationForm, OffreModificationForm

# READ (Liste) - Accessible aux étudiants/responsables
def liste_offres(request):
    # On récupère toutes les offres
    lesOffres = Offre.objects.all().order_by('-DateDepot')
    return render(request, 'internship_projet/liste_offres.html', {'offres': lesOffres})

# READ (Détail)
def detail_offre(request, offre_id):
    lOffre = get_object_or_404(Offre, IDOffre=offre_id)
    return render(request, 'internship_projet/detail_offre.html', {'offre': lOffre})

# CREATE - Accessible aux entreprises (pas de login requis selon PDF)
def creer_offre(request):
    form = OffreCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        # Redirection vers une page de confirmation ou la liste
        return render(request, 'internship_projet/confirmation_creation.html')
    
    return render(request, 'internship_projet/formulaire_creation_offre.html', {'form': form})

# UPDATE - Accessible aux responsables (devrait être protégé par @login_required)
def modifier_offre(request, offre_id):
    offre_a_modifier = get_object_or_404(Offre, IDOffre=offre_id)
    
    if request.method == 'POST':
        form = OffreModificationForm(request.POST, instance=offre_a_modifier)
        if form.is_valid():
            form.save()
            return redirect('/offres/') # Retour à la liste
    else:
        form = OffreModificationForm(instance=offre_a_modifier)

    return render(request, 'internship_projet/formulaire_modification_offre.html', 
                  {'form': form, 'offre': offre_a_modifier})

# DELETE - Accessible aux responsables/admin
def supprimer_offre(request, offre_id):
    offre = get_object_or_404(Offre, IDOffre=offre_id)
    offre.delete()
    return redirect('/offres/')