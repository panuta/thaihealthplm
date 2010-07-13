from django.conf.urls.defaults import *

urlpatterns = patterns('budget.views',
    url(r'^master_plan/manage/program/(?P<program_id>\d+)/budget/$', 'view_master_plan_program_budget', name='view_master_plan_program_budget'),
    #url(r'^master_plan/(?P<master_plan_id>\d+)/finance/$', 'view_master_plan_finance', name='view_master_plan_finance'),
    
    #url(r'^project/(?P<project_id>\d+)/finance/$', 'view_project_finance', name='view_project_finance'),
    
    #url(r'^finance/(?P<schedule_id>\d+)/$', 'view_finance_overview', name='view_finance_overview'),
)

#urlpatterns += patterns('finance.ajax',
#    url(r'^ajax/finance/update/$', 'ajax_update_finance_value', name="ajax_update_finance_value"),
#    url(r'^ajax/finance/claim/$', 'ajax_claim_finance_schedule', name="ajax_claim_finance_schedule"),
#)