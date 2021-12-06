from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from homeapp.models import SiteUpdateNews, UserUpdateNewsRelation


class SiteUpdateNewsSerializer(ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    # 8, 12:40
    annotated_likes = serializers.IntegerField()

    class Meta:
        model = SiteUpdateNews
        fields = ('id', 'title', 'intro', 'text', 'date', 'likes_count', 'annotated_likes',)

    def get_likes_count(self, instance):
        return UserUpdateNewsRelation.objects.filter(update_news=instance, like=True).count()


class UserUpdateNewsRelationSerializer(ModelSerializer):
    class Meta:
        model = UserUpdateNewsRelation
        fields = ('update_news', 'like', 'rate')
