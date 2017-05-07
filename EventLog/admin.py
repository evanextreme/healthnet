from django.contrib import admin
from EventLog.models import Log
from django.core.exceptions import PermissionDenied


class LogAdmin(admin.ModelAdmin):

    raw_id_fields = ["user"]
    list_filter = ["action", "timestamp"]
    #the fields that will be displayed.
    list_display = ["timestamp", "user", "action", "notes"]
    #the fields that can be used for searching
    search_fields = ["user__username", "user__email", "timestamp", "action", "notes"]
    
    #deny admin for deleting logs
    def has_delete_permission(self, request, obj=None):
        return False
    
    #deny admin for adding/modifying logs
    def save_model(self, *args, **kwargs):
        raise PermissionDenied

admin.site.register(Log, LogAdmin)
