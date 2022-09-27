import io

import ffmpeg_streaming
from django.shortcuts import render

from vid.forms import VideoForm
from vid.models import Video
from vid.tasks import transcode


def home_view(request):
    form = VideoForm(request.POST or None, request.FILES or None)
    if request.POST:

        if form.is_valid():
            form.save()

    context = {
        'form': form
    }

    return render(request, 'home.html', context)
