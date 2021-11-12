from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from homeapp.models import SiteUpdateNews
from homeapp.permissions import IsOwnerOrStaffOrReadOnly
from homeapp.serializers import SiteUpdateNewsSerializer


def index(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'home/index.html', context)


class SiteUpdateNewsViewSet(ModelViewSet):
    queryset = SiteUpdateNews.objects.all()
    serializer_class = SiteUpdateNewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_fields = ['title']
    search_fields = ['title', 'intro']
    ordering_fields = ['title', 'date']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


def auth(request):
    context = {
        'title': 'Auth'
    }
    return render(request, 'home/oauth.html', context)
