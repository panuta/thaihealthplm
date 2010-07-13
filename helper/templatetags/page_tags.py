# -*- encoding: utf-8 -*-

from django import template
register = template.Library()

from django.conf import settings
from django.core.urlresolvers import reverse

from accounts.models import UserRoleResponsibility, GroupDetails
from domain.models import SectorMasterPlan

# TEMPLATE #################################################################

@register.simple_tag
def display_header_navigation(user):
    html = ''
    
    if user.groups.all():
        primary_role = user.groups.all()[0]
        
        if primary_role.name == 'director':
            html = html + '<a href="%s"><img src="%s/images/base/nav_front.png" /> หน้าผู้จัดการกองทุน</a>' % (reverse('view_dashboard'), settings.MEDIA_URL)
        
        elif primary_role.name == 'sector_manager':
            responsibility = UserRoleResponsibility.objects.get(user=user.get_profile(), role=primary_role)
            sector = responsibility.sectors.all()[0]
            html = html + '<a href="%s"><img src="%s/images/base/nav_front.png" /> ภาพรวมสำนัก %d</a>' % (reverse('view_sector_overview', args=[sector.ref_no]), settings.MEDIA_URL, sector.ref_no)
        
        elif primary_role.name == 'sector_manager_assistant':
            html = html + '<a href="%s"><img src="%s/images/base/nav_front.png" /> หน้าแรก</a>' % (reverse('view_dashboard'), settings.MEDIA_URL)
        
        elif primary_role.name == 'program_manager':
            html = html + '<a href="%s"><img src="%s/images/base/nav_front.png" /> หน้าแรก</a>' % (reverse('view_dashboard'), settings.MEDIA_URL)
        
        elif primary_role.name == 'program_manager_assistant':
            html = html + '<a href="%s"><img src="%s/images/base/nav_front.png" /> หน้าแรก</a>' % (reverse('view_dashboard'), settings.MEDIA_URL)
    
    if user.is_superuser:
        html = html + '<a href="%s"><img src="%s/images/base/admin.png" class="icon"/> จัดการระบบ</a>' % (reverse('view_administration'), settings.MEDIA_URL)
    
    html = html + '<a href="%s"><img src="%s/images/base/org_chart.png" class="icon"/> ผังองค์กร</a>' % (reverse('view_organization'), settings.MEDIA_URL)
    
    return html

@register.simple_tag
def display_sector_header(user, sector):
    header_html = '<div class="supertitle">'
    
    master_plan_list = []
    for sector_master_plan in SectorMasterPlan.objects.filter(sector=sector):
        master_plan = sector_master_plan.master_plan
        master_plan_list.append(unicode('<a href="%s">แผน %d</a>', 'utf-8') % (reverse('view_master_plan_overview', args=[master_plan.ref_no]), master_plan.ref_no))
    
    header_html = header_html + ' | '.join(master_plan_list)
    header_html = header_html + unicode('</div><h1>สำนัก %d - %s</h1>', 'utf-8') % (sector.ref_no, sector.name)
    return header_html

from helper import permission

@register.simple_tag
def display_master_plan_header(user, master_plan):
    header_html = '<div class="supertitle">'
    
    sector_list = []
    for sector_master_plan in SectorMasterPlan.objects.filter(master_plan=master_plan):
        sector = sector_master_plan.sector
        sector_list.append(unicode('<a href="%s">สำนัก %d</a>', 'utf-8') % (reverse('view_sector_overview', args=[sector.ref_no]), sector.ref_no))
    
    header_html = header_html + ' | '.join(sector_list)
    header_html = header_html + unicode('</div><h1>แผน %d - %s</h1>', 'utf-8') % (master_plan.ref_no, master_plan.name)
    
    if permission.access_obj(user, 'master_plan manage', master_plan):
        header_html = header_html + unicode('<div class="subtitle"><img src="%s/images/icons/settings.png" class="icon" /> <a href="%s">จัดการแผนหลัก</a></div>', 'utf-8') % (settings.MEDIA_URL, reverse('view_master_plan_manage_organization', args=[master_plan.ref_no]))
    
    return header_html

@register.simple_tag
def display_master_plan_management_header(user, master_plan):
    return unicode('<div class="supertitle"><a href="%s">แผน %d - %s</a></div><h1>จัดการแผนหลัก</h1>', 'utf-8') % (reverse('view_master_plan_overview', args=[master_plan.ref_no]), master_plan.ref_no, master_plan.name)

@register.simple_tag
def display_program_header(user, program):
    return unicode('<div class="supertitle"><a href="%s">แผน %d - %s</a></div><h1>แผนงาน (%s) %s</h1>', 'utf-8') % (reverse('view_master_plan_overview', args=[program.plan.master_plan.ref_no]), program.plan.master_plan.ref_no, program.plan.master_plan.name, program.ref_no, program.name)

@register.simple_tag
def display_project_header(user, master_plan):
    pass

@register.simple_tag
def display_activity_header(user, master_plan):
    pass

# ADMIN PAGE

@register.simple_tag
def list_user_roles(user_account):
    role_html = ''
    
    for responsibility in UserRoleResponsibility.objects.filter(user=user_account):
        group_details = GroupDetails.objects.get(group=responsibility.role)
        
        if group_details.level == GroupDetails.SECTOR_LEVEL:
            for sector in responsibility.sectors.all():
                role_html = role_html + unicode('<li>%s - สำนัก %d</li>', 'utf-8') % (group_details.name, sector.ref_no)
            
        elif group_details.level == GroupDetails.PROGRAM_LEVEL:
            for program in responsibility.programs.all():
                role_html = role_html + unicode('<li>%s - แผนงาน %s</li>', 'utf-8') % (group_details.name, program.ref_no)
            
        else:
            role_html = role_html + '<li>%s</li>' % (group_details.name)
    
    return role_html
    