# Generated by Django 5.1.4 on 2024-12-08 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='two_fa_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='two_fa_secret',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
