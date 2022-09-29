from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Video
from .tasks import transcode
from asgiref.sync import async_to_sync, sync_to_async


def send_progress(percentage, time_left):
    print('hii 5')
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "admin_notifications", {
            "type": "admin.pusher",
            "notificationType": "notifications",
            "event": "video_transcoding_progress",
            "percentage": percentage,
            "time_left": time_left
        }
    )


@receiver(post_save, sender=Video)
def start_transcoding(sender, instance, **kwargs):
    if not instance.transcode_complete:
        send_progress(12, "3fdgdfgd")
        transcode.delay(instance.id)


@receiver(post_save, sender=Video)
def start_transcoding(sender, instance, **kwargs):
    if not instance.transcode_complete:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "admin_notifications", {
                "type": "admin.pusher",
                "notificationType": "notifications",
                "event": "video_transcoding_progress",
                "percentage": '12',
                "time_left": 'time_left'
            }
        )
        # transcode.delay(instance.id)
