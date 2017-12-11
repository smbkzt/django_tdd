from django.db import models
from django.urls import reverse


class Lists(models.Model):
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Items(models.Model):
    text = models.TextField(blank=False)
    list = models.ForeignKey(Lists, on_delete="CASCADE")
