from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views
from .views import SiteUpdateNewsViewSet

router = SimpleRouter()

router.register(r'updates', SiteUpdateNewsViewSet)

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += router.urls
