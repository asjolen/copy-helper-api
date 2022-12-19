from django.db import models
from django.contrib.auth.models import User
from team.models import Team


class Usage(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    tokens = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=5)
    ratio = models.IntegerField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Usage, self).save(*args, **kwargs)