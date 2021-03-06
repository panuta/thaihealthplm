# -*- encoding: utf-8 -*-
from django import template
register = template.Library()

from django.core.urlresolvers import reverse

def _generate_tabs(html):
    return '<div id="body-tabs"><ul>%s</ul><div class="clear"></div></div>' % html

@register.simple_tag
def tabs_for_administration(page):
    html = ''
    
    if page == 'organization': html = html + '<li class="selected">โครงสร้างองค์กร</li>'
    else: html = html + '<li><a href="%s">โครงสร้างองค์กร</a></li>' % reverse('view_administration_organization')
    
    if page == 'users': html = html + '<li class="selected">ผู้ใช้ระบบ</li>'
    else: html = html + '<li><a href="%s">ผู้ใช้ระบบ</a></li>' % reverse('view_administration_users')
    
    return _generate_tabs(html)

@register.simple_tag
def tabs_for_sector(page, user, sector):
    html = ''
    
    if page == 'overview': html = html + '<li class="selected">ภาพรวม</li>'
    else: html = html + '<li><a href="%s">ภาพรวม</a></li>' % reverse('view_sector_overview', args=[sector.ref_no])
    
    if page == 'progress': html = html + '<li class="selected">ความก้าวหน้า</li>'
    else: html = html + '<li><a href="%s">ความก้าวหน้า</a></li>' % reverse('view_sector_progress', args=[sector.ref_no])
    
    if page == 'kpi': html = html + '<li class="selected">แผนผลลัพธ์</li>'
    else: html = html + '<li><a href="%s">แผนผลลัพธ์</a></li>' % reverse('view_sector_kpi', args=[sector.ref_no])
    
    if page == 'budget': html = html + '<li class="selected">แผนการเงิน</li>'
    else: html = html + '<li><a href="%s">แผนการเงิน</a></li>' % reverse('view_sector_budget', args=[sector.ref_no])
    
    return _generate_tabs(html)

@register.simple_tag
def tabs_for_master_plan(page, user, master_plan):
    html = ''
    
    if page == 'overview': html = html + '<li class="selected">ภาพรวม</li>'
    else: html = html + '<li><a href="%s">ภาพรวม</a></li>' % reverse('view_master_plan_overview', args=[master_plan.ref_no])
    
    if page == 'programs': html = html + '<li class="selected">แผนงาน/โครงการ</li>'
    else: html = html + '<li><a href="%s">แผนงาน/โครงการ</a></li>' % reverse('view_master_plan_programs', args=[master_plan.ref_no])
    
    if page == 'progress': html = html + '<li class="selected">ความก้าวหน้า</li>'
    else: html = html + '<li><a href="%s">ความก้าวหน้า</a></li>' % reverse('view_master_plan_progress', args=[master_plan.ref_no])
    
    if page == 'kpi': html = html + '<li class="selected">แผนผลลัพธ์</li>'
    else: html = html + '<li><a href="%s">แผนผลลัพธ์</a></li>' % reverse('view_master_plan_kpi', args=[master_plan.ref_no])
    
    if page == 'budget': html = html + '<li class="selected">แผนการเงิน</li>'
    else: html = html + '<li><a href="%s">แผนการเงิน</a></li>' % reverse('view_master_plan_budget', args=[master_plan.ref_no])
    
    return _generate_tabs(html)

@register.simple_tag
def tabs_for_manage_master_plan(page, master_plan):
    html = ''
    
    if page == 'organization': html = html + '<li class="selected">แผนงาน/โครงการ</li>'
    else: html = html + '<li><a href="%s">แผนงาน/โครงการ</a></li>' % reverse('view_master_plan_manage_organization', args=[master_plan.ref_no])
    
    if page == 'kpi': html = html + '<li class="selected">ตัวชี้วัด</li>'
    else: html = html + '<li><a href="%s">ตัวชี้วัด</a></li>' % reverse('view_master_plan_manage_kpi', args=[master_plan.ref_no])
    
    return _generate_tabs(html)

@register.simple_tag
def tabs_for_program(page, user, program):
    html = ''
    
    if page == 'overview': html = html + '<li class="selected">ภาพรวม</li>'
    else: html = html + '<li><a href="%s">ภาพรวม</a></li>' % reverse('view_program_overview', args=[program.id])
    
    if page == 'progress': html = html + '<li class="selected">ความก้าวหน้า</li>'
    else: html = html + '<li><a href="%s">ความก้าวหน้า</a></li>' % reverse('view_program_progress', args=[program.id])
    
    if page == 'kpi': html = html + '<li class="selected">แผนผลลัพธ์</li>'
    else: html = html + '<li><a href="%s">แผนผลลัพธ์</a></li>' % reverse('view_program_kpi', args=[program.id])
    
    if page == 'budget': html = html + '<li class="selected">แผนการเงิน</li>'
    else: html = html + '<li><a href="%s">แผนการเงิน</a></li>' % reverse('view_program_budget', args=[program.id])
    
    return _generate_tabs(html)

@register.simple_tag
def tabs_for_project(page, project):
    html = ''
    
    if page == 'overview': html = html + '<li class="selected">ภาพรวม</li>'
    else: html = html + '<li><a href="%s">ภาพรวม</a></li>' % reverse('view_project_overview', args=[project.id])
    
    if page == 'progress': html = html + '<li class="selected">ความก้าวหน้า</li>'
    else: html = html + '<li><a href="%s">ความก้าวหน้า</a></li>' % reverse('view_project_progress', args=[project.id])
    
    if page == 'document': html = html + '<li class="selected">เอกสาร</li>'
    else: html = html + '<li><a href="%s">เอกสาร</a></li>' % reverse('view_project_document', args=[project.id])
    
    return _generate_tabs(html)
