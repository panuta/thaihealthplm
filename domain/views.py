# -*- encoding: utf-8 -*-
import calendar
from datetime import datetime, date

from django.conf import settings
from django.contrib import messages
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
def view_sector_overview(request, sector_ref_no):
    sector = get_object_or_404(Sector, ref_no=sector_ref_no)
    sector_master_plans = SectorMasterPlan.objects.filter(sector=sector).order_by('master_plan__ref_no')
    master_plans = [sector_master_plan.master_plan for sector_master_plan in sector_master_plans]
    
    return render_page_response(request, 'overview', 'page_sector/sector_overview.html', {'sector':sector, 'master_plans':master_plans})

def view_sector_progress(request, sector_ref_no):
    sector = get_object_or_404(Sector, ref_no=sector_ref_no)
    return render_page_response(request, 'progress', 'page_sector/sector_progress.html', {'sector':sector, })

def view_sector_kpi(request, sector_ref_no):
    sector = get_object_or_404(Sector, ref_no=sector_ref_no)
    return render_page_response(request, 'kpi', 'page_sector/sector_kpi.html', {'sector':sector, })

def view_sector_budget(request, sector_ref_no):
    sector = get_object_or_404(Sector, ref_no=sector_ref_no)
    return render_page_response(request, 'budget', 'page_sector/sector_budget.html', {'sector':sector, })

#
# MASTER PLAN #######################################################################
#

@login_required
def view_master_plan_overview(request, master_plan_ref_no):
    master_plan = get_object_or_404(MasterPlan, ref_no=master_plan_ref_no)
    current_date = date.today()
    
    # Plans
    plans = Plan.objects.filter(master_plan=master_plan)
    for plan in plans:
        plan.current_projects = Project.objects.filter(plan=plan, start_date__lte=current_date, end_date__gte=current_date).order_by('ref_no')

    master_plan.plans = plans
    #master_plan = finance_functions.overview_master_plan_finance(master_plan)
    return render_page_response(request, 'overview', 'page_sector/master_plan_overview.html', {'master_plan': master_plan})

def view_master_plan_progress(request, master_plan_ref_no):
    master_plan = get_object_or_404(MasterPlan, ref_no=master_plan_ref_no)
    return render_page_response(request, 'progress', 'page_sector/master_plan_progress.html', {'master_plan':master_plan, })

def view_master_plan_kpi(request, master_plan_ref_no):
    master_plan = get_object_or_404(MasterPlan, ref_no=master_plan_ref_no)
    return render_page_response(request, 'kpi', 'page_sector/master_plan_kpi.html', {'master_plan':master_plan, })

def view_master_plan_budget(request, master_plan_ref_no):
    master_plan = get_object_or_404(MasterPlan, ref_no=master_plan_ref_no)
    return render_page_response(request, 'budget', 'page_sector/master_plan_budget.html', {'master_plan':master_plan, })

#
# MASTER PLAN MANAGEMENT #######################################################################
#

def view_master_plan_manage_organization(request, master_plan_ref_no):
    master_plan = get_object_or_404(MasterPlan, ref_no=master_plan_ref_no)
    
    if not permission.access_obj(request.user, 'master_plan manage', master_plan):
        return access_denied(request)
    
    current_date = date.today().replace(day=1)
    plans = Plan.objects.filter(master_plan=master_plan).order_by('ref_no')
    
    for plan in plans:
        plan.programs = Program.objects.filter(plan=plan).order_by('ref_no')
        for program in plan.programs:
            program.removable = Project.objects.filter(program=program).count() == 0
    
    return render_page_response(request, 'organization', 'page_sector/manage_master_plan/manage_organization.html', {'master_plan':master_plan, 'plans':plans})

def view_master_plan_add_plan(request, master_plan_ref_no):
    master_plan = get_object_or_404(MasterPlan, ref_no=master_plan_ref_no)
    
    if not permission.access_obj(request.user, 'master_plan manage', master_plan):
        return access_denied(request)
    
    if request.method == 'POST':
        form = ModifyPlanForm(request.POST, master_plan=master_plan)
        if form.is_valid():
            plan = Plan.objects.create(ref_no=form.cleaned_data['ref_no'], name=form.cleaned_data['name'], master_plan=master_plan)
            
            messages.success(request, 'เพิ่มกลุ่มแผนงานเรียบร้อย')
            return redirect('view_master_plan_manage_organization', (master_plan.ref_no))
            
    else:
        form = ModifyPlanForm(master_plan=master_plan)
    
    return render_page_response(request, 'organization', 'page_sector/manage_master_plan/manage_modify_plan.html', {'master_plan':master_plan, 'form':form})

def view_master_plan_edit_plan(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)
    master_plan = plan.master_plan
    
    if not permission.access_obj(request.user, 'master_plan manage', master_plan):
        return access_denied(request)
    
    if request.method == 'POST':
        form = ModifyPlanForm(request.POST, master_plan=master_plan)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            plan.ref_no = cleaned_data['ref_no']
            plan.name = cleaned_data['name']
            plan.save()
            
            messages.success(request, 'แก้ไขกลุ่มแผนงานเรียบร้อย')
            return redirect('view_master_plan_manage_organization', (master_plan.ref_no))
    else:
        form = ModifyPlanForm(master_plan=master_plan, initial={'plan_id':plan.id, 'ref_no':plan.ref_no, 'name':plan.name})
    
    return render_page_response(request, 'organization', 'page_sector/manage_master_plan/manage_modify_plan.html', {'master_plan':master_plan, 'plan':plan, 'form':form})

def view_master_plan_delete_plan(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)
    master_plan = plan.master_plan
    
    if not permission.access_obj(request.user, 'master_plan manage', master_plan):
        return access_denied(request)
    
    if not Program.objects.filter(plan=plan).count():
        plan.delete()
        messages.success(request, 'ลบกลุ่มแผนงานเรียบร้อย')
    else:
        messages.error(request, 'ไม่สามารถลบกลุ่มแผนงานได้ เนื่องจากมีแผนงานที่อยู่ภายใต้')
    
    return redirect('view_master_plan_manage_organization', (master_plan.ref_no))

@login_required
def view_master_plan_add_program(request, master_plan_ref_no):
    master_plan = get_object_or_404(MasterPlan, ref_no=master_plan_ref_no)
    
    if not permission.access_obj(request.user, 'master_plan manage', master_plan):
        return access_denied(request)
    
    if Plan.objects.filter(master_plan=master_plan).count() == 0:
        messages.error(request, 'กรุณาสร้างกลุ่มแผนงานก่อนการสร้างแผนงาน')
        return redirect('view_master_plan_manage_organization', (master_plan.ref_no))
    
    if request.method == 'POST':
        form = MasterPlanProgramForm(request.POST, master_plan=master_plan)
        if form.is_valid():
            program = Program.objects.create(
                plan=form.cleaned_data['plan'],
                ref_no=form.cleaned_data['ref_no'],
                name=form.cleaned_data['name'],
                start_date=form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date'],
                )
            
            messages.success(request, u'เพิ่มแผนงาน/โครงการเรียบร้อย')
            return redirect('view_master_plan_manage_organization', (master_plan.id))
        
    else:
        form = MasterPlanProgramForm(master_plan=master_plan)
    
    return render_page_response(request, 'organization', 'page_sector/manage_master_plan/manage_modify_program.html', {'master_plan':master_plan, 'form':form})

@login_required
def view_master_plan_edit_program(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    master_plan = program.plan.master_plan
    
    if not permission.access_obj(request.user, 'master_plan manage', master_plan):
        return access_denied(request)
    
    if request.method == 'POST':
        form = MasterPlanProgramForm(request.POST, master_plan=master_plan)
        if form.is_valid():
            program.plan = form.cleaned_data['plan']
            program.ref_no = form.cleaned_data['ref_no']
            program.name = form.cleaned_data['name']
            program.start_date = form.cleaned_data['start_date']
            program.end_date = form.cleaned_data['end_date']
            program.save()
            
            messages.success(request, u'แก้ไขแผนงาน/โครงการเรียบร้อย')
            return redirect('view_master_plan_manage_organization', (master_plan.id))
        
    else:
        form = MasterPlanProgramForm(master_plan=master_plan, initial={'program_id':program.id, 'plan':program.plan.id, 'ref_no':program.ref_no, 'name':program.name, 'description':program.description, 'start_date':program.start_date, 'end_date':program.end_date})
    
    return render_page_response(request, 'organization', 'page_sector/manage_master_plan/manage_modify_program.html', {'master_plan':master_plan, 'program':program, 'form':form})

@login_required
def view_master_plan_delete_program(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    master_plan = program.plan.master_plan

    if not permission.access_obj(request.user, 'master_plan manage', master_plan):
        return access_denied(request)
    
    if Project.objects.filter(program=program).count():
        messages.error(request, u'ไม่สามารถลบแผนงาน/โครงการได้ เนื่องจากยังมีโครงการที่อยู่ภายใต้')
    else:
        schedules = ProgramBudgetSchedule.objects.filter(program=program)
        ProgramBudgetScheduleRevision.objects.filter(schedule__in=schedules).delete()
        schedules.delete()
        
        # TODO: Delete KPI Schedule
        
        program.delete()
        messages.success(request, u'ลบแผนงาน/โครงการเรียบร้อย')
    
    return redirect('view_master_plan_manage_organization', (master_plan.id))

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






