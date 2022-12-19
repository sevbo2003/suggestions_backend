# from apps.notification.models import Notification
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# from apps.notification.tasks import send_notification
# from apps.notification.serializers import NotificationSerializer, NotificationCreateSerializer


# @receiver(post_save, sender=Notification, dispatch_uid="notification_message")
# def notification_message(sender, instance, created, **kwargs):
#     # save_m2m
#     if created:
#         serializer = NotificationSerializer(instance=instance)
#         send_notification.apply_async(args=['notification', NotificationSerializer(instance).data])
  
