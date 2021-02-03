# Generated by Django 3.1.3 on 2021-02-03 02:04

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0013_auto_20210126_0506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=cloudinary.models.CloudinaryField(default='', max_length=255, verbose_name='avatar'),
            preserve_default=False,
        ),
    ]