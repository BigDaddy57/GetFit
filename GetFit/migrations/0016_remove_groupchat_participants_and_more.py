# Generated by Django 4.2 on 2023-05-17 02:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GetFit', '0015_conversation_groupchat_user_message_groupchatmessage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupchat',
            name='participants',
        ),
        migrations.RemoveField(
            model_name='groupchatmessage',
            name='group_chat',
        ),
        migrations.RemoveField(
            model_name='groupchatmessage',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='message',
            name='conversation',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.DeleteModel(
            name='Conversation',
        ),
        migrations.DeleteModel(
            name='GroupChat',
        ),
        migrations.DeleteModel(
            name='GroupChatMessage',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]