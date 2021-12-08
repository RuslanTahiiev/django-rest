from django.db.models import Count, Case, When, Avg, Subquery, Value, F
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from homeapp.models import SiteUpdateNews, UserUpdateNewsRelation
from homeapp.permissions import IsOwnerOrStaffOrReadOnly
from homeapp.serializers import SiteUpdateNewsSerializer, UserUpdateNewsRelationSerializer


def index(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'home/index.html', context)


class SiteUpdateNewsViewSet(ModelViewSet):
    queryset = SiteUpdateNews.objects.all().annotate(
            annotated_likes=Count(Case(When(userupdatenewsrelation__like=True, then=1))),
            rating=Avg('userupdatenewsrelation__rate'),
            owner_name=F('owner__username'),
        ).prefetch_related('watchers').order_by('id')
    serializer_class = SiteUpdateNewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_fields = ['title']
    search_fields = ['title', 'intro']
    ordering_fields = ['title', 'date']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserUpdateNewsRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserUpdateNewsRelation.objects.all()
    serializer_class = UserUpdateNewsRelationSerializer
    lookup_field = 'id'

    def get_object(self):
        obj, _ = UserUpdateNewsRelation.objects.get_or_create(user=self.request.user,
                                                              update_news=SiteUpdateNews.objects.get(
                                                                            pk=int(self.kwargs['id'])
                                                                            )
                                                              )
        return obj


def auth(request):
    context = {
        'title': 'Auth'
    }
    return render(request, 'home/oauth.html', context)
