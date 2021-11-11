from rest_framework.serializers import ModelSerializer
from homeapp.models import SiteUpdateNews


class SiteUpdateNewsSerializer(ModelSerializer):
    class Meta:
        model = SiteUpdateNews
        fields = ('id', 'title', 'intro', 'text', 'date')
