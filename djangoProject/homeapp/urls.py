from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import SimpleRouter
from . import views
from .views import SiteUpdateNewsViewSet

router = SimpleRouter()

router.register(r'updates', SiteUpdateNewsViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    url('', include('social_django.urls', namespace='social')),
]

urlpatterns += router.urls
