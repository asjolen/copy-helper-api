from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from team.models import Team
from team.models import Team
from django.db.models import JSONField
from django.contrib.auth.models import User


class Object(MPTTModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(blank=False, null=False, max_length=100)
    type = models.IntegerField()
    sub_type = models.IntegerField(null=True, blank=True)
    deleted = models.DateTimeField(auto_now=False, blank=True, null=True)
    settings = JSONField(default=dict)
    uuid = models.CharField(blank=True, null=True, max_length=255, unique=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Object, self).save(*args, **kwargs)


class Favorite(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Favorite, self).save(*args, **kwargs)


class Access(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_access")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name="team_access")

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Access, self).save(*args, **kwargs)


class Editor(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Editor, self).save(*args, **kwargs)


class Reserved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.CharField(blank=True, null=True, max_length=255, unique=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Reserved, self).save(*args, **kwargs)
