from django.db import models

class MasterPlanKPI(models.Model):
	master_plan = models.ForeignKey('domain.MasterPlan')
	ref_no = models.CharField(max_length=100)
	name = models.CharField(max_length=1000)
	abbr_name = models.CharField(max_length=200)
	unit_name = models.CharField(max_length=100)
	enabled = models.BooleanField(default=True)

class MasterPlanKPISchedule(models.Model):
	kpi = models.ForeignKey('MasterPlanKPI')
	program = models.ForeignKey('domain.Program')
	target = models.IntegerField()
	result = models.IntegerField()
	quarter = models.IntegerField() # 1-4
	quarter_year = models.IntegerField() # gregorian calendar year

class MasterPlanKPIScheduleRevision(models.Model):
	schedule = models.ForeignKey('MasterPlanKPISchedule')
	target = models.IntegerField()
	result = models.IntegerField()
	quarter = models.IntegerField() # 1-4
	quarter_year = models.IntegerField() # gregorian calendar year
	revised = models.DateTimeField(auto_now_add=True)
	revised_by = models.ForeignKey('accounts.UserAccount')

class MasterPlanKPIScheduleRelatedProject(models.Model):
	schedule = models.ForeignKey('MasterPlanKPISchedule')
        project = models.ForeignKey('domain.Project')
