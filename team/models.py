from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import User
from organization.models import Organization


class Team(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=100)
    subscription = models.IntegerField(default=0)
    settings = JSONField(default=dict)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Team, self).save(*args, **kwargs)


class Member(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="team_member")
    role = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Member, self).save(*args, **kwargs)


class Keywords(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    value = models.CharField(blank=False, null=False, max_length=50)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Keywords, self).save(*args, **kwargs)
