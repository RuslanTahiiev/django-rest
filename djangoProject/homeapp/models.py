from django.db import models


class SiteUpdateNews(models.Model):

    # id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    intro = models.CharField(max_length=250)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'ID#{self.id}: {self.title}'
