# -*- encoding: utf-8 -*-

from datetime import date

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string

from forms import *

from accounts.models import UserAccount, UserRoleResponsibility
from domain.models import *

from helper import utilities, permission
from helper.shortcuts import render_response, render_page_response, access_denied

@login_required
def view_administration(request):
    return redirect('/administration/organization/')

@login_required
def view_administration_organization(request):
    if not request.user.is_superuser: return access_denied(request)
    
    sectors = Sector.objects.all().order_by('ref_no')
    for sector in sectors:
        sector.has_child = SectorMasterPlan.objects.filter(sector=sector).count() > 0

    master_plans = MasterPlan.objects.all().order_by('ref_no')
    for master_plan in master_plans:
        managing_sectors = SectorMasterPlan.objects.filter(master_plan=master_plan)
        
        master_plan.sectors = []
        for sector in managing_sectors:
            master_plan.sectors.append(sector.sector.ref_no)
    
    return render_page_response(request, 'organization', 'page_administration/manage_organization.html', {'sectors':sectors, 'master_plans':master_plans})

@login_required
def view_administration_organization_add_sector(request):
    if not request.user.is_superuser: return access_denied(request)

    if request.method == 'POST':
        form = ModifySectorForm(request.POST)
        if form.is_valid():
            Sector.objects.create(ref_no=form.cleaned_data['ref_no'], name=form.cleaned_data['name'])
            
            set_message(request, u'เพิ่มสำนักเรียบร้อย')
            return redirect('view_administration_organization')
    else:
        form = ModifySectorForm()

    return render_response(request, 'page_administration/administration_organization_sector_modify.html', {'form':form})

@login_required
def view_administration_organization_edit_sector(request, sector_id):
    if not request.user.is_superuser: return access_denied(request)

    sector = get_object_or_404(Sector, pk=sector_id)

    if request.method == 'POST':
        form = ModifySectorForm(request.POST)
        if form.is_valid():
            sector.ref_no = form.cleaned_data['ref_no']
            sector.name = form.cleaned_data['name']
            sector.save()

            set_message(request, u'แก้ไขสำนักเรียบร้อย')
            return redirect('view_administration_organization')

    else:
        form = ModifySectorForm(initial={'sector_id':sector.id, 'ref_no':sector.ref_no, 'name':sector.name})

    return render_response(request, 'page_administration/administration_organization_sector_modify.html', {'sector':sector, 'form':form})

@login_required
def view_administration_organization_delete_sector(request, sector_id):
    if not request.user.is_superuser: return access_denied(request)

    sector = get_object_or_404(Sector, pk=sector_id)

    if not MasterPlan.objects.filter(sector=sector).count():
        sector.delete()
        set_message(request, u'ลบสำนักเรียบร้อย')
    else:
        set_message(request, u'ไม่สามารถลบสำนัก%s ได้เนื่องจากยังมีข้อมูลแผนหลักอยู่ภายใต้' % sector.name)

    return redirect('view_administration_organization')

@login_required
def view_administration_organization_add_masterplan(request):
    if not request.user.is_superuser: return access_denied(request)

    if request.method == 'POST':
        form = ModifyMasterPlanForm(request.POST)
        if form.is_valid():
            ref_no = form.cleaned_data['ref_no']
            name = form.cleaned_data['name']
            sectors = form.cleaned_data['sectors']
            
            month_span = MonthSpan.objects.get(is_default=True)
            master_plan = MasterPlan.objects.create(ref_no=ref_no, name=name, month_span=month_span)
            
            for sector in sectors: SectorMasterPlan.objects.create(sector=sector, master_plan=master_plan)
            
            set_message(request, u'เพิ่มแผนหลักเรียบร้อย')
            return redirect('view_administration_organization')

    else:
        form = ModifyMasterPlanForm()
    
    has_sectors = Sector.objects.all().count() > 0
    return render_response(request, 'page_administration/administration_organization_masterplan_modify.html', {'form':form, 'has_sectors':has_sectors})

@login_required
def view_administration_organization_edit_masterplan(request, master_plan_id):
    if not request.user.is_superuser: return access_denied(request)

    master_plan = get_object_or_404(MasterPlan, pk=master_plan_id)

    if request.method == 'POST':
        form = ModifyMasterPlanForm(request.POST)
        if form.is_valid():
            ref_no = form.cleaned_data['ref_no']
            name = form.cleaned_data['name']
            sectors = form.cleaned_data['sectors']
            
            master_plan.ref_no = ref_no
            master_plan.name = name
            master_plan.save()
            
            SectorMasterPlan.objects.filter(master_plan=master_plan).delete()
            for sector in sectors: SectorMasterPlan.objects.create(sector=sector, master_plan=master_plan)
            
            set_message(request, u'แก้ไขแผนหลักเรียบร้อย')
            return redirect('view_administration_organization')

    else:
        form = ModifyMasterPlanForm(initial={'sectors':[sector.sector.id for sector in SectorMasterPlan.objects.filter(master_plan=master_plan)], 'master_plan_id':master_plan.id, 'ref_no':master_plan.ref_no, 'name':master_plan.name})
    
    has_sectors = Sector.objects.all().count() > 0
    return render_response(request, 'page_administration/administration_organization_masterplan_modify.html', {'master_plan':master_plan, 'form':form, 'has_sectors':has_sectors})

@login_required
def view_administration_organization_delete_masterplan(request, master_plan_id):
    if not request.user.is_superuser: return access_denied(request)

    master_plan = get_object_or_404(MasterPlan, pk=master_plan_id)

    if not Plan.objects.filter(master_plan=master_plan).count() and not Project.objects.filter(master_plan=master_plan).count():
        master_plan.delete()
        SectorMasterPlan.objects.filter(master_plan=master_plan).delete()
        
        set_message(request, u'ลบแผนหลักเรียบร้อย')
    else:
        set_message(request, u'ไม่สามารถลบแผนหลัก%s ได้เนื่องจากยังมีข้อมูลกลุ่มแผนงานหรือแผนงานอยู่ภายใต้' % master_plan.name)

    return redirect('view_administration_organization')


@login_required
def view_administration_users(request):
    if not request.user.is_superuser: return access_denied(request)
    
    users = UserAccount.objects.filter(user__is_superuser=False).order_by('sector__ref_no')
    
    for user_account in users:
        responsibilities = UserRoleResponsibility.objects.filter(user=user_account)
        
        if responsibilities:
            responsibility = responsibilities[0]
            user_account.role_name = GroupName.objects.get(group=responsibility.role).name
            
            if responsibility.role.name == 'project_manager' or responsibility.role.name == 'project_manager_assistant':
                user_account.projects = responsibility.projects.all()
        else:
            user_account.role_name = ''
    
    return render_response(request, 'page_administration/administration_users.html', {'users': users})

@login_required
def view_administration_users_add(request):
    if not request.user.is_superuser: return access_denied(request)

    if request.method == 'POST':
        form = UserAccountForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            role = form.cleaned_data['role']
            sector = form.cleaned_data['sector']
            responsible = form.cleaned_data['responsible']

            password = utilities.make_random_user_password()

            user = User.objects.create_user(username, email, password=password)
            user_account = UserAccount.objects.get(user=user)
            user_account.first_name = first_name
            user_account.last_name = last_name
            user_account.random_password = password
            user_account.sector = sector
            user_account.save()
            
            group = Group.objects.get(name=role)
            
            user.groups.add(group)
            responsibility = UserRoleResponsibility.objects.create(user=user_account, role=group)

            if role == 'project_manager' or role == 'project_manager_assistant':
                project = Project.objects.get(pk=responsible)
                responsibility.projects.add(project)
            else:
                responsibility.sectors.add(sector)
            
            email_render_dict = {'username':username, 'password':password, 'settings':settings, 'site':Site.objects.get_current()}
            email_subject = render_to_string('email/create_user_subject.txt', email_render_dict)
            email_message = render_to_string('email/create_user_message.txt', email_render_dict)
            
            send_mail(email_subject, email_message, settings.SYSTEM_NOREPLY_EMAIL, [email])
            
            return redirect('view_administration_users_password', user.id)

    else:
        form = UserAccountForm()

    if request.POST.get('responsible'):
        responsible = request.POST['responsible']
        project = Project.objects.get(pk=responsible)

        master_plans = MasterPlan.objects.all()
        projects = Project.objects.filter(master_plan=project.master_plan, parent_project=None)

        return render_response(request, 'page_administration/administration_users_modify.html', {'form': form, 'master_plans':master_plans, 'projects':projects, 'responsible':project})
    else:
        return render_response(request, 'page_administration/administration_users_modify.html', {'form': form, 'responsible':''})

@login_required
def view_administration_users_edit(request, user_id):
    if not request.user.is_superuser: return access_denied(request)
    
    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        form = UserAccountForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            role = form.cleaned_data['role']
            sector = form.cleaned_data['sector']
            responsible = form.cleaned_data['responsible']

            user.username = username
            user.email = email
            user.save()

            user_account = UserAccount.objects.get(user=user)
            user_account.first_name = first_name
            user_account.last_name = last_name
            user_account.sector = sector
            user_account.save()
            
            group = Group.objects.get(name=role)
            user.groups.clear()
            user.groups.add(group)
            
            UserRoleResponsibility.objects.filter(user=user_account).delete()
            responsibility = UserRoleResponsibility.objects.create(user=user_account, role=group)
            
            if role == 'project_manager' or role == 'project_manager_assistant':
                project = Project.objects.get(pk=responsible)
                responsibility.projects.clear()
                responsibility.projects.add(project)
            else:
                responsibility.sectors.clear()
                responsibility.sectors.add(sector)
            
            set_message(request, u'แก้ไขข้อมูลผู้ใช้เรียบร้อย')
            return redirect('view_administration_users')

        else:
            if request.POST.get('responsible'):
                responsible = request.POST['responsible']
                project = Project.objects.get(pk=responsible)

                master_plans = MasterPlan.objects.all()
                projects = Project.objects.filter(master_plan=project.master_plan, parent_project=None)
            else:
                project = None
                master_plans = None
                projects = None

    else:
        role = user.groups.all()[0].name
        if role == 'project_manager' or role == 'project_manager_assistant':
            responsible = UserRoleResponsibility.objects.filter(user=user.get_profile())[0].projects.all()[0].id
        else:
            responsible = None

        form = UserAccountForm(initial={
            'username':user.username,
            'email':user.email,
            'first_name':user.get_profile().first_name,
            'last_name':user.get_profile().last_name,
            'role':role,
            'sector':user.get_profile().sector.id,
            'responsible':responsible});

        if responsible:
            project = Project.objects.get(pk=responsible)
            master_plans = MasterPlan.objects.all()
            projects = Project.objects.filter(master_plan=project.master_plan, parent_project=None)
        else:
            project = None
            master_plans = None
            projects = None

    return render_response(request, 'page_administration/administration_users_modify.html', {'editing_user':user, 'form': form, 'master_plans':master_plans, 'projects':projects, 'responsible':project})

@login_required
def view_administration_users_password(request, user_id):
    if not request.user.is_superuser: return access_denied(request)

    user = User.objects.get(pk=user_id)
    new_user_account = UserAccount.objects.get(user=user)

    return render_response(request, 'page_administrationistration/administration_users_password.html', {'new_user_account': new_user_account})

@login_required
def view_administration_users_change_password(request, user_id):
    if not request.user.is_superuser: return access_denied(request)
    user = User.objects.get(pk=user_id)
    
    if request.method == 'POST':
        form = UserChangePasswordForm(request.POST)
        if form.is_valid():
            print form.cleaned_data['password1']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            set_message(request, u'ตั้งรหัสผ่านใหม่เรียบร้อย')
            return redirect('view_administration_users_edit', (user.id))
        
    else:
        form = UserChangePasswordForm()
    
    return render_response(request, 'page_administration/administration_users_change_password.html', {'editing_user': user, 'form':form})


