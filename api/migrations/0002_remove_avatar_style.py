# Generated by Django 5.2.3 on 2025-06-30 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avatar',
            name='style',
        ),
    ]
