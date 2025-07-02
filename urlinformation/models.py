from django.db import models


class URLInformationModel(models.Model):
    url = models.URLField(primary_key=True)
    domain_name = models.CharField(max_length=255)
    protocol = models.CharField(max_length=15)
    title = models.TextField(blank=True)
    images = models.JSONField(default=list)
    stylesheets = models.IntegerField()
