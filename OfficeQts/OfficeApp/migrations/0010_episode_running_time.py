# Generated by Django 3.0.4 on 2020-03-16 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OfficeApp', '0009_episode_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='running_time',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
