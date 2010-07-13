# Create your views here.

def view_master_plan_program_kpi(request):
    program = get_object_or_404(Program, pk=program_id)
    master_plan = program.plan.master_plan
    
    
    
    
    return render_page_response(request, 'organization', 'page_sector/manage_master_plan/manage_kpi.html', {'master_plan':master_plan, })


def view_master_plan_manage_kpi(request, master_plan_ref_no):
    master_plan = get_object_or_404(MasterPlan, ref_no=master_plan_ref_no)
    
    return render_page_response(request, 'kpi', 'page_sector/manage_master_plan/manage_kpi.html', {'master_plan':master_plan, })
