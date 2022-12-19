from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(blank=False, null=False, max_length=255, unique=True)
    website = models.CharField(blank=True, null=True, max_length=255)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Organization, self).save(*args, **kwargs)


class Member(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Member, self).save(*args, **kwargs)


class Invitation(models.Model):
    email = models.CharField(blank=True, null=True, max_length=255)
    role = models.IntegerField(default=0)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Invitation, self).save(*args, **kwargs)
