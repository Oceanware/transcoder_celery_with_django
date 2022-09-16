# Generated by Django 4.0.6 on 2022-08-01 22:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vid', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_description',
            field=models.TextField(default='description'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_title',
            field=models.CharField(default=uuid.uuid4, max_length=200),
        ),
    ]