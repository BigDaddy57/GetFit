# Generated by Django 4.2 on 2023-06-06 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GetFit', '0028_joinrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='join_requests',
        ),
        migrations.AlterField(
            model_name='joinrequest',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='join_requests', to='GetFit.group'),
        ),
    ]
