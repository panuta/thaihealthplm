from django.conf.urls.defaults import *

urlpatterns = patterns('progress.views',
    url(r'^sector/(?P<sector_ref_no>\d+)/progress/$', 'view_sector_progress', name='view_sector_progress'),
    url(r'^master_plan/(?P<master_plan_ref_no>\d+)/progress/$', 'view_master_plan_progress', name='view_master_plan_progress'),
    url(r'^program/(?P<program_id>\d+)/progress/$', 'view_program_progress', name='view_program_progress'),
    url(r'^project/(?P<project_id>\d+)/progress/$', 'view_project_progress', name='view_project_progress'),
    url(r'^project/(?P<project_id>\d+)/document/$', 'view_project_document', name='view_project_document'),
    url(r'^activity/(?P<activity_id>\d+)/progress/$', 'view_activity_progress', name='view_activity_progress'),
)
