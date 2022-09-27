from django.forms import ModelForm

from vid.models import Video


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = '__all__'
        exclude = ('video_status', 'transcode_complete', 'slug', 'video_title', 'video_description')  # remove video_title & video_description

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
