import io

import ffmpeg_streaming
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render

from vid.forms import VideoForm
from vid.models import Video
from vid.tasks import transcode


def home_view(request):
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

    form = VideoForm(request.POST or None, request.FILES or None)
    if request.POST:

        if form.is_valid():
            form.save()

    context = {
        'form': form
    }

    return render(request, 'home.html', context)
