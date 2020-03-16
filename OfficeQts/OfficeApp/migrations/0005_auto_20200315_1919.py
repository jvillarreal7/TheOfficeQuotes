# Generated by Django 3.0.4 on 2020-03-16 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OfficeApp', '0004_auto_20200315_1901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episode',
            name='number',
        ),
        migrations.AddField(
            model_name='episode',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='episode',
            name='season',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='OfficeApp.Season'),
            preserve_default=False,
        ),
    ]