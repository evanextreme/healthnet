from django.contrib import admin
from EventLog.models import Log
from django.core.exceptions import PermissionDenied


class LogAdmin(admin.ModelAdmin):

    raw_id_fields = ["user"]
    list_filter = ["action", "timestamp"]
    list_display = ["timestamp", "user", "action", "notes"]
    search_fields = ["user__username", "user__email", "timestamp", "action", "notes"]
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def save_model(self, *args, **kwargs):
        raise PermissionDenied

admin.site.register(Log, LogAdmin)
