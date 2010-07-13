from django.conf.urls.defaults import *

urlpatterns = patterns('progress.views',
    url(r'^sector/(?P<sector_ref_no>\d+)/progress/$', 'view_sector_progress', name='view_sector_progress'),
    url(r'^master_plan/(?P<master_plan_ref_no>\d+)/progress/$', 'view_master_plan_progress', name='view_master_plan_progress'),
    url(r'^program/(?P<program_id>\d+)/progress/$', 'view_program_progress', name='view_program_progress'),
)