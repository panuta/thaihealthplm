# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from domain.models import MasterPlan, Project

from helper.shortcuts import render_response, render_page_response, access_denied

@login_required
def view_sector_progress(request, sector_ref_no):
    sector = get_object_or_404(Sector, ref_no=sector_ref_no)
    return render_page_response(request, 'progress', 'page_sector/sector_progress.html', {'sector':sector, })

@login_required
def view_master_plan_progress(request, master_plan_ref_no):
    master_plan = get_object_or_404(MasterPlan, ref_no=master_plan_ref_no)
    return render_page_response(request, 'progress', 'page_sector/master_plan_progress.html', {'master_plan':master_plan, })

@login_required
def view_program_progress(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    return render_page_response(request, 'progress', 'page_program/program_progress.html', {'program':program, })

@login_required
def view_project_progress(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.plan:
        project.parent = project.plan
    elif project.program:
        project.parent = project.program
    return render_page_response(request, 'progress', 'page_program/project_progress.html', {'project': project})

@login_required
def view_project_document(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.plan:
        project.parent = project.plan
    elif project.program:
        project.parent = project.program
    return render_page_response(request, 'document', 'page_program/project_document.html', {'project': project})
