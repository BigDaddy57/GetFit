# Generated by Django 4.2 on 2023-06-01 03:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('GetFit', '0019_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='created_groups', to=settings.AUTH_USER_MODEL),
        ),
    ]
