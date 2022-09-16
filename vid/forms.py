from django.forms import ModelForm

from vid.models import Video


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = '__all__'
        exclude = ('video_status',)

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
