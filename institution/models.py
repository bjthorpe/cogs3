from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    identity_provider = models.URLField(max_length=200, blank=True)
    logo_path = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
