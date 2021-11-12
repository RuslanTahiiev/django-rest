from django.contrib import admin
from django.contrib.admin import ModelAdmin

from homeapp.models import SiteUpdateNews


@admin.register(SiteUpdateNews)
class SiteUpdateNewsAdmin(ModelAdmin):
    pass
