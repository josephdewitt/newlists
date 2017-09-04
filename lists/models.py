from django.db import models
from django.core.urlresolvers import reverse


class List(models.Model):
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    #id = models.IntegerField(default='',primary_key=True)
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    class Meta:
        ordering = ('id',)
        unique_together = ('list','text')






