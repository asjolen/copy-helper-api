from django.db import models
from object.models import Object
from team.models import Team
from django.contrib.auth.models import User


class Recipes(models.Model):
    identifier = models.CharField(max_length=255, blank=False, null=False, unique=True)
    data = models.JSONField()
    fields = models.JSONField()
    settings = models.JSONField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Recipes, self).save(*args, **kwargs)


class Custom(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    data = models.JSONField()
    fields = models.JSONField()
    settings = models.JSONField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Custom, self).save(*args, **kwargs)


class Favorites(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Favorites, self).save(*args, **kwargs)
