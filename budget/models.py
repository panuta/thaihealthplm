from django.db import models

class MasterPlanBudget(models.Model):
	master_plan = models.ForeignKey('domain.MasterPlan')
	budget = models.IntegerField(default=0) # budget amount from board
	year = models.IntegerField() # gregorian calendar year

class MasterPlanBudgetRevision(models.Model):
	master_plan = models.ForeignKey('domain.MasterPlan')
	budget = models.IntegerField()
	year = models.IntegerField()
	revised = models.DateTimeField(auto_now_add=True)
        revised_by = models.ForeignKey('accounts.UserAccount')

class PlanBudget(models.Model):
	plan = models.ForeignKey('domain.Plan')
	budget = models.IntegerField(default=0) # budget amount that sector planned
	year = models.IntegerField() # gregorian calendar year

class PlanBudgetRevision(models.Model):
	plan = models.ForeignKey('domain.Plan')
	budget = models.IntegerField()
	year = models.IntegerField()
	revised = models.DateTimeField(auto_now_add=True)
        revised_by = models.ForeignKey('accounts.UserAccount')

class ProgramBudgetSchedule(models.Model):
	program = models.ForeignKey('domain.Program')
	grant_budget = models.IntegerField(default=0)
	claim_budget = models.IntegerField(default=0)
	schedule_on = models.DateField()

class ProgramBudgetScheduleRevision(models.Model):
	program = models.ForeignKey('domain.Program')
	grant_budget = models.IntegerField()
	claim_budget = models.IntegerField()
	schedule_on = models.DateField()
	revised = models.DateTimeField(auto_now_add=True)
        revised_by = models.ForeignKey('accounts.UserAccount')

class ClaimReport(models.Model):
	schedule = models.ForeignKey('ProgramBudgetSchedule')
	content = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
        created_by = models.ForeignKey('accounts.UserAccount')

class ClaimReportAttachment(models.Model):
	report = models.ForeignKey('ClaimReport')
	filename = models.CharField(max_length=500)

class ClaimReportRelatedProject(models.Model):
	report = models.ForeignKey('ClaimReport')
	project = models.ForeignKey('domain.Project')

