# Generated by Django 4.0.2 on 2022-02-21 06:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verified', models.BooleanField()),
                ('url', models.URLField()),
                ('description', models.TextField()),
                ('twitter_user_id', models.TextField()),
                ('username', models.CharField(max_length=255)),
                ('protected', models.BooleanField()),
                ('profile_image_url', models.URLField()),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField()),
                ('isAnalysing', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
