from django.db import models
from django.db.models.base import Model
import django

# Create your models here.
class Images(models.Model):
    Id = models.AutoField(primary_key=True)
    Filename = models.CharField(max_length=256)
    InsertedAt = models.DateTimeField(django.utils.timezone.now())
    LocalPath = models.CharField(max_length=256)
    S3Path = models.CharField(max_length=256)
    Tag = models.CharField(max_length=256)

