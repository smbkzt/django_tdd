from django.db import models


class Lists(models.Model):
    pass


class Items(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(Lists, on_delete="CASCADE")
