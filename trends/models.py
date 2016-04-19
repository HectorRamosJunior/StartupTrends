from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Startup(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200, null=True)
    yc_class = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Technology(models.Model):
    name = models.CharField(max_length=200)
    startups = models.ManyToManyField(Startup)

class Service(models.Model):
    name = models.CharField(max_length=200)
    technologies = models.ForeignKey(Technology)

