from django.db import models
from django.contrib.auth.models import User

import os


class TaskInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=20, choices=[
        ('classification', 'classification'),
        ('cutoff', 'cutoff'),
    ])
    time_creation = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return os.path.join(self.task_type, self.user.username)
