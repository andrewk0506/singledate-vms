from django.db import models
from .scheduling import Site


class Role(models.Model):

    ROLES = [("A", "ADMIN"), ("V", "VACCINATOR"), ("S", "SUPPORT STAFF")]

    role = models.CharField(max_length=1, choices=ROLES, default=None, null=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
