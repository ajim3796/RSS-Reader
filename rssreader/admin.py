from django.contrib import admin

from .models import RssModel


@admin.register(RssModel)
class RssModel(admin.ModelAdmin):
    pass
