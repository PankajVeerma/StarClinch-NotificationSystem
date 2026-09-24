from django.contrib import admin

from .models import ( NotificationTrigger, NotificationTemplate,)


@admin.register(NotificationTrigger)
class NotificationTriggerAdmin(admin.ModelAdmin):
    list_display = ("name","code","is_active","created_at",)
    list_filter = ("is_active",)
    search_fields = ("name","code",)


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ("trigger","channel","is_active","created_at",)
    list_filter = ("channel","is_active",)
    search_fields = ("trigger__name","trigger__code","body",)