# Generated by Django 4.2 on 2023-06-06 04:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('GetFit', '0033_discussion_image_discussion_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='invited_users',
            field=models.ManyToManyField(related_name='invited_groups', to=settings.AUTH_USER_MODEL),
        ),
    ]
