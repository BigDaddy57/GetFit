# Generated by Django 4.2 on 2023-05-08 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GetFit', '0005_rename_instagram_link_userprofile_instagram_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='instagram',
            new_name='instagram_link',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='twitter',
            new_name='twitter_link',
        ),
    ]