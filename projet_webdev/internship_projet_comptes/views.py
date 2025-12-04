from django.shortcuts import redirect

def dispatch_login(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    
    # 1. Si c'est un Admin -> Interface Admin Django
    if user.is_superuser:
        return redirect('/admin/')
        
    # 2. Si c'est un Prof -> Dashboard Profs
    if user.groups.filter(name='Profs').exists():
        return redirect('dashboard_profs')
        
    # 3. Sinon (Étudiant par défaut) -> Liste des offres
    return redirect('liste_offres')