from django.contrib import admin
from django.contrib.admin import ModelAdmin

from homeapp.models import SiteUpdateNews, UserUpdateNewsRelation


@admin.register(SiteUpdateNews)
class SiteUpdateNewsAdmin(ModelAdmin):
    pass


@admin.register(UserUpdateNewsRelation)
class UserUpdateNewsRelationAdmin(ModelAdmin):
    pass