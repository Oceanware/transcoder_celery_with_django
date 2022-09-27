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


async def send_progress(percentage, time_left):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        "admin_notifications", {
            "type": "admin.pusher",
            "notificationType": "notifications",
            "event": "video_transcoding_progress",
            "percentage": percentage,
            "time_left": time_left
        }
    )


def monitor(ffmpeg, duration, time_, time_left, process):
    """
    Handling proccess.

    Examples:
    1. Logging or printing ffmpeg command
    logging.info(ffmpeg) or print(ffmpeg)

    2. Handling Process object
    if "something happened":
        process.terminate()

    3. Email someone to inform about the time of finishing process
    if time_left > 3600 and not already_send:  # if it takes more than one hour and you have not emailed them already
        ready_time = time_left + time.time()
        Email.send(
            email='someone@somedomain.com',
            subject='Your video will be ready by %s' % datetime.timedelta(seconds=ready_time),
            message='Your video takes more than %s hour(s) ...' % round(time_left / 3600)
        )
       already_send = True

    4. Create a socket connection and show a progress bar(or other parameters) to your users
    Socket.broadcast(
        address=127.0.0.1
        port=5050
        data={
            percentage = per,
            time_left = datetime.timedelta(seconds=int(time_left))
        }
    )

    :param ffmpeg: ffmpeg command line
    :param duration: duration of the video
    :param time_: current time of transcoded video
    :param time_left: seconds left to finish the video process
    :param process: subprocess object
    :return: None
    """
    per = round(time_ / duration * 100)
    dt_tl = datetime.timedelta(seconds=int(time_left))
    sys.stdout.write(
        "\rTranscoding...(%s%%) %s left [%s%s]" %
        (per, dt_tl, '#' * per, '-' * (100 - per))
    )
    sys.stdout.flush()
    send_progress(per, dt_tl)


@shared_task
def transcode(video_id):
    print("Video id: ", video_id)
    video = Video.objects.get(id=video_id)
    path = os.path.join(settings.MEDIA_ROOT, "videos", video.slug, "hls.m3u8")

    print("video: ", video)
    print("path: ", path)

    video = ffmpeg_streaming.input(video.video_file.path)

    # hls = video.hls(Formats.h264())
    # hls.auto_generate_representations()

    _360p = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
    _480p = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
    _720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))

    hls = video.hls(Formats.h264())
    hls.representations(_360p, _480p, _720p)

    hls.output(path, monitor=monitor)

    return {"status": True}
