from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from course.models import Session


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    interest = models.CharField(max_length=100, default='Unanswered')

    def __str__(self):
        return f'{self.user.username} Account'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.session} session payment by {self.user.username}'
