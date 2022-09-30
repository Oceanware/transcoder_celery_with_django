from asgiref.sync import async_to_sync, sync_to_async
from celery import shared_task
from ffmpeg_streaming import Representation, Size, Bitrate, Formats
import concurrent.futures as cf
from ffmpeg_streaming import Formats
import sys, os
import datetime
import ffmpeg_streaming
import io
from concurrent.futures import as_completed, wait
from django.conf import settings
from vid.models import Video
from channels.layers import get_channel_layer
from celery.concurrency.thread import TaskPool


@shared_task(bind=True, name='queue_ws_event', ignore_result=True, queue='wsQ')
def queue_ws_event(self, ws_channel, ws_event: dict, group=True):
    channel_layer = get_channel_layer()
    # print(ws_channel, ws_event)
    if group:
        async_to_sync(channel_layer.group_send)(ws_channel, ws_event)
    else:
        async_to_sync(channel_layer.send)(ws_channel, ws_event)


def send_progress(percentage, time_left, vid, vname):
    queue_ws_event.delay("admin_notifications",
                         {
                             "type": "admin.pusher",
                             "notificationType": "notifications",
                             "event": "video_transcoding_progress",
                             "per": percentage,
                             "time_left": time_left,
                             "id": vid,
                             "name": vname
                         }
                         )


def make_video_monitor(vid, vname):
    def monitor(ffmpeg, duration, time_, time_left, process):
        per = round(time_ / duration * 100)
        dt_tl = datetime.timedelta(seconds=int(time_left))
        sys.stdout.write(
            "\rTranscoding...(%s%%) %s left [%s%s]" %
            (per, dt_tl, '#' * per, '-' * (100 - per))
        )
        sys.stdout.flush()
        send_progress(per, str(dt_tl), vid, vname)

    return monitor


@shared_task
def transcode(video_id):
    # print("Video id: ", video_id)
    video = Video.objects.get(id=video_id)
    vname = video.video_title
    path = os.path.join(settings.MEDIA_ROOT, "videos", video.slug, "hls.m3u8")

    video = ffmpeg_streaming.input(video.video_file.path)

    # hls = video.hls(Formats.h264())
    # hls.auto_generate_representations()

    _360p = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
    _480p = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
    _720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))

    hls = video.hls(Formats.h264())
    hls.representations(_360p, _480p, _720p)

    hls.output(path, monitor=make_video_monitor(video_id, vname))

    return {"status": True}
