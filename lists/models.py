from django.db import models


class Items(models.Model):
    text = models.TextField(default="")
