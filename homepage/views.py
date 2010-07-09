from django.shortcuts import redirect

def view_homepage(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    
    else:
        if request.user.is_superuser:
            return _view_admin_frontpage(request)
        else:
            primary_role = request.user.groups.all()[0] # Currently support only 1 role per user
            
            if primary_role.name == 'director':
                return _view_sector_admin_frontpage(request)
            
            elif primary_role.name == 'sector_admin':
                return _view_sector_admin_frontpage(request)
            
            elif primary_role.name == 'sector_manager':
                return _view_sector_manager_frontpage(request)
            
            elif primary_role.name == 'sector_manager_assistant':
                return _view_sector_manager_assistant_frontpage(request)
            
            elif primary_role.name == 'program_manager':
                return _view_project_manager_frontpage(request)
            
            elif primary_role.name == 'program_manager_assistant':
                return _view_project_manager_assistant_frontpage(request)
        
        raise Http404

def _view_admin_frontpage(request):
    return redirect('view_administration')