# Generated by Django 3.1.3 on 2020-12-26 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_profile_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='education',
            field=models.CharField(blank=True, choices=[('Intell', 'Intell'), ('Regular', 'Regular'), ('Under Educated', 'Under Educated')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='intelligence',
            field=models.CharField(blank=True, choices=[('Intellectual', 'Intellectual'), ('Regular', 'Regular'), ('Not at All', 'Not at All')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='type',
            field=models.CharField(blank=True, choices=[('Type A', 'Type A'), ('Type B', 'Type B')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='temperament',
            field=models.CharField(blank=True, choices=[('Boring', 'Boring'), ('Quiet', 'Quiet'), ('Loud', 'Loud')], max_length=24, null=True),
        ),
    ]