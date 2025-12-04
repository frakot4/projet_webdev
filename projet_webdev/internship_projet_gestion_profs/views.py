from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from internship_projet.models import Offre
from internship_projet.forms import OffreModificationForm # Import depuis l'autre app

# Test de sécurité : Doit être dans le groupe 'Profs'
def is_prof(user):
    return user.groups.filter(name='Profs').exists()

@login_required
@user_passes_test(is_prof)
def dashboard_profs(request):
    # Le prof voit TOUT, trié par les plus récentes
    lesOffres = Offre.objects.all().order_by('-DateDepot')
    return render(request, 'gestion_profs/dashboard.html', {'offres': lesOffres})

@login_required
@user_passes_test(is_prof)
def valider_offre(request, offre_id):
    offre = get_object_or_404(Offre, IDOffre=offre_id)
    if request.method == 'POST':
        form = OffreModificationForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            return redirect('dashboard_profs')
    else:
        form = OffreModificationForm(instance=offre)
    
    return render(request, 'gestion_profs/editer_offre.html', {'form': form, 'offre': offre})

@login_required
@user_passes_test(is_prof)
def supprimer_offre_prof(request, offre_id):
    offre = get_object_or_404(Offre, IDOffre=offre_id)
    offre.delete()
    return redirect('dashboard_profs')