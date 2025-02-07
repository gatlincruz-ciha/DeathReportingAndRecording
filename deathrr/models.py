import datetime

from django.db import models


class DeceasedEntry(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by = models.CharField(max_length=100, null=True, blank=True, default="jill.sain@cherokeehospital.org")
    last_modified_by = models.CharField(max_length=100, null=True, blank=True, default="")
    deleted_flag = models.BooleanField(null=True, blank=True, default=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    chart_num = models.CharField(max_length=15, null=True, blank=True)
    dob = models.DateField(null=True, blank=True, default=datetime.date(2030,1,1))
    state_where_died = models.CharField(max_length=15, null=True, blank=True, default="North Carolina")
    death_cert_num = models.CharField(max_length=20, null=True, blank=True)
    dod = models.DateField(null=False, blank=False)
    place_of_death = models.CharField(max_length=50,null=True, blank=True)
    race = models.CharField(max_length=80, null=True, blank=True)
    autopsy_performed = models.BooleanField(default=False)
    manner_of_death = models.CharField(max_length=30, null=True, blank=True)
    death_by_work_injury = models.BooleanField(default=False)
    place_of_injury = models.CharField(max_length=50, blank=True, null=True)
    method_of_verification = models.CharField(max_length=50, default="")

    empty_value_display = "-empty-"


class ICDCode(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=10, default="")
    description = models.CharField(max_length=100, default="")
    type = models.CharField(max_length=2, default="")
    ien = models.IntegerField(default=1)

    def __str__(self):
        return str(self.code) + " - " + str(self.description)


class DeceasedCodes(models.Model):
    id = models.BigAutoField(primary_key=True)
    code_id = models.ForeignKey(ICDCode, on_delete=models.CASCADE)
    deceased_id = models.ForeignKey(DeceasedEntry, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)




