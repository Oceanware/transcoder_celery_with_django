from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from uuid import uuid4

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


def video_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'videos/{0}/{1}'.format(instance.slug, filename)


class Video(models.Model):
    video_title = models.CharField(max_length=200)
    video_description = models.TextField(null=True, blank=True)
    video_file = models.FileField(upload_to=video_directory_path)
    slug = models.SlugField(max_length=200, null=False, unique=True)
    video_status = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transcode_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.video_title}"

    def save(self, *args, **kwargs):  # new
        self.video_title = uuid4()
        if not self.slug:
            self.slug = slugify(self.video_title)
        return super().save(*args, **kwargs)
