from django.contrib import admin
from apps.notification.models import Mahalla, Notification, UserNotification


@admin.register(Mahalla)
class MahallaAdmin(admin.ModelAdmin):
    list_display = ["district", "mahalla"]
    list_filter = ["district"]
    search_fields = ["district", "mahalla"]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "image", "date"]
    search_fields = ["title", "description", "mahalla"]


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "notification", "is_read"]
    list_filter = ["is_read"]
    search_fields = ["user", "notification"]