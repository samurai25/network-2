# Generated by Django 3.2.12 on 2024-05-31 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20240508_2130'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Follows',
            new_name='Following',
        ),
        migrations.RemoveField(
            model_name='user',
            name='follows',
        ),
        migrations.RemoveField(
            model_name='user',
            name='follows_people',
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='following', to='network.Following'),
        ),
    ]
