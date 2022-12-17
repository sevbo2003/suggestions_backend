from django.contrib import admin
from apps.notification.models import Mahalla


@admin.register(Mahalla)
class MahallaAdmin(admin.ModelAdmin):
    list_display = ["district", "mahalla"]
    list_filter = ["district"]
    search_fields = ["district", "mahalla"]