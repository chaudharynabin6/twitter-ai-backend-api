from django.contrib import admin
from .models import TwitterUser
# Register your models here.
@admin.register(TwitterUser)
class TwitterUserAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site) -> None:
        self.list_display = [str(field.name) for field in TwitterUser._meta.fields]
        super().__init__(model, admin_site)