# Generated by Django 3.0.4 on 2020-03-16 02:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OfficeApp', '0007_remove_episode_written_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='written_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='episodes_w', to='OfficeApp.StaffMember'),
        ),
    ]
