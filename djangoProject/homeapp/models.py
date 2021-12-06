from django.contrib.auth.models import User
from django.db import models


class SiteUpdateNews(models.Model):

    # id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    intro = models.CharField(max_length=250)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_updatenews')
    watchers = models.ManyToManyField(User, through='UserUpdateNewsRelation', related_name='updatenews_watchers')

    def __str__(self):
        return f'ID#{self.id}: {self.title}'


class UserUpdateNewsRelation(models.Model):

    RATE_CHOISES = (
        (1, 'Bad'),
        (2, 'Not Bad'),
        (3, 'Ok'),
        (4, 'Fine'),
        (5, 'Amazing')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_news = models.ForeignKey(SiteUpdateNews, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOISES, null=True)

    def __str__(self):
        return f'User: {self.user.username}: {self.rate}'
