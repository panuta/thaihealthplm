from django.db import models

# Master Plan Progress Report
class MasterPlanReport(models.Model):
    master_plan = models.ForeignKey('domain.MasterPlan')
    content = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.UserAccount')

class MasterPlanReportAttachment(models.Model):
    report = models.ForeignKey('MasterPlanReport')
    filename = models.CharField(max_length=500)


class MasterPlanSubReport(models.Model):
    master_plan = models.ForeignKey('domain.MasterPlan')
    content = models.TextField(null=True)

class MasterPlanSubReportAttachment(models.Model):
    report = models.ForeignKey('MasterPlanSubReport')
    filename = models.CharField(max_length=500)

class MasterPlanSubReportPrograms(models.Model):
    report = models.ForeignKey('MasterPlanSubReport')
    program = models.ForeignKey('domain.Program')

# Program Progress Report
class ProgramReport(models.Model):
    program = models.ForeignKey('domain.Program')
    content = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.UserAccount')
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)

class ProgramReportAttachment(models.Model):
    report = models.ForeignKey('ProgramReport')
    filename = models.CharField(max_length=500)

class ProgramReportProjects(models.Model):
    report = models.ForeignKey('ProgramReport')
    project = models.ForeignKey('domain.Project')

# Project Progress
class ProjectProgress(models.Model):
    project = models.ForeignKey('domain.Project', unique=True)
    manual_progress = models.IntegerField(default=0, null=True)
    current_situation = models.CharField(max_length=500)
    quality = models.IntegerField(default=0, null=True)

class ProjectProblem(models.Model):
    project = models.ForeignKey('domain.Project')
    problem = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.UserAccount')
    fixed = models.BooleanField(default=False)
    fixed_on = models.DateTimeField(null=True)

class ProjectDocument(models.Model):
    project = models.ForeignKey('domain.Project')
    document_name = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.UserAccount')

# Activity Progress
class ActivityProgress(models.Model):
    activity = models.ForeignKey('domain.Activity', unique=True)
    progress = models.IntegerField(default=0)
    current_situation = models.CharField(max_length=500)
    summary = models.TextField()
    detail = models.TextField()

class ActivityDocument(models.Model):
    activity = models.ForeignKey('domain.Activity')
    document_name = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.UserAccount')
