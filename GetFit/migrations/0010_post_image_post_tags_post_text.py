# Generated by Django 4.2 on 2023-05-12 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GetFit', '0009_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='post',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]
