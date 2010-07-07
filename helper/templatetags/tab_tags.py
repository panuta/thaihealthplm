# -*- encoding: utf-8 -*-
from django import template
register = template.Library()

from django.core.urlresolvers import reverse

def _generate_tabs(html):
    return '<div id="body-tabs"><ul>%s</ul><div class="clear"></div></div>' % html

@register.simple_tag
def tabs_for_administration(page):
    html = ''
    
    if page == 'organization':
        html = html + '<li class="selected">โครงสร้างองค์กร</li>'
    else:
        html = html + '<li><a href="%s">โครงสร้างองค์กร</a></li>' % reverse('view_administration_organization')
    
    if page == 'users':
        html = html + '<li class="selected">ผู้ใช้ระบบ</li>'
    else:
        html = html + '<li><a href="%s">ผู้ใช้ระบบ</a></li>' % reverse('view_administration_users')
    
    return _generate_tabs(html)

@register.simple_tag
def tabs_for_sector():
    return _generate_tabs()

@register.simple_tag
def tabs_for_master_plan():
    return _generate_tabs()

@register.simple_tag
def tabs_for_manage_master_plan():
    return _generate_tabs()

@register.simple_tag
def tabs_for_program():
    return _generate_tabs()

@register.simple_tag
def tabs_for_project():
    return _generate_tabs()
