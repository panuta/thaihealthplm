# -*- encoding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect

from domain.models import MasterPlan, Project, Activity
from progress.models import ActivityProgress, ActivityDocument

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
    if request.method == 'POST':
        try:
            project_progress = ProjectProgress.objects.get(project=project)
            project_progress.manual_progress = 0
            project_progress.current_situation = ''
            project_progress.quality = 0
            project_progress.save()
        except ObjectDoesNotExist:
            project_progress = ProjectProgress(project=project,
                                               manual_progress=0,
                                               current_situation='',
                                               quality=0)
            project_progress.save()

    ctx = {'project': project}

    return render_page_response(request, 'progress', 'page_program/project_progress.html', ctx)

@login_required
def view_project_document(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render_page_response(request, 'document', 'page_program/project_document.html', {'project': project})

#
# ACTIVITY #######################################################################
#

@login_required
def view_activity_progress(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if request.method == 'POST':
        activity_progress = request.POST['activity_progress']
        if activity_progress == 'COMPLETED':
            progress = 100
        elif activity_progress == 'ON_PROGRESS':
            progress = request.POST['activity_progress_on_progress_percentage']
            if not progress.isdigit():
                progress = 0
        else:
            progress = 0

        current_situation = request.POST['activity_progress_current_situation']
        summary = request.POST['activity_progress_summary']
        detail = request.POST['activity_progress_detail']

        try:
            activity_progress = ActivityProgress.objects.get(activity=activity)
            activity_progress.progress = progress
            activity_progress.current_situation = current_situation
            activity_progress.summary = summary
            activity_progress.detail = detail
            activity_progress.save()
        except ObjectDoesNotExist:
            activity_progress = ActivityProgress(activity=activity,
                                                 progress=progress,
                                                 current_situation=current_situation,
                                                 summary=summary,
                                                 detail=detail)
            activity_progress.save()

        if request.FILES:
            document_name = request.FILES['activity_progress_file_attachment']
            activity_doc = ActivityDocument(activity=activity,
                                            document_name=document_name,
                                            created_by=request.user.get_profile())
            activity_doc.save()

        messages.success(request, 'The activity progress has been saved.')

        activity_docs = ActivityDocument.objects.filter(activity=activity)
        form = {'progress_percentage': activity_progress.progress,
                'current_situation': activity_progress.current_situation,
                'summary': activity_progress.summary,
                'detail': activity_progress.detail,
                'docs': activity_docs}
    else:
        try:
            activity_docs = ActivityDocument.objects.filter(activity=activity)
            activity_progress = ActivityProgress.objects.get(activity=activity)
            form = {'progress_percentage': activity_progress.progress,
                    'current_situation': activity_progress.current_situation,
                    'summary': activity_progress.summary,
                    'detail': activity_progress.detail,
                    'docs': activity_docs}
        except ObjectDoesNotExist:
            form = {'progress_percentage': 0}

    ctx = {'activity': activity, 'form': form}
    return render_response(request, 'page_program/activity_progress.html', ctx)

