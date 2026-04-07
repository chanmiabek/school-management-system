from .models import Notification


def notification_context(request):
    if request.user.is_authenticated:
        unread_notification = Notification.objects.filter(user=request.user, is_read=False)
        return {
            "unread_notification": unread_notification,
            "unread_notification_count": unread_notification.count(),
        }
    return {
        "unread_notification": [],
        "unread_notification_count": 0,
    }
