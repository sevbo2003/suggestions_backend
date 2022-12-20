from datetime import datetime

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from apps.notification.models import Notification, UserNotification
from apps.accounts.models import PhoneNumberAbstactUser
from django.db.models import Q 

channel_layer = get_channel_layer()


@shared_task
def send_notification(group_name, message):
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'notification_message',
            'message': message
        }
    )

@shared_task
def save_notification_to_notification_users(notification_id, group_name, message):
    print("Came to task")
    notification = Notification.objects.get(id=notification_id)
    users = PhoneNumberAbstactUser.objects.filter(
        Q(mahallalar__in=notification.mahalla.all()) & Q(is_active=True)
    )
    for user in users:
        UserNotification.objects.create(user=user, notification=notification)
    send_notification.apply_async(args=[group_name, message])
    return {'status': 'success'}
    