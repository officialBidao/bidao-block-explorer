from django.db import models
import datetime
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils import timezone


class Account(models.Model):
    address = models.CharField(max_length=100, blank=False, null=False, db_index=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    balance = models.FloatField(default=0)


class Transaction(models.Model):
    t_from = models.CharField(max_length=100, blank=False, null=False, db_index=True)
    t_to = models.CharField(max_length=100, blank=False, null=False, db_index=True)
    amount = models.FloatField(default=0)
    when = models.DateTimeField(default=timezone.now)
