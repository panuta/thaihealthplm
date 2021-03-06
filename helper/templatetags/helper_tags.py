# -*- encoding: utf-8 -*-
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import NodeList

from helper import utilities, permission

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

# PERMISSION

class AccessNode(template.Node):
    """
    Parameter
    user : django.contrib.auth.user object
    permission names : string represents permission names
    object : object to be accessed
    
    Permission Names Guide
    - Use ',' to separate between permission
    - Use '+' in front of permission list to indicate that all permissions listed must meet
    """
    
    def __init__(self, nodelist_true, nodelist_false, user, permission_name, obj):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.user = template.Variable(user)
        self.permission_names = permission_name.strip(' \"\'')
        self.obj = template.Variable(obj)
    
    def render(self, context):
        user = self.user.resolve(context)
        permission_names = self.permission_names
        obj = self.obj.resolve(context)
        
        at_least_one_permission = True
        if permission_names[0] == '+':
            at_least_one_permission = False
            permission_names = permission_names[1:]
        
        permission_names = [permission_name.strip() for permission_name in permission_names.split(',')]
        
        if permission.access_obj(user, permission_names, obj, at_least_one_permission):
            output = self.nodelist_true.render(context)
            return output
        else:
            output = self.nodelist_false.render(context)
            return output

@register.tag(name="access")
def do_access(parser, token):
    try:
        tag_name, user, permission_names, obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "Responsible tag raise ValueError"
    
    nodelist_true = parser.parse(('else', 'endaccess'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endaccess',))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    
    return AccessNode(nodelist_true, nodelist_false, user, permission_names, obj)

# BACK TO PAGE #################################################################

@register.simple_tag
def back_to_this(request):
    back_list = request.GET.getlist('back')
    
    if back_list:
        return 'back=%s&back=%s' % (request.path, '&back='.join(request.GET.getlist('back')))
    else:
        return 'back=%s' % request.path

@register.simple_tag
def back_form(request):
    back_list = request.GET.getlist('back')
    
    str = ''
    for back in back_list:
        if str: str = str + '&'
        str = str + 'back=%s' % back
    
    if str:
        return '<input type="hidden" name="back" value="%s"/>' % str
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

@register.simple_tag
def generate_quarter_table_header(quarter_year):
    from helper.constants import THAI_MONTH_ABBR_NAME
    
    start_month = settings.QUARTER_START_MONTH
    end_month = settings.QUARTER_START_MONTH + 2
    if end_month > 12: end_month = end_month - 12
    
    html = ''
    for i in range(1, 5):
        year = quarter_year
        
        if start_month >= settings.QUARTER_START_MONTH and not settings.QUARTER_LOWER_YEAR_NUMBER:
            year = quarter_year - 1
        
        if start_month < settings.QUARTER_START_MONTH and settings.QUARTER_LOWER_YEAR_NUMBER:
            year = quarter_year + 1
        
        html = html + '<th colspan="2">ไตรมาสที่ %d (%s - %s %d)</th>' % (i, THAI_MONTH_ABBR_NAME[start_month], THAI_MONTH_ABBR_NAME[end_month], year+543)
        
        start_month = start_month + 3
        if start_month > 12: start_month = start_month - 12
        
        end_month = end_month + 3
        if end_month > 12: end_month = end_month - 12
    
    return html
