from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from homeapp.models import SiteUpdateNews
from homeapp.serializers import SiteUpdateNewsSerializer


def index(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'home/index.html', context)


class SiteUpdateNewsViewSet(ModelViewSet):
    queryset = SiteUpdateNews.objects.all()
    serializer_class = SiteUpdateNewsSerializer
