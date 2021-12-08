from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from homeapp.models import SiteUpdateNews, UserUpdateNewsRelation


class SiteUpdateNewsWatchersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class SiteUpdateNewsSerializer(ModelSerializer):
    # 1st (annotate likes)
    annotated_likes = serializers.IntegerField(read_only=True)
    # 2nd (annotate rating)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    owner_name = serializers.CharField(read_only=True)
    watchers = SiteUpdateNewsWatchersSerializer(many=True, read_only=True)

    class Meta:
        model = SiteUpdateNews
        fields = ('id', 'title', 'intro', 'text', 'date', 'annotated_likes', 'rating', 'owner_name', 'watchers')


class UserUpdateNewsRelationSerializer(ModelSerializer):
    class Meta:
        model = UserUpdateNewsRelation
        fields = ('update_news', 'like', 'rate')
