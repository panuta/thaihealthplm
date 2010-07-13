from django.conf.urls.defaults import *

urlpatterns = patterns('budget.views',
    url(r'^sector/(?P<sector_ref_no>\d+)/budget/$', 'view_sector_budget', name='view_sector_budget'),
    
    url(r'^master_plan/manage/program/(?P<program_id>\d+)/budget/$', 'view_master_plan_program_budget', name='view_master_plan_program_budget'),
    url(r'^master_plan/(?P<master_plan_ref_no>\d+)/budget/$', 'view_master_plan_budget', name='view_master_plan_budget'),
    
    url(r'^program/(?P<program_id>\d+)/budget/$', 'view_program_budget', name='view_program_budget'),
    
    url(r'^budget/(?P<schedule_id>\d+)/$', 'view_budget_overview', name='view_budget_overview'),
)

#urlpatterns += patterns('finance.ajax',
#    url(r'^ajax/finance/update/$', 'ajax_update_finance_value', name="ajax_update_finance_value"),
#    url(r'^ajax/finance/claim/$', 'ajax_claim_finance_schedule', name="ajax_claim_finance_schedule"),
#)