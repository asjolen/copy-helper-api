from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import User


class Extended(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(blank=True, null=True, max_length=255)
    given_name = models.CharField(blank=True, null=True, max_length=255)
    family_name = models.CharField(blank=True, null=True, max_length=255)
    user_language = models.CharField(blank=True, null=True, max_length=255)
    name = models.CharField(blank=True, null=True, max_length=255)
    picture = models.CharField(blank=True, null=True, max_length=255)
    settings = JSONField(default=dict)

    email_verified = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Extended, self).save(*args, **kwargs)