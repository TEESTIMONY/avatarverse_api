# Generated by Django 5.2.3 on 2025-07-15 19:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_avatar_image_avatar_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction', models.CharField(choices=[('heart', 'Heart'), ('fire', 'Fire'), ('laugh', 'Laugh')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('avatar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='api.avatar')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'avatar')},
            },
        ),
    ]
