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

            video_title = form.cleaned_data['video_title']
            vid = Video.objects.get(video_title=video_title)

            # param_file = io.TextIOWrapper(request.FILES['videoz'].file)
            # print(param_file.name)


            transcode.delay(vid.id)
            context = {
                'form': form
            }
            return render(request, 'home.html', context)

    context = {
        'form': form
    }
    return render(request, 'home.html', context)
