from django.db import models

# Create your models here.

class Profile(models.Model):
  name = models.CharField(max_length=100, blank=False, null=False, db_index=True)
