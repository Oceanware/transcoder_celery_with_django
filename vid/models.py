from django.db import models
from uuid import uuid4


# Create your models here.


class Video(models.Model):
    video_title = models.CharField(max_length=200, default=uuid4)
    video_description = models.TextField(default='description')
    video_file = models.FileField(upload_to='videos/')
    video_status = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.video_title
