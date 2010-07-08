# -*- encoding: utf-8 -*-
from django import template
register = template.Library()

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

