from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from accounts.models import UserRoleResponsibility

from helper.shortcuts import render_response

def view_homepage(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        return redirect('view_dashboard')

@login_required
def view_dashboard(request):
    if request.user.groups.all():
        primary_role = request.user.groups.all()[0] # Currently support only 1 role per user
        
        if primary_role.name == 'director':
            return _view_director_dashboard(request)
        
        elif primary_role.name == 'sector_manager':
            responsibility = UserRoleResponsibility.objects.get(user=request.user.get_profile(), role=primary_role)
            return redirect('view_sector_overview', (responsibility.sectors.all()[0].id))
        
        elif primary_role.name == 'sector_manager_assistant':
            return _view_sector_manager_assistant_homepage(request)
        
        elif primary_role.name == 'program_manager':
            return _view_program_manager_homepage(request)
        
        elif primary_role.name == 'program_manager_assistant':
            return _view_program_manager_homepage(request)
    
    if request.user.is_superuser:
        return redirect('view_administration')
    
    raise Http404

def _view_director_dashboard(request):
    return render_response(request, "page_dashboard/director_dashboard.html", {})

def _view_sector_manager_assistant_homepage(request):
    return render_response(request, "page_dashboard/sector_assistant_dashboard.html", {})

def _view_program_manager_homepage(request):
    return render_response(request, "page_dashboard/program_manager_dashboard.html", {})



