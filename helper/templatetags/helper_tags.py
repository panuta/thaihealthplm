# -*- encoding: utf-8 -*-
from django import template
register = template.Library()

from django.core.urlresolvers import reverse

from accounts.models import UserRoleResponsibility

from helper import utilities

# DATE TIME #################################################################

@register.filter(name='full_datetime')
def full_datetime(datetime):
    return utilities.format_full_datetime(datetime)

@register.filter(name='abbr_datetime')
def abbr_datetime(datetime):
    return utilities.format_abbr_datetime(datetime)

@register.filter(name='full_date')
def full_date(datetime):
    return utilities.format_full_date(datetime)

@register.filter(name='abbr_date')
def abbr_date(datetime):
    return utilities.format_abbr_date(datetime)

@register.filter(name='full_month_year')
def full_month_year(datetime):
    return utilities.format_full_month_year(datetime)

@register.filter(name='abbr_month_year')
def abbr_month_year(datetime):
    return utilities.format_abbr_month_year(datetime)

@register.filter(name='week_elapse')
def week_elapse(value):
    return utilities.week_elapse_text(value)

# TEMPLATE #################################################################

@register.simple_tag
def display_header_navigation(user, MEDIA_URL):
    html = ''
    
    if user.groups.all():
        primary_role = user.groups.all()[0]
        
        if primary_role.name == 'director':
            html = html + '<a href="%s"><img src="%s/images/base/nav_front.png" /> หน้าผู้จัดการกองทุน</a>' % (reverse('view_dashboard'), MEDIA_URL)
        
        elif primary_role.name == 'sector_manager':
            responsibility = UserRoleResponsibility.objects.get(user=user.get_profile(), role=primary_role)
            sector = responsibility.sectors.all()[0]
            html = html + '<a href="%s"><img src="%s/images/base/nav_front.png" /> ภาพรวมสำนัก %d</a>' % (reverse('view_sector_overview', args=[sector.id]), MEDIA_URL, sector.id)
        
        elif primary_role.name == 'sector_manager_assistant':
            html = html + '<a href="%s"><img src="%s/images/base/nav_front.png" /> หน้าแรก</a>' % (reverse('view_dashboard'), MEDIA_URL)
        
        elif primary_role.name == 'program_manager':
            html = html + '<a href="%s"><img src="%s/images/base/nav_front.png" /> หน้าแรก</a>' % (reverse('view_dashboard'), MEDIA_URL)
        
        elif primary_role.name == 'program_manager_assistant':
            html = html + '<a href="%s"><img src="%s/images/base/nav_front.png" /> หน้าแรก</a>' % (reverse('view_dashboard'), MEDIA_URL)
        
        html = html + '<a href="%s">ผังองค์กร</a>' % reverse('view_organization')
    
    if user.is_superuser:
        html = html + '<a href="%s">จัดการระบบ</a>' % reverse('view_administration')
    
    return html

# FORM #################################################################

@register.simple_tag
def display_required():
    return '<span class="required">* ต้องกรอก</span>'

# MESSAGES #################################################################

@register.simple_tag
def display_messages(messages):
    if messages:
        html = ''
        for message in messages:
            html = html + '<li class="%s">%s</li>' % (message.tags, message)
        
        return '<ul class="ss_messages">%s</ul>' % html
    else:
        return ''

# TEMPLATE #################################################################
@register.simple_tag
def display_pagination(objects, url_name):
    if objects.paginator.num_pages != 1:
        html = ''
        
        if objects.number != 1:
            html = html + '<span><a href="%s">&#171; หน้าแรก</a></span>' % reverse(url_name)
        else:
            html = html + '<span class="disabled">&#171; หน้าแรก</span>'
        
        if objects.has_previous():
            html = html + '<span><a href="%s?p=%d">&#139; ก่อนหน้า</a></span>' % (reverse(url_name), objects.previous_page_number())
        else:
            html = html + '<span class="disabled">&#139; ก่อนหน้า</span>'
        
        html = html + '<span class="number">หน้าที่ %d / %d</span>' % (objects.number, objects.paginator.num_pages)
        
        if objects.has_next():
            html = html + '<span><a href="%s?p=%d">ถัดไป &#155;</a></span>' % (reverse(url_name), objects.next_page_number())
        else:
            html = html + '<span class="disabled">ถัดไป &#155;</span>'
        
        if objects.number != objects.paginator.num_pages:
            html = html + '<span><a href="%s?p=%d">หน้าสุดท้าย &#187;</a></span>' % (reverse(url_name), objects.paginator.num_pages)
        else:
            html = html + '<span class="disabled">หน้าสุดท้าย &#187;</span>'
        
        return '<div class="ss_pagination">%s</div>' % html
    
    else:
        return ''


