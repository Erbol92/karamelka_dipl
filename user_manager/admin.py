from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
# Register your models here.

admin.site.unregister(User)

class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 1
    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe(f'<img style="width:96px" src="{obj.photo.url}">')
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    inlines = [
        ProfileInline,
    ]

    