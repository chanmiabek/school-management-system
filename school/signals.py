from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification, FeeCollection, Event
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Notification)
def send_realtime_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_name = f"user_{instance.user.id}"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "message": instance.message
            }
        )

@receiver(post_save, sender=FeeCollection)
def fee_collection_notif(sender, instance, created, **kwargs):
    if created:
        # Notify all admins about the fee collection
        admins = User.objects.filter(is_superuser=True) # or instance.is_admin if using CustomUser roles
        for admin in admins:
            Notification.objects.create(
                user=admin,
                message=f"New Fee Collection: {instance.amount} from {instance.student.first_name if instance.student else 'Unknown'}"
            )

@receiver(post_save, sender=Event)
def event_notif(sender, instance, created, **kwargs):
    if created:
        # Notify everyone about the new event
        all_users = User.objects.all()
        for user in all_users:
            Notification.objects.create(
                user=user,
                message=f"New Event Scheduled: {instance.title} on {instance.event_date}"
            )
