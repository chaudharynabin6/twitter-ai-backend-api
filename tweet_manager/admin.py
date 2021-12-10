from typing import Optional
from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from .models import Tweet,TwittterUser
# Register your models here.
@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site: Optional[AdminSite]) -> None:
        self.list_display = [str(field.name) for field in Tweet._meta.fields]
        super().__init__(model, admin_site)

@admin.register(TwittterUser)
class TwitterUserAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site: Optional[AdminSite]) -> None:
        self.list_display = [str(field.name) for field in TwittterUser._meta.fields]
        super().__init__(model, admin_site)