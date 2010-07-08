# -*- encoding: utf-8 -*-
import calendar
from datetime import datetime, date

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect

from forms import *
from models import *

from accounts.models import *
from budget.models import *
from kpi.models import *

from helper import utilities, permission
from helper.shortcuts import render_response, render_page_response, access_denied

#
# SECTOR #######################################################################
#

@login_required
def view_organization(request):
    master_plans = MasterPlan.objects.all().order_by('ref_no')
    sectors = Sector.objects.all().order_by('ref_no')
    return render_response(request, 'organization.html', {'sectors':sectors, 'master_plans':master_plans})

@login_required
def view_sector_overview(request, sector_id):
    sector = get_object_or_404(Sector, pk=sector_id)
    sector_master_plans = SectorMasterPlan.objects.filter(sector=sector).order_by('master_plan__ref_no')
    master_plans = [sector_master_plan.master_plan for sector_master_plan in sector_master_plans]
    
    return render_page_response(request, 'overview', 'page_sector/sector_overview.html', {'sector':sector, 'master_plans':master_plans})

def view_sector_progress(request, sector_id):
    return render_page_response(request, 'progress', 'page_sector/sector_progress.html', {'sector':sector, })

def view_sector_kpi(request, sector_id):
    return render_page_response(request, 'kpi', 'page_sector/sector_kpi.html', {'sector':sector, })

def view_sector_budget(request, sector_id):
    return render_page_response(request, 'budget', 'page_sector/sector_budget.html', {'sector':sector, })

#
# MASTER PLAN #######################################################################
#

@login_required
def view_master_plan_overview(request, master_plan_id):
    master_plan = get_object_or_404(MasterPlan, pk=master_plan_id)
    current_date = date.today()
    
    # Plans
    plans = Plan.objects.filter(master_plan=master_plan)
    for plan in plans:
        plan.current_projects = Project.objects.filter(plan=plan, start_date__lte=current_date, end_date__gte=current_date).order_by('ref_no')

    master_plan.plans = plans
    #master_plan = finance_functions.overview_master_plan_finance(master_plan)
    return render_page_response(request, 'overview', 'page_sector/master_plan_overview.html', {'master_plan': master_plan})

def view_master_plan_progress(request, master_plan_id):
    return render_page_response(request, 'progress', 'page_sector/master_plan_progress.html', {'master_plan':master_plan, })

def view_master_plan_kpi(request, master_plan_id):
    return render_page_response(request, 'kpi', 'page_sector/master_plan_kpi.html', {'master_plan':master_plan, })

def view_master_plan_budget(request, master_plan_id):
    return render_page_response(request, 'budget', 'page_sector/master_plan_budget.html', {'master_plan':master_plan, })

#
# MASTER PLAN MANAGEMENT #######################################################################
#

def view_master_plan_manage_organization(request, master_plan_id):
    master_plan = get_object_or_404(MasterPlan, pk=master_plan_id)
    
    return render_page_response(request, 'organization', 'page_sector/manage_master_plan/manage_organization.html', {'master_plan':master_plan, })

def view_master_plan_manage_kpi(request, master_plan_id):
    master_plan = get_object_or_404(MasterPlan, pk=master_plan_id)
    
    return render_page_response(request, 'kpi', 'page_sector/manage_master_plan/manage_kpi.html', {'master_plan':master_plan, })

#
# PROGRAM #######################################################################
#

@login_required
def view_program_overview(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    
    return render_page_response(request, 'overview', 'page_program/program_overview.html', {'program':program, })

@login_required
def view_program_progress(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    
    return render_page_response(request, 'progress', 'page_program/program_progress.html', {'program':program, })

@login_required
def view_program_kpi(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    
    return render_page_response(request, 'kpi', 'page_program/program_kpi.html', {'program':program, })

@login_required
def view_program_budget(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    
    return render_page_response(request, 'budget', 'page_program/program_budget.html', {'program':program, })

#
# PROJECT #######################################################################
#

@login_required
def view_project_overview(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    current_date = date.today()

    if not project.parent_project:
        current_projects = Project.objects.filter(parent_project=project, start_date__lte=current_date, end_date__gte=current_date)
        report_submissions = ReportSubmission.objects.filter(project=project).filter(Q(state=APPROVE_ACTIVITY) | (Q(state=SUBMIT_ACTIVITY) & (Q(report__need_approval=False) | Q(report__need_checkup=False)))).order_by('-schedule_date')[:5]
        return render_response(request, 'page_project/project_overview.html', {'project':project, 'current_projects':current_projects, 'report_submissions':report_submissions})

    else:
        current_activities = Activity.objects.filter(project=project, start_date__lte=current_date, end_date__gte=current_date)
        return render_response(request, 'page_project/project_overview.html', {'project':project, 'current_activities':current_activities})






