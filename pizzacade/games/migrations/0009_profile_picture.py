# Generated by Django 3.1.3 on 2021-01-05 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0008_auto_20201231_0213'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]