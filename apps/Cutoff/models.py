from django.db import models


class TaskIdentification(models.Model):
    task_id = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    time_creation = models.DateTimeField(auto_now=True)
