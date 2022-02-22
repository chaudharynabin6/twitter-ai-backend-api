from typing import Optional
from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from .models import Tweet,TwitterUserMetaData,TotalSummary,TimeSeriesSummary
# Register your models here.
@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site: Optional[AdminSite]) -> None:
        self.list_display = [str(field.name) for field in Tweet._meta.fields]
        super().__init__(model, admin_site)


@admin.register(TwitterUserMetaData)
class TwitterUserMetaDataAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site: Optional[AdminSite]) -> None:
        self.list_display = [str(field.name) for field in TwitterUserMetaData._meta.fields]
        super().__init__(model, admin_site)


@admin.register(TotalSummary)
class TotalSummaryAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site: Optional[AdminSite]) -> None:
        self.list_display = [str(field.name) for field in TotalSummary._meta.fields]
        super().__init__(model, admin_site)


@admin.register(TimeSeriesSummary)
class TimeSeriesSummaryAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site: Optional[AdminSite]) -> None:
        self.list_display = [str(field.name) for field in TimeSeriesSummary._meta.fields]
        super().__init__(model, admin_site)